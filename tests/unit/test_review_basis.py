"""Scoped TEST-008-02/03/06/07 and TEST-006-05; no full review service."""

from dataclasses import replace

from deal_or_no_deal_ai.context import InputError
from deal_or_no_deal_ai.review import (
    ANALYSIS_FIELDS, Actor, PendingReview, Requirement, accept_review, advance_handling,
    analytical_basis, consume_own_receipt, prepare_review_conditions, support_draft,
)
from tests.support import OfflineTest, uid


class ReviewTests(OfflineTest):
    def setUp(self):
        super().setUp()
        self.basis = analytical_basis({key: key + ":v1" for key in ANALYSIS_FIELDS})
        self.request = PendingReview(uid("pending"), uid("workspace"), uid("deal"),
            uid("thread"), 1, self.basis, 1, "NORMAL",
            (Requirement("DSCR-handling", False, None, 1),))
        self.approver = Actor("AuthorizedApprover", uid("workspace"), frozenset({uid("deal")}), frozenset({"NORMAL"}))
        self.risk = Actor("RiskManager", uid("workspace"), frozenset({uid("deal")}))
        self.compliance = Actor("ComplianceOfficer", uid("workspace"), frozenset({uid("deal")}))

    def handled(self):
        return advance_handling(self.request, Requirement("DSCR-handling", True, "handling:1", 2), expected_gate_version=1)

    def test_specialist_progress_changes_gate_not_analysis(self):
        updated = self.handled()
        self.assertEqual(updated.analytical_basis_digest, self.basis)
        self.assertEqual(updated.gate_version, 2)
        self.assertNotEqual(updated.gate_digest, self.request.gate_digest)
        self.assertEqual(advance_handling(updated, updated.requirements[0], expected_gate_version=2), updated)
        new_basis = analytical_basis({key: key + (":v2" if key == "sources" else ":v1") for key in ANALYSIS_FIELDS})
        self.assertNotEqual(new_basis, self.basis)

    def test_missing_handling_and_stale_or_wrong_actor_cannot_accept(self):
        with self.assertRaisesRegex(InputError, "UNSATISFIED"):
            accept_review(self.request, self.approver, uid("accept"), "Approve", expected_basis=self.basis, expected_gate_version=1)
        for actor, version, basis in ((self.risk, 2, self.basis), (self.approver, 1, self.basis),
                                      (self.approver, 2, "changed")):
            with self.subTest(actor=actor.persona, version=version), self.assertRaises(InputError):
                accept_review(self.handled(), actor, uid("accept"), "Approve", expected_basis=basis, expected_gate_version=version)

    def test_normal_approver_cannot_satisfy_senior_tier(self):
        with self.assertRaisesRegex(InputError, "TIER_REQUIRED"):
            accept_review(replace(self.handled(), required_tier="SENIOR"), self.approver,
                          uid("accept"), "Reject", expected_basis=self.basis, expected_gate_version=2)

    def test_draft_targets_exist_before_support_and_survive_acceptance(self):
        current, draft = prepare_review_conditions(
            self.handled(), self.approver, uid("draft"), ("Obtain required current review.",),
            (("issue:DSCR",),), (frozenset({"FINANCIAL_RISK", "POLICY_CONTROL"}),),
            frozenset({"issue:DSCR"}), expected_basis=self.basis, expected_gate_version=2)
        target = draft.targets[0]
        self.assertTrue(target.target_id)
        with self.assertRaisesRegex(InputError, "UNSATISFIED"):
            accept_review(current, self.approver, uid("accept"), "Conditional Approve",
                          expected_basis=self.basis, expected_gate_version=current.gate_version, draft=draft)
        with self.assertRaisesRegex(InputError, "WRONG_SUPPORT_DOMAIN"):
            support_draft(current, draft, self.approver, target.target_id, "FINANCIAL_RISK",
                          ("issue:DSCR",), "support:fake", expected_gate_version=current.gate_version)
        for actor, domain in ((self.risk, "FINANCIAL_RISK"), (self.compliance, "POLICY_CONTROL")):
            current = support_draft(current, draft, actor, target.target_id, domain,
                ("issue:DSCR",), "support:" + domain, expected_gate_version=current.gate_version)
        accepted = accept_review(current, self.approver, uid("accept"), "Conditional Approve",
            expected_basis=self.basis, expected_gate_version=current.gate_version, draft=draft)
        self.assertEqual(accepted.condition_target_refs, (target.target_id,))
        self.assertEqual(current.analytical_basis_digest, self.basis)

    def test_own_committed_receipt_can_resume_without_self_staleness(self):
        current = self.handled()
        accepted = accept_review(current, self.approver, uid("accept"), "Reject",
            expected_basis=self.basis, expected_gate_version=current.gate_version)
        recorded = replace(current, state="RECORDED", recorded_operation_id=accepted.operation_id)
        self.assertEqual(recorded.gate_digest, current.gate_digest)
        self.assertEqual(consume_own_receipt(recorded, accepted), accepted)
        for altered in (replace(recorded, analytical_basis_digest="changed"),
                        replace(recorded, recorded_operation_id=uid("other")),
                        replace(recorded, gate_version=recorded.gate_version + 1)):
            with self.assertRaises(InputError):
                consume_own_receipt(altered, accepted)
