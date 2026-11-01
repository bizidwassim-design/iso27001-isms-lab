# Contributing

Contributions that make the lab more realistic or more useful for teaching are welcome:

* **Better worked examples**: a sharper risk statement, a more realistic audit finding, a clearer management review decision.
* **New checks** in `scripts/validate_isms.py` that catch a real ISMS consistency mistake.
* **Translations** of the context, audit and review documents (add a language suffix: `isms-scope.fr.md`).
* **Corrections** to clause or control references.

## Ground rules

1. **Original wording only.** Reference ISO/IEC 27001:2022 by clause number and Annex A control ID with its short
   title. Never paste text from the standard, from other toolkits or from vendors. The same applies to laws and
   regulations: summarise obligations in your own words.
2. **Fictional data only.** Keep to Northwind Logistics FZ-LLC and the fictional suppliers (Contoso, Fabrikam). No
   real people, clients, domains, IP addresses, tenant IDs or secrets.
3. **Keep the ISMS coherent.** A new risk needs an owner, assets, Annex A controls and, unless retained, a treatment
   action. A new finding needs evidence references. A new corrective action must point at a finding.
4. **Never edit generated files by hand.** Change `data/*.csv`, then run the build. Generated files: everything in
   `02-risk/` except `risk-methodology.md`, everything in `03-soa/`, and `05-review/isms-metrics-pack.md`.

## Before you open a pull request

```bash
pip install openpyxl
python scripts/build_isms.py
python scripts/validate_isms.py
python -m unittest discover -s tests -v
git status   # commit the regenerated files together with your data change
```

CI runs the same commands and fails if a generated file is out of date or a cross-reference is broken.

## Process

Open an issue to discuss anything larger than a typo fix, then a pull request describing what changed and why.
By contributing you agree your work is released under the [MIT License](LICENSE) and you accept the
[Code of Conduct](CODE_OF_CONDUCT.md).
