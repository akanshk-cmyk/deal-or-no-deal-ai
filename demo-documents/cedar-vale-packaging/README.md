# Cedar Vale Packaging LLC — new fictional upload package

Upload only these three PDFs together for one deal:

1. 01-loan-agreement.pdf
2. 02-financial-projections.pdf
3. 03-collateral-evidence.pdf

Three pages total; 6,150 bytes. Each file was parsed successfully by the existing
upload_parser worker and independently read with pypdf strict mode. Borrower text
is present on every page. This borrower was absent from the local application
records when the package was created. No runtime registration, upload, model call,
human review or decision was performed during preparation.

## Reporting context to check

- Borrower: Cedar Vale Packaging LLC.
- Current annual projection: 2027-01-01 through 2027-12-31.
- Comparative annual projection: 2026-01-01 through 2026-12-31.
- Balance-sheet/transaction date: 2026-10-25.
- USD whole units; standalone borrower; facility CVP-DEMO-01.
- Review date: choose the intended review date; an upload-date default is not a
  source-stated review date.
- Sample equipment-policy applicability: review whether Yes is appropriate to
  this stated equipment loan. KYC/sanctions applicability is not established.

## Independent expected arithmetic — not AI results

| Calculation | Expected value |
|---|---|
| Requested amount | USD960,000 |
| Term | 36 months |
| EBIT | 480,000 + 60,000 + 100,000 = USD640,000 |
| EBITDA | 640,000 + 120,000 + 40,000 = USD800,000 |
| Funded debt | 1,640,000 + 960,000 - 200,000 = USD2,400,000 |
| Annual DSCR | 540,000 / (300,000 + 60,000) = 1.50x |
| Debt / EBITDA | 3.00x |
| Equipment LTV, if applicable | (960,000 + 0) / 1,600,000 = 60% |
| Projected revenue growth | (3,300,000 - 3,000,000) / 3,000,000 = 10% |
| Current ratio | 900,000 / 450,000 = 2.00x |
| EBIT / interest expense | 640,000 / 60,000 = 10.666..., displayed 10.67x |

No authored borrower factor ratings, bureau reports or KYC/sanctions evidence are
supplied. Expect no composite risk score until a supported scoring path exists;
do not inherit the registered Standard Deal's Low rating. The annual-statements
covenant has no stated delivery deadline and needs evaluation, not an invented
due date or automatic breach. Readiness may be Additional Information Required
because risk evidence is absent; Pending Review is not guaranteed. Do not force
an approval outcome merely because DSCR and LTV look favorable.

These are fictional source assumptions, not audited statements, verified
collateral, real lending policy, statistical credit ratings or investment advice.
Do not upload this README or manifest.json as deal PDFs. Keep the manifest for
source hashes and demonstration evidence.
