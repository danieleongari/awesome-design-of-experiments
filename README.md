# Awesome Design of Experiments (DOE) [![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome)

## pyDOE - [GitHub](https://github.com/clicumu/pyDOE2), [Docs](https://pythonhosted.org/pyDOE/)

Fork called `pyDOE2`, which is just adding the GSD method (i.e., a 3+levels fractional factorial) to `pyDOE`.

- Factorial Designs
    - General Full-Factorial (``fullfact``)
    - 2-level Full-Factorial (``ff2n``)
    - 2-level Fractional Factorial (``fracfact``)
    - Plackett-Burman (``pbdesign``)
    - Generalized Subset Designs (``gsd``)
- Response-Surface Designs 
    - Box-Behnken (``bbdesign``)
    - Central-Composite (``ccdesign``)
- Randomized Designs
    - Latin-Hypercube (``lhs``)

## DOEPY - [GitHub](https://github.com/tirthajyoti/doepy), [Docs](https://doepy.readthedocs.io/en/latest/)

* Full factorial: `build.full_fact()`
* 2-level fractional factorial: `build.frac_fact_res()`
* Plackett-Burman: `build.plackett_burman()`
* Sukharev grid: `build.sukharev()`
* Box-Behnken: ``build.box_behnken()``
* Box-Wilson (Central-composite) 
  * with center-faced option: ``build.central_composite()`` with ``face='ccf'`` option
  * with center-inscribed option: ``build.central_composite()`` with ``face='cci'`` option
  * with center-circumscribed option: ``build.central_composite()`` with ``face='ccc'`` option
* Latin hypercube (simple): ``build.lhs()``
* Latin hypercube (space-filling): ``build.space_filling_lhs()``
* Random k-means cluster: ``build.random_k_means()``
* Maximin reconstruction: ``build.maximin()``
* Halton sequence based: ``build.halton()``
* Uniform random matrix: ``build.uniform_random()``

## dexpy - [GitHub](https://github.com/statease/dexpy), [Docs](https://statease.github.io/dexpy/)

- Fractional Factorial: `build_factorial(factor_count, run_count)`
- Full Factorial: `build_full_factorial(factor_count)`
- Central Composite: `build_ccd(factor_count, alpha='rotatable', center_points=1)`
- Mixture Simplex Lattice: `build_simplex_lattice(factor_count, model_order=<ModelOrder.quadratic: 2>)`
- Mixture Simplex Centroid: `build_simplex_centroid(factor_count)`
- Optimal Designs: `build_optimal(factor_count, **kwargs)`

Analysis of the design:
- Statistical Power: `f_power(model, design, effect_size, alpha)`
- Alias list: `alias_list(model, design)`

## diversipy - [GitHub](https://github.com/DavidWalz/diversipy), [Docs](https://diversipy.readthedocs.io/en/latest/index.html) 

- `cube` - Uniform sampling from the unit hypercube
  - `cube.stratify_conventional`: stratification of the unit hypercube
  - `stratify_generalized`: generalized stratification of the unit hypercube
  - `cube.latin_design`: generate a random latin hypercube design matrix
  - `cube.improved_latin_design`: generate an ‘improved’ latin hypercube design matrix
  - `cube.rank1_design`: design matrix for a rank-1 lattice
  - `cube.sample_halton`: generate a Halton point set
  - `cube.sample_maximin`: maximize the minimal distance in the unit hypercube with extensions
  - `cube.sample_k_means`: in its default setup, this algorithm converges to a centroidal Voronoi tesselation of the unit hypercube
  - `cube.grid`: create conventional grid in the unit hypercube
- `simplex` - Uniform sampling on the unit simplex
- `polytope` - Uniform sampling from convex polytopes
- `subset` - Select diverse subsets
  - `subset.psa_partition`: partition the data set into the given number of clusters with the part-and-select algorithm
  - `subset.psa_select`: select representatives points with the part-and-select algorithm
  - `subset.select_greedy_maximin`: greedily select a subset according to maximin criterion
  - `subset.select_greedy_maxisum`: greedily select a subset according to maxisum criterion.

Analysis of the design:

- `indicator.solow_polasky_diversity`: Solow-Polasky diversity
- `indicator.weitzman_diversity`: Weitzman diversity
- `indicator.sum_of_dists`: square root of the sum of all pairwise distances
- `indicator.average_inverse_dist`: average inverse distance
- `indicator.separation_dist`: minimal pairwise distance
- `indicator.wmh_index`: quality index of Wahl, Mercadier, and Helbert
- `indicator.sum_of_nn_dists`: sum of nearest-neighbor distances
- `indicator.unanchored_L2_discrepancy`: unanchored L2 discrepancy

## Definitive Screening Design - [GitHub](https://github.com/danieleongari/definitive_screening_design)
- `dsd.generate(n_num, n_cat, factors_dict=None, method='dsd', min_13=True, n_fake_factors=0)`

Analysis of the design:
- `dsd.analysis.get_map_of_correlations(X, effects)`

## pyLHD - [GitHub](https://github.com/toledo60/pyLHD), [Docs](https://toledo60.github.io/pyLHD/), [WebApp](https://share.streamlit.io/toledo60/pylhd-streamlit/main/pyLHD_streamlit.py)
Generate several variants of the Latin Hypercube design.

Analysis of the design:

Average Absolute Correlation, Maximum Absolute Correlation, Maximum Projection Criterion ([Joseph 2015](https://academic.oup.com/biomet/article-abstract/102/2/371/246859?redirectedFrom=fulltext)), Coverage measure, Inter-site Distance, Discrepancy, MaxiMin, Mesh Ratio, Phi_p Criterion. 

## BoFire - [GitHub](https://github.com/experimental-design/bofire), [Docs](https://experimental-design.github.io/bofire/)
- D-, A-, G-, E-, K- optimality in a constrained design space
- Space filling in a constrained design space

Analysis of the design:

- `bofire.utils.doe.get_confounding_matrix()`


