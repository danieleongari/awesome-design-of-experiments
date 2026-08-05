# Learning Design of Experiments through published case studies

These eleven notebooks turn openly accessible scientific papers into executable Design of Experiments (DoE) case studies. They are written for practitioners who want to understand **why a design was chosen, what it can estimate, how the analysis works, and where its conclusions can fail**—not merely recover a reported optimum.

## Why this belongs in Awesome DoE

Awesome DoE maps the open-source tools available for generating designs, diagnosing their statistical properties, analysing responses, and augmenting experiments. This notebook collection is its applied companion: the catalogue answers **“which tools exist?”** and these cases answer **“how are they used responsibly in practice?”**

The portfolio deliberately spans response surfaces, screening, robust designs, mixtures, factorial error strata, computer experiments, and DoE/ML hybrids. The notebooks therefore differ scientifically while sharing one reading pattern and one restrained Python stack.

## The same reading structure in every notebook

Practitioners can move between cases without relearning the document layout:

| Section | Question it answers |
|---:|---|
| 0. Reproducibility card | Which paper, access route, licence, evidence level, seed, and limitations apply? |
| 1. Scientific context | What is the experimental unit, response, factor space, and practical question? |
| 2. Data provenance and reproduction boundary | Which rows or aggregate values are available, transcribed, missing, or confidential? |
| 3. Reconstruct the design | How is the nominal design generated, coded, constrained, and matched to the publication? |
| 4. Understand the design | What is estimable, aliased, balanced, replicated, or weakly supported? |
| 5. Reproduce the article analysis | Which published models, tests, surfaces, rankings, or optima can be recalculated? |
| 6. Validate against the paper | How closely do notebook results match explicit publication targets? |
| 7. Go beyond the paper | What additional, clearly labelled teaching analysis reveals the design's behaviour? |
| 8. Practitioner conclusions | What should be trusted, avoided, or changed in a real application? |
| 9. Reproducibility metadata | Which exact versions and random choices produced the saved outputs? |

The evidence vocabulary is also consistent:

- **paper** — a value or conclusion reported by the publication;
- **reproduction** — a notebook calculation from available article data or equations;
- **teaching analysis** — a new diagnostic or synthetic demonstration, never new experimental evidence.

## A deliberately small Python toolchain

All notebooks install from one shared [`requirements.txt`](requirements.txt). The limited stack keeps differences between cases focused on the design and scientific problem:

- **PyDOE (`pydoe`) first** for design generation whenever it represents the published design faithfully;
- **NumPy, pandas, and SciPy** for transparent calculations, data handling, tests, and design metrics;
- **statsmodels** for regression, ANOVA, contrasts, and diagnostics;
- **scikit-learn** only for useful validation or restrained surrogate comparisons;
- **Matplotlib** for explanatory figures.

When PyDOE lacks a paper-specific construction—or would hide its mechanism—a notebook uses a short transparent implementation and validates its consequences. Other DoE frameworks are not added merely for convenience. Section 9 of each notebook preserves the detailed environment used for its saved execution, which may predate the current shared baseline.


## Reproduction levels

Three levels of reproducibility are defined in the opening card of each notebook:

- **Level A — exact:** published rows and responses support direct numerical reproduction.
- **Level B — analytical:** design and analysis are reproducible, with differences caused by rounding, conventions, or undocumented software details.
- **Level C — methodological:** confidential or unavailable data prevent exact refitting, so the method and its consequences are reconstructed transparently.

“Reproduced” therefore does not always mean numerically identical. Each opening card states the boundary, and every validation section explains discrepancies rather than forcing agreement. These notebooks are learning resources, not substitutes for the original articles or for subject-matter review of a new experiment.

## Notebook map

| Notebook | Level | Application or comparison | Main lessons |
|---|:---:|---|---|
| [`kim2022.ipynb`](kim2022.ipynb) | B | PET glycolysis | Box–Behnken design, quadratic surfaces, lack of fit, diagnostics, and confirmation |
| [`fardmasoumi2011.ipynb`](fardmasoumi2011.ipynb) | B | Enzymatic ester synthesis | Taguchi L9 arrays, signal-to-noise ratios, interaction aliasing, and robustness claims |
| [`ding2022.ipynb`](ding2022.ipynb) | B | DHA fermentation | Plackett–Burman screening followed by central-composite optimization |
| [`guedesoliveira2019.ipynb`](guedesoliveira2019.ipynb) | C | Reduced-fat food formulation | Mixture constraints, simplex geometry, Scheffé models, and multi-response trade-offs |
| [`piepho2018.ipynb`](piepho2018.ipynb) | B | Factorial field experiments | Interactions, quantitative trends, error strata, blocking, hierarchy, and lack of fit |
| [`jones2011.ipynb`](jones2011.ipynb) | B | Definitive screening methodology | Three-level construction, second-order effects, aliasing, power, and estimability |
| [`husslage2011.ipynb`](husslage2011.ipynb) | B | Computer experiments | Latin hypercubes, maximin spacing, projections, discrepancy, and surrogate-design quality |
| [`kucherenko2015.ipynb`](kucherenko2015.ipynb) | B | Numerical integration | Monte Carlo, Latin hypercube, and Sobol sampling under equal budgets and effective dimensions |
| [`arboretti2021.ipynb`](arboretti2021.ipynb) | C | Confidential detergent formulation | BBD geometry, D-optimal reduction, nested replication, RSM/ML evidence, and grouped validation |
| [`arboretti2022.ipynb`](arboretti2022.ipynb) | C | DoE and machine-learning simulation | Equal-budget design comparisons, prediction models, noise sensitivity, and nonparametric rankings |
| [`choi2021.ipynb`](choi2021.ipynb) | C | Building-load surrogate design | Fractional factorial versus LHS, curvature estimability, validation geometry, and metric definitions |

## Suggested learning paths

- **Start with a complete response-surface workflow:** `kim2022`, then `ding2022` for screening followed by optimization.
- **Learn specialized experimental geometries:** `fardmasoumi2011` for Taguchi arrays and `guedesoliveira2019` for mixtures.
- **Study estimability and experimental structure:** `piepho2018` for error strata and `jones2011` for definitive screening.
- **Move to computer experiments and predictive modelling:** `husslage2011`, `kucherenko2015`, `arboretti2021`, `arboretti2022`, and `choi2021`.

Within any case, read Sections 1–4 before interpreting model results. Use Section 6 to see what actually matches the article, and treat Section 7 as a lesson about design behaviour rather than an extension of the publication's scientific evidence.

## Running the notebooks

From the repository root, create one environment for the whole collection:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r notebooks/requirements.txt
jupyter lab notebooks/
```

Saved outputs support immediate reading. Rerun a notebook before adapting assumptions, changing a design, or comparing a new response model. `arboretti2022` exposes a practical `balanced` profile by default and a substantially slower `paper_scale` profile for publication-sized simulation budgets.
