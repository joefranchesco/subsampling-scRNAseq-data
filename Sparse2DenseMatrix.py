import sys
import os
import pandas
import numpy as np

from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt
sys.path.append(os.path.abspath("/Users/joca4543/.local/lib/python3.6/site-packages/"))
sys.path.append(os.path.abspath("/Users/joca4543/.local/jhub_venv/lib/python3.6/site-packages/"))
sys.path.append(os.path.abspath("/Users/joca4543/scanpy"))
sys.path.append(os.path.abspath("/Users/joca4543/jhub_venv/lib/python3.6/site-packages/"))
import scanpy.api as sc

from sys import argv
sys.setrecursionlimit(10000)

#may need rest of scanpy import settings/statements
#cleanup import statements to remove unusued imports



def ConvertToDense(inputdirectory,outNAME,savedirectory):
	matrix = sc.read_10x_mtx(inputdirectory, var_names='gene_symbols', cache=True)
	matrix.var_names_make_unique()
	statcounts = pandas.DataFrame(matrix.X.todense())
	genenames = matrix.var_names.to_series()
	cellnames = matrix.obs_names.to_series()
	statcounts.columns = genenames
	statcounts.index = cellnames
	statcounts = statcounts.T
  #transpose the matrix so that cells are now the columns and genes are now the rows
###	statcounts.to_csv(outNAME, sep='\t', header=None, index=False)
	statcounts.to_pickle(savedirectory+outNAME)
###	return statscounts
###should I both return the file and save it?




if __name__=="__main__":
#       try :
	print(argv)
	indir1 = argv[1]
	outputname=argv[2]
	savedirect=argv[3]
	DenseMatrix=ConvertToDense(indir1, outputname, savedirect)

#                outNormalizedFile = inputCSVfileA[:-4]+"normalizedToLastKBgene.csv"
#                outWindowedFile = inputCSVfileA[:-4]+"Windowed.csv"
#                outClusterredFile = inputCSVfileA[:-4]+"Clusterred.csv"



###note:to run this, need to activate virtualenvironment for jupyter notebook by typing:
###module load python/3.6.3
###then to run command type python3 Sparse2DenseMatrix.py <rootname>




