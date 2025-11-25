1.data_process.py
Purpose

Pre-process raw growth curves by trimming noisy tails, removing incomplete series, and exporting a cleaned dataset.

Key Steps

Removes NaN values per series.

Requires at least 10 data points per curve.

Computes 5-point moving average and identifies the time window before the maximum local average.

Cuts the curve at max_average_index + 5 to remove unreliable late-phase fluctuations.

Removes curves that cannot be properly trimmed.

Saves the cleaned table as:
Table S1_3880_251125_cleaned.xlsx

Input

Table S1_3880_251125.xlsx (raw growth curves)

Output

Cleaned growth curves with aligned length per sample.

2.calculate_DDTW.py
Purpose

Compute a Derivative Dynamic Time Warping (DDTW) distance matrix for all 3,880 × 3,880 growth curves.

Key Features

Implements custom derivative and derivative-based DTW metric.

Uses a dynamic programming approach for computing DDTW distances.

Removes NaN values before comparison.

Computes pairwise distances for all pairs (i, j) where j > i.

Saves results to Excel matrix:
Table S3. DDTW matrix of 3,880 growth curves.xlsx

Input

Table S1. 3,880 processed growth curves.xlsx (cleaned curves)

Output

A square matrix of DDTW distances (upper-triangular filled).

3.calculate_DTW.py
Purpose

Compute a FastDTW-based distance matrix for all 3,880 growth curves as a computationally efficient alternative to full DTW.

Key Features

Uses the FastDTW algorithm with Euclidean distance.

Removes NaN values and flattens each curve.

Computes distances for pairs (i, j) with j > i to reduce redundant calculations.

Saves the distance matrix to:
230507第三条DTW0-200.xlsx

Input

Table S1. 3,880 processed growth curves.xlsx

Output

FastDTW pairwise distance matrix.


4. clustering_and_calculateSC.py
Purpose

Perform hierarchical clustering on growth-curve distance matrices (DTW and DDTW), evaluate clustering quality under different mixing ratios, and compute cluster-level enrichment for phenotype categories.

Key Functions

Combine DTW and DDTW matrices using a weighted sum:
combined = (1 – α) * DTW + α * DDTW
for α ∈ {0.0, 0.1, …, 1.0}.

Perform Agglomerative Clustering with:

n_clusters = 2 … 9

linkage: "average"

Compute clustering evaluation metrics:

Silhouette Coefficient (SC)

Adjusted Rand Index (ARI)

Adjusted Mutual Information (AMI)

Calinski–Harabasz Index (CHI)

V-measure

Create Excel files summarizing evaluation metrics across α and cluster numbers.

For each cluster, compute:

Category composition

Category enrichment using hypergeometric test

Export results to cluster-specific Excel sheets.

Input

Table S2. DTW matrix of 3,880 growth curves.xlsx

Table S3. DDTW matrix of 3,880 growth curves.xlsx

LABEL.xlsx (true labels)

LABEL_TYPE.xlsx (category of each curve)

Output

SC.xls — Silhouette, ARI, AMI, CHI, V-measure for each α and cluster number

genecategory_enrich.xls — Summary of category enrichment across clusters

Individual files:
230418 M63 {α} genename{n} enrich.xls (detailed cluster membership and enrichment)

5. calculate DTW and DDTW between same experiment and select top 25%.py
Purpose

Identify highly similar growth curves originating from the same experiment, and select the top-quality replicates using derivative-based DTW (DDTW).

This script processes the full set of 10,247 growth curves.

Key Steps

Group growth curves by experiment
Based on the prefix before the first “.” in column names.

Compute pairwise distances within each experiment
For all pairs (i, j) within an experiment:

Compute derivative DTW distance using a custom implementation (__dtw + derivative metric).

Save all distances to:
DDTW distances of growth curves between experimental replicates.xlsx

Select the top 25% most similar replicates

Pairs with DDTW distance < 0.00053357 are considered highly similar.

All unique curves appearing in these pairs are retained.

Export filtered dataset
Combine all selected high-quality replicates into:
selected_seriesby_DDTW_25percentage.xlsx

Input

Table S7. 10,247 growth curves.xlsx

Output

DDTW distances of growth curves between experimental replicates.xlsx
(pairwise replicate distances)

selected_seriesby_DDTW_25percentage.xlsx
(subset of high-quality replicate curves)
