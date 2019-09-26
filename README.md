# subsampling-scRNAseq-data
the point of this repository is to encapsulate the tools I'm making/developing for subsampling data from 10X scRNA-seq to allow fair comparisons
between samples. The goal of the subsampling is to be able to input my full dense hdf5 data, and output dense matrices of data for my
four samples. However, after subsampling I should end up with four matrices that have the same number of cells each, and each of those cells
should have the same number of reads each. Importantly, the cells and reads that were removed need to be randomly chosen.

I then made scripts to collect statistics on the subsampled or unstampled dense matrices to help with my analysis.
