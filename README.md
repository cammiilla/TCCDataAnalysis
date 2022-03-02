# TCC_Data_Analysis

This is the code repository with all the analisys developed for the monograph named "Quasar classification using the t-SNE algorithm". The sequence of the files is:

step1_data_match.py - does a match with DES data and SLOAN data and results are divided into two samples.

step2_tsne_analysis.ipynb - is where the tsne reduction occur, and it is separete by perplexity and number of iteration variation.

step3_tsne_analysis_visualization.ipynb - with all the reduction, here is the grafich visualisation.

step4_test_sample_analysis.py - here is where the best tsne distribution is applied to the test sample using the K Dimensional Tree (KD Tree) algorithm.

step5_data_classification.ipynb - here is where the data is classified in quasars and others. 

step6_data_visualization.ipynb - this is where the results of the classification are displayed graphically.


THE ABSTRACT

CARDOSO, C. O. Quasar classification using the t-SNE algorithm. 2021. 68p.
Monograph (Conclusion Course Paper) - Escola de Engenharia de Lorena, Universidade
de São Paulo, Lorena, 2021.

The present work presents a separation of quasars from other objects using the t-distributed
Stochastic Neighbor Embedding (t-SNE) method. The t-SNE is a dimensional reduction
algorithm, for a set of points in high dimension where we try to preserve its original
distribution. Among the t-SNE parameters that can influence the final distribution of
points, the perplexity and the number of iterations were varied in order to obtain a
good result. The sample group was separated into a training and a test set, and they
comprise objects present in the Dark Energy Survey Data Release 2 (DES DR2) that
have a correspondence in the spectroscopic survey of the Sloan Digital Sky Surveys Data
Release 16 (SDSS DR16), where the classification contained in the SDSS DR16 was used
to identify the objects in: quasar, star or galaxy. The t-SNE algorithm was run for the
training sample, with the following dimensions to be reduced: magnitudes, colors and
morphological classifications of objects. Nine different reductions were performed, varying
the perplexity and number of iterations parameters. The best reduction obtained was
with perplexity equal to 100 and number of iterations equal to 5000, being possible to
obtain a cut that contained 70.18% of the quasars in relation to the total number of
quasars in the sample. To test the effectiveness of this distribution, the test sample was
submitted to the algorithm K Dimensional Tree (KD Tree), which identifies which is the
closest neighbor point of a given point in high dimensionality. The KD Tree was used
to identify in each object of the test sample the two closest neighbors contained in the
training sample, and thus the average of the coordinates of these two training objects in
the plane was performed and this was the respective coordinate in the plane of the test
sample object. The same cut was made for the test sample and resulted in a composition
very similar to that obtained for the training, which contained 76.58% of the quasars in
relation to the total number of quasars in the sample. The objective of making a separation
of quasars in a photometric set of heterogeneous data proved to be achievable using the
t-SNE dimensionality reduction tool. However, it is not possible to affirm a good result
when the model is applied to a less restricted sample set, and the purity of the cut can be
improved by adopting other selection methods.

Keywords: t-distributed Stochastic Neighbor Embedding. Quasars. K Dimensional Tree.
Astronomy.

