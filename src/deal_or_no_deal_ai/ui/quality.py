"""Read-only saved RAGAS reports; no evaluator imports or inference on refresh."""
import json
from pathlib import Path
from ..answer_evaluation import report_digest


def render(st, root, scope):
    st.subheader("Answer quality evaluation")
    directory = Path(root)/"var/evaluations"
    reports = []
    for path in sorted(directory.glob("answer-quality-*.json"))[:100] if directory.exists() else []:
        if not path.resolve().is_relative_to(directory.resolve()) or path.stat().st_size > 262144:
            continue
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
            if report["sample"]["scope"] != scope or report["digest"] != report_digest({k:v for k,v in report.items() if k != "digest"}):
                continue
            reports.append(report)
        except (ValueError, KeyError, OSError):
            continue
    if not reports:
        st.info("No answer-quality evaluation has been recorded for this review. Retrieval ID scores do not establish answer accuracy.")
        st.caption("Evaluation is a separate explicit developer action. Refreshing this page makes no model or embedding calls.")
        return
    for report in sorted(reports,key=lambda r:r["evaluated_at_utc"],reverse=True):
        result = report["result"]
        with st.expander("RAGAS · "+result["status"]+" · "+report["evaluated_at_utc"],expanded=True):
            st.caption("Subject: "+("Live AI response" if report["sample"]["application_mode"] == "LIVE" else "Saved example response")+" · Original synthesis · Diagnostic evaluation, not credit authority")
            readiness=result["independent_checks"].get("approval_readiness")
            proposed=report["sample"]["response_fields"].get("panel_decision.decision")
            if proposed in ("Approve","Conditional Approve") and readiness != "Ready for Human Decision":
                st.warning("Independent control concern: the original AI proposed "+proposed+" while readiness was "+str(readiness)+". High judge scores do not clear this concern; human adjudication is required.")
            st.dataframe([dict(Metric=name.replace("_"," ").title(),Status=row["status"],Score=row.get("value"),Scale=row.get("scale"),Reason=row.get("reason","")) for name,row in result["native"].items()],hide_index=True)
            custom = (result.get("custom_rubric") or {}).get("dimensions",{})
            for name,row in custom.items():
                st.write("**"+name.replace("_"," ").title()+":** "+str(row["score"])+"/5 · "+row["status"])
                st.write(row["explanation"])
                for example in row["examples"]:
                    st.write(example["observation"])
                    if example["response_excerpt"]: st.text("Response: "+example["response_excerpt"])
                    if example["evidence_excerpt"]: st.text("Evidence: "+example["evidence_excerpt"])
            st.caption("Recorded paid requests: "+str(result.get("paid_requests","Not recorded"))+" · Cost USD"+str(result.get("cost_at_verified_rates_usd","Not recorded")))
            st.write(" ".join(result["limitations"]))
            st.download_button("Download evaluation report",json.dumps(report,indent=2,ensure_ascii=False),file_name="answer-quality-report.json",mime="application/json",key="quality:"+report["evaluation_id"])
