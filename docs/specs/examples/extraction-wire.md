# Extraction wire contract and illustrative payload

Version: 1.3
Status: DOCUMENT_REVIEW / ILLUSTRATIVE; no executable schema, fixture package or model request
Authority: [SPEC-002](../extraction.md), [CONTRACT-1.0](../overview.md)

## Field registry and strict validation

DealTermsWire has exactly terms, financial_inputs and conflicts. Every listed term/financial key is required. Every WireFact has exactly value, refs and basis_id. No Boolean-to-number, string-to-integer or unknown-key coercion. A present finite money/financial value is a canonical Decimal string. term_months is a strict positive integer. Dates use valid ISO YYYY-MM-DD. Other scalar terms are strings.

The thirteen terms are borrower, legal_entity, facility_type, requested_amount, currency, term_months, maturity_date, interest_terms, repayment_structure, collateral, guarantees, covenants and use_of_proceeds. collateral, guarantees and covenants are lists of strings; Python maps each item to a domain Fact using that field's references. An empty list means explicitly documented none, with evidence; absent is null with empty refs. requested_amount must be positive; facility_type TERM_LOAN and currency USD are the supported scope.

The eighteen financial keys are shown below. Units are USD; each known financial value requires a valid supplied assessment-basis ID. All financial values, including explicit zero and supported negatives, stay Decimal strings. Inapplicable term bases can be null.

InterestTerms has exactly kind (FIXED/FLOATING), annual_rate_percent, index, spread_bps, reset_frequency and floor_percent. Numeric members are finite Decimal strings or null; other members are string or null. Preserve supported clauses; do not fill omitted rate details with zero or calculate future rates. Missing essential rate details remain an explicit validation issue.

