import sys
import os
import pandas as pd
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

import statsmodels.formula.api as smf

#cleanup import statements to remove unusued imports
#making a stats function that can collect stats for the subsetted dense matrices"
#repeat of stats program above but explicitly writing out 1/mean and covar2 to help with linear regression for now

def GetTheseStats2(df, outputDIR, outName):
	StatsForOneMatrix =pandas.DataFrame(index=df.index)
	StatsForOneMatrix["mean"]=df.mean(axis=1)
	StatsForOneMatrix["INVmean"]=(1/StatsForOneMatrix["mean"])
	StatsForOneMatrix["median"] = df.median(axis=1)
	StatsForOneMatrix["var"]=df.var(axis=1)
	StatsForOneMatrix["covar"]=df.std(axis=1)/df.mean(axis=1)
	StatsForOneMatrix["covar2"]=(StatsForOneMatrix["covar"]*StatsForOneMatrix["covar"])
	StatsForOneMatrix["totalreadsinallcells"]=df.sum(axis=1)
	StatsForOneMatrix["cellswithreads"]= df.astype(bool).sum(axis=1)
	StatsForOneMatrix["logmean"]=np.log(StatsForOneMatrix["mean"])
	StatsForOneMatrix["LOGcovar2"]=np.log(StatsForOneMatrix["covar2"])
	with pd.option_context('mode.use_inf_as_na', True):
		StatsForOneMatrix.fillna(0, inplace=True)
	
	StatsForOneMatrix['gene']=StatsForOneMatrix.index
#trying adding in a few columns for linear regression of cv2 vs mean plots. can separate these later if preferred
	model = smf.ols('covar2 ~ INVmean', data=StatsForOneMatrix)
	model = model.fit()
	StatsForOneMatrix['predictedCovar2'] = model.predict(StatsForOneMatrix['INVmean'])
	StatsForOneMatrix['LOGpredictedCovar2']=np.log(StatsForOneMatrix['predictedCovar2'])
	StatsForOneMatrix['Covar2_linDiffFromPredicted']=(StatsForOneMatrix['predictedCovar2']-StatsForOneMatrix["covar2"]).abs()
	
	StatsForOneMatrix.to_pickle(outputDIR+outName)


if __name__=="__main__":
#       try :
	print(argv)
	root1= argv[1]
	indir=argv[2]
	
	outdir=indir+'StatsMatrices/'
	
	file1=indir+root1
	df1 = pd.read_pickle(file1)
	
	name1=root1[:-4]+'Stats.pkl'

	Stats=GetTheseStats2(df1, outdir, name1)



###note:to run this, need to activate virtualenvironment for jupyter notebook by typing:
###module load python/3.6.3
###then to run command type python3 Sparse2DenseMatrix.py <rootname>




