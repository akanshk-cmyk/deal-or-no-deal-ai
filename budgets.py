"""Pure cumulative allowance arithmetic; no provider dispatch or timing claims."""

from dataclasses import asdict, dataclass, field, replace
from decimal import Decimal, localcontext

from .context import InputError, canonical_decimal


class BudgetExceeded(ValueError):
    pass


@dataclass(frozen=True)
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    attempts: int = 0
    nodes: int = 0
    tools: int = 0
    active_ms: int = 0
    cost_usd: Decimal = Decimal("0")

    def __post_init__(self):
        for name, value in asdict(self).items():
            if name == "cost_usd":
                if not isinstance(value, Decimal) or not value.is_finite() or value < 0:
                    raise InputError("INVALID_COST")
            elif type(value) is not int or value < 0:
                raise InputError("INVALID_USAGE_COUNTER")

    def __add__(self, other):
        with localcontext() as context:
            context.prec = 50
            return Usage(**{key: value + getattr(other, key) for key, value in asdict(self).items()})

    def within(self, maximum: "Usage") -> bool:
        return all(value <= getattr(maximum, name) for name, value in asdict(self).items())

    def to_dict(self):
        return {**asdict(self), "cost_usd": canonical_decimal(self.cost_usd)}

    @classmethod
    def from_dict(cls, data: dict):
        if set(data) != set(cls.__dataclass_fields__) or type(data["cost_usd"]) is not str:
            raise InputError("INVALID_USAGE_SCHEMA")
        cost = Decimal(data["cost_usd"])
        if canonical_decimal(cost) != data["cost_usd"]:
            raise InputError("NONCANONICAL_SAVED_COST")
        return cls(**{**data, "cost_usd": cost})


LIMIT = Usage(8000, 2000, 5, 20, 12, 180000, Decimal("0.25"))
CORRECTION_RESERVE = Usage(input_tokens=1500, output_tokens=350)
PATHS = {"INITIAL_DIRECT": (9, 4, 2), "INITIAL_REVIEWED": (11, 4, 2),
         "FINANCIAL_CORRECTION_DIRECT": (7, 4, 1),
         "FINANCIAL_CORRECTION_REVIEWED": (9, 4, 1), "PENDING_REVIEW_RESUME": (2, 0, 0)}


@dataclass(frozen=True)
class Ledger:
    review_id: str
    committed: Usage = Usage()
    reservations: dict[str, Usage] = field(default_factory=dict)
    completed: dict[str, Usage] = field(default_factory=dict)
    unknown: frozenset[str] = frozenset()
    correction_used: bool = False

    def __post_init__(self):
        if type(self.review_id) is not str or not self.review_id.strip() or set(self.reservations) & set(self.completed):
            raise InputError("INVALID_LEDGER_IDENTITY")
        if not self.unknown <= self.reservations.keys():
            raise InputError("INVALID_UNKNOWN_RESERVATION")
        if type(self.correction_used) is not bool:
            raise InputError("INVALID_CORRECTION_STATE")
        completed_total = Usage()
        for usage in self.completed.values():
            completed_total = completed_total + usage
        if not completed_total.within(self.committed):
            raise InputError("COMPLETED_USAGE_EXCEEDS_COMMITTED")
        if not self.total.within(LIMIT):
            raise BudgetExceeded("BUDGET_EXHAUSTED")

    @property
    def total(self) -> Usage:
        result = self.committed
        for value in self.reservations.values():
            result = result + value
        return result

    def reserve(self, request_id: str, usage: Usage, *, purpose: str = "ORDINARY") -> "Ledger":
        if purpose not in ("ORDINARY", "OPTIONAL_REPAIR", "SYNTHESIS_CORRECTION"):
            raise InputError("UNKNOWN_RESERVATION_PURPOSE")
        if request_id in self.reservations:
            if self.reservations[request_id] != usage:
                raise InputError("RESERVATION_CONFLICT")
            return self
        if request_id in self.completed:
            raise InputError("REQUEST_ALREADY_COMPLETED")
        proposed = self.total + usage
        if purpose == "OPTIONAL_REPAIR" and not self.correction_used:
            proposed = proposed + CORRECTION_RESERVE
        if not proposed.within(LIMIT):
            raise BudgetExceeded("BUDGET_EXHAUSTED")
        if purpose == "SYNTHESIS_CORRECTION" and self.correction_used:
            raise BudgetExceeded("PROTECTED_CORRECTION_ALREADY_USED")
        return replace(self, reservations={**self.reservations, request_id: usage},
                       correction_used=self.correction_used or purpose == "SYNTHESIS_CORRECTION")

    def mark_unknown(self, request_id: str) -> "Ledger":
        if request_id not in self.reservations:
            raise InputError("RESERVATION_NOT_FOUND")
        return replace(self, unknown=self.unknown | {request_id})

    def settle(self, request_id: str, actual: Usage, *, reconciled: bool = False) -> "Ledger":
        if request_id in self.completed:
            if self.completed[request_id] != actual:
                raise InputError("USAGE_RECONCILIATION_CONFLICT")
            return self
        maximum = self.reservations.get(request_id)
        if maximum is None:
            raise InputError("RESERVATION_NOT_FOUND")
        if request_id in self.unknown and not reconciled:
            raise InputError("EXPLICIT_RECONCILIATION_REQUIRED")
        if not actual.within(maximum):
            raise BudgetExceeded("USAGE_EXCEEDS_RESERVED_PROFILE")
        return replace(self, committed=self.committed + actual,
                       reservations={key: value for key, value in self.reservations.items() if key != request_id},
                       completed={**self.completed, request_id: actual}, unknown=self.unknown - {request_id})

    def require_path(self, path: str, *, fixture: bool = False) -> Usage:
        if path not in PATHS:
            raise InputError("UNKNOWN_COMPLETION_PATH")
        nodes, tools, attempts = PATHS[path]
        estimate = Usage(nodes=nodes, tools=tools, attempts=0 if fixture else attempts)
        if not (self.total + estimate).within(LIMIT):
            raise BudgetExceeded("BUDGET_EXHAUSTED")
        # This is a count feasibility check, not token/cost/output fit proof.
        return estimate

    def operation_timeout_ms(self) -> int:
        remaining = LIMIT.active_ms - self.total.active_ms
        if remaining <= 0:
            raise BudgetExceeded("ACTIVE_TIME_EXHAUSTED")
        return min(45000, remaining)

    def to_dict(self) -> dict:
        return {"review_id": self.review_id, "committed": self.committed.to_dict(),
                "reservations": {key: value.to_dict() for key, value in self.reservations.items()},
                "completed": {key: value.to_dict() for key, value in self.completed.items()},
                "unknown": sorted(self.unknown), "correction_used": self.correction_used}

    @classmethod
    def from_dict(cls, data: dict) -> "Ledger":
        if set(data) != set(cls.__dataclass_fields__) or type(data["correction_used"]) is not bool:
            raise InputError("INVALID_LEDGER_SCHEMA")
        return cls(data["review_id"], Usage.from_dict(data["committed"]),
                   {key: Usage.from_dict(value) for key, value in data["reservations"].items()},
                   {key: Usage.from_dict(value) for key, value in data["completed"].items()},
                   frozenset(data["unknown"]), data["correction_used"])