A missing field has value=null, refs=[] and basis_id=null. A conflicting field uses that same null representation plus a conflicts entry with exactly field_name and candidates (at least two evidence-backed WireFacts of the field's type). Python derives CONFLICT rather than MISSING for those fields. No automatic precedence. Every known candidate/value needs nonempty valid refs; a null value with ordinary evidence refs is not an accepted known fact.

Python maps refs to scoped source/version/page/passage and basis IDs to unit, period/as-of and assessment basis. Under CANON-1.0 the registry uses exact logical identities independent of incidental UUIDs; COVERAGE-1.0 expands a cross-page handle to every contributing original location, including table context/footnotes. raw_text is the first referenced verbatim passage for display; all refs remain and the display selection confers no authority. Python adds trusted deal/run/revision/schema metadata. Ref resolution alone does not prove semantic support. The existing three-root wire below is unchanged.

SME fixes preserve this wire unchanged: subject/facility metadata and FACT-SUPPORT-1.0 are application-side records, not additional provider keys. Reported/adjusted EBITDA normalization and automated reconciliation are explicitly deferred; original source text remains available. Do not add reported_ebitda, factor ratings or condition-management fields to this strict payload without a separately revised contract. A hydrated KNOWN value is not HUMAN_SUPPORTED. This illustrative payload is not a registered complete case pack or a Live semantic-support result.

INPUT-EDU-1.0 in the overview supplies the shared strict JSON/technical-size/numeric limits before this wire's field validation. Reject duplicate keys at any level before parsing into a normal dictionary; apply financial bounds after exact source-unit normalization. The JSON below remains unchanged and within those illustrative limits; this is not an executable schema or proof of provider/token compatibility.

## Illustrative source registry

This is a contract illustration, separate from the complete E-N01 runtime fixture. No PDF pages have been authored or parsed. Future pages must actually contain the mapped excerpts; invented locators fail validation.

- P1, illustrative document DEMO-1 v1 page1: “Example Equipment LLC requests a USD1,200,000 term loan for 48 months, fixed annual rate 6%. Principal and interest follow the supplied annual schedule. First-ranking equipment security; no guarantees; annual financial statements required.” Maturity date is not stated.
- P2, page2: “Documented projected assessment year FY-ASSESS: net income USD700,000; interest expense USD100,000; income tax USD100,000; depreciation USD100,000; amortization USD100,000; cash available for debt service USD900,000; principal payments USD500,000 and interest payments USD100,000, including the proposed facility; revenue USD4,400,000. Comparable prior annual revenue FY-PREV USD4,000,000. At transaction basis TXN-1: existing funded debt USD2,400,000; proposed funding USD1,200,000; debt repaid USD300,000; eligible equipment USD2,000,000; prior liens USD0; secured exposure USD1,200,000; current assets USD1,500,000; current liabilities USD750,000.”
- P3, page3: “Use of proceeds: purchase equipment.”
- P4, page4: “Use of proceeds: working capital.” No approved precedence supplied.
- FY-ASSESS/FY-PREV are documented comparable annual periods; TXN-1 is the documented transaction/balance-sheet basis. No projected values are generated by the application.

## Complete provider-facing JSON example

~~~json
{
  "terms": {
    "borrower": {
      "value": "Example Equipment LLC",
      "refs": [
        "P1"
      ],
      "basis_id": null
    },
    "legal_entity": {
      "value": "Example Equipment LLC",
      "refs": [
        "P1"
      ],
      "basis_id": null
    },
    "facility_type": {
      "value": "TERM_LOAN",
      "refs": [
        "P1"
      ],
      "basis_id": null
    },
    "requested_amount": {
      "value": "1200000",
      "refs": [
        "P1"
      ],
      "basis_id": null
    },
    "currency": {
      "value": "USD",
      "refs": [
        "P1"
      ],
      "basis_id": null
    },
    "term_months": {
      "value": 48,
      "refs": [
        "P1"
      ],
      "basis_id": null
    },
    "maturity_date": {
      "value": null,
      "refs": [],
      "basis_id": null
    },
    "interest_terms": {
      "value": {
        "kind": "FIXED",
        "annual_rate_percent": "6",
        "index": null,
        "spread_bps": null,
        "reset_frequency": null,
        "floor_percent": null
      },
      "refs": [
        "P1"
      ],
      "basis_id": null
    },
    "repayment_structure": {
      "value": "Principal and interest per documented annual schedule",
      "refs": [
        "P1"
      ],
      "basis_id": null
    },
    "collateral": {
      "value": [
        "First-ranking equipment security"
      ],
      "refs": [
        "P1"
      ],
      "basis_id": null
    },
    "guarantees": {
      "value": [],
      "refs": [
        "P1"
      ],
      "basis_id": null
    },
    "covenants": {
      "value": [
        "Annual financial statements"
      ],
      "refs": [
        "P1"
      ],
      "basis_id": null
    },
    "use_of_proceeds": {
      "value": null,
      "refs": [],
      "basis_id": null
    }
  },
  "financial_inputs": {
    "net_income": {
      "value": "700000",
      "refs": [
        "P2"
      ],
      "basis_id": "FY-ASSESS"
    },
    "interest_expense": {
      "value": "100000",
      "refs": [
        "P2"
      ],
      "basis_id": "FY-ASSESS"
    },
    "income_tax_expense": {
      "value": "100000",
      "refs": [
        "P2"
      ],
      "basis_id": "FY-ASSESS"
    },
    "depreciation": {
      "value": "100000",
      "refs": [
        "P2"
      ],
      "basis_id": "FY-ASSESS"
    },
    "amortization": {
      "value": "100000",
      "refs": [
        "P2"
      ],
      "basis_id": "FY-ASSESS"
    },
    "cash_available_for_debt_service": {
      "value": "900000",
      "refs": [
        "P2"
      ],
      "basis_id": "FY-ASSESS"
    },
    "annual_principal_payments": {
      "value": "500000",
      "refs": [
        "P2"
      ],
      "basis_id": "FY-ASSESS"
    },
    "annual_interest_payments": {
      "value": "100000",
      "refs": [
        "P2"
      ],
      "basis_id": "FY-ASSESS"
    },
    "existing_funded_debt": {
      "value": "2400000",
      "refs": [
        "P2"
      ],
      "basis_id": "TXN-1"
    },
    "proposed_funded_borrowing": {
      "value": "1200000",
      "refs": [
        "P2"
      ],
      "basis_id": "TXN-1"
    },
    "transaction_debt_repaid": {
      "value": "300000",
      "refs": [
        "P2"
      ],
      "basis_id": "TXN-1"
    },
    "eligible_equipment_value": {
      "value": "2000000",
      "refs": [
        "P2"
      ],
      "basis_id": "TXN-1"
    },
    "prior_ranking_liens": {
      "value": "0",
      "refs": [
        "P2"
      ],
      "basis_id": "TXN-1"
    },
    "secured_facility_exposure": {
      "value": "1200000",
      "refs": [
        "P2"
      ],
      "basis_id": "TXN-1"
    },
    "current_revenue": {
      "value": "4400000",
      "refs": [
        "P2"
      ],
      "basis_id": "FY-ASSESS"
    },
    "previous_revenue": {
      "value": "4000000",
      "refs": [
        "P2"
      ],
      "basis_id": "FY-PREV"
    },
    "current_assets": {
      "value": "1500000",
      "refs": [
        "P2"
      ],
      "basis_id": "TXN-1"
    },
    "current_liabilities": {
      "value": "750000",
      "refs": [
        "P2"
      ],
      "basis_id": "TXN-1"
    }
  },
  "conflicts": [
    {
      "field_name": "terms.use_of_proceeds",
      "candidates": [
        {
          "value": "Purchase equipment",
          "refs": [
            "P3"
          ],
          "basis_id": null
        },
        {
          "value": "Working capital",
          "refs": [
            "P4"
          ],
          "basis_id": null
        }
      ]
    }
  ]
}
~~~

Expected domain result: PARTIAL, maturity_date MISSING, use_of_proceeds CONFLICT, term_months integer48, all financial values typed Decimal with the listed bases. Neither conflict resolution nor a completed PanelDecision is implied. Domain missing_fields excludes fields already classified CONFLICT. Invalid types/bases are quarantined with explicit validation issues; they are never silently promoted.

The compact wire avoids repeating raw text and trusted metadata. The 1,000-output-token Extractor allocation remains a proposed feasibility target; measure the entire schema/output with the selected model before enabling Live. If it cannot fit faithfully, reallocate within approved cumulative limits while preserving correction reserve, or mark Live unavailable. Do not truncate fields/evidence to manufacture a pass.
