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

#cleanup import statements to remove unusued imports


#the bellow two functions can help me to subset to a desired read number/cell
#any cells with fewer reads than this number will be tossed
#any cells with that number or more will be pruned down to this number of reads by randomly tossing reads
#can't find a way to seed the np.random.choice function so skipping that for now

def genelist(row,cell):
	return [row["gene"] for i in range(int(row[cell]))]
#think this mini function looks at a gene(row) and one cell within that, and outputs 
#a list of the name of that gene repeated as many times as that gene was detected in that cell


def subsampletoreadnumber(readnumber,dfname):
#drop cells that don't have the min read number
	print ("shape",dfname.shape)
	df = dfname.drop([col for col, val in dfname.sum().iteritems() if val <= readnumber], axis=1)
#here dfname.sum().iteritems() seems to go through and produce a sum of counts for each cell (column)
        #and remove that column(cell) if the cell doesnt have that minimum read number
	print ("shape",df.shape)
	newcols = []
	for i,cell in enumerate(df.columns):
		cellcounts = df[cell].to_frame()
#convert contents from each cell(column) to a new unique dataframe
		sumofcell = cellcounts[cell].sum()
#number of reads in that cell: sum each column
		getridof = int(sumofcell-readnumber)
#calc number of reads we wish to drop for each cell. This is a integer. For instance if minreads is 100 and reads is 110, we need to drop 10 reads.
		cellcounts = cellcounts[cellcounts[cell]!=0]
#remove the rows of each cell column that have no counts
            #this notation is weird because the cellcounts[cell] items are actually genes...
		cellcounts["gene"]=cellcounts.index
#assign each cell's dataframe a second column which is the gene name, currently is an index instead of column
		cellcounts["genes"]=cellcounts.apply(lambda row: genelist(row,cell),axis=1)
            #now we're applying the above gene list function to the cellcounts dataframe (counts of each gene from one cell)
            #this produces a third column of info for each cell that has a list of lists of the names of genes detected
            #repeated as many times as they were detected
		lofgenenames = cellcounts["genes"].tolist()
            #converted the above column of the cellcounts df to its own list (that contains lists of genes)
		longgeneslist = np.array([gene for genelist in lofgenenames for gene in genelist])
            #because it was a list of lists.. this is unpacking it all into a single array
            #ex: before we had a list like: [[ActB, ActB,ActB'][Gene2, Gene2]]
            #needed to unpack it into a single array with one long list of all genes: actb,actb,actb,gene2,gene2 etc
		readstogetridof = pandas.DataFrame(np.random.choice(longgeneslist, replace=False, size=getridof))
            #now, in each of these long genes lists, using the numpy random choice function to randomly choose
            #getridof number of counts, which are represented by repeats of the gene names, to remove
            #made a dataframe of this list of gene names to remove
		countofreadstoremove = readstogetridof[0].value_counts().to_frame()
            #now, we're counting up the repeats of the gene names in this removal list and making a new 
            #counts to remove DF
		m = pandas.concat([cellcounts,countofreadstoremove],axis=1,sort=False)
            #now making a new df m which is composed of the concatenation of
            #that original cellcounts df for each cell concatenated with a new column of data which is the counts
            #of each gene to remove, and aligning on the index, so gene names match up
		m.fillna(0,inplace=True)
            #turns all na into 0
		m["sub_"+cell] = m[cell]-m[0]
            #making another column of data which is the subsetted numbers of counts for that cell
		newcols.append((m["sub_"+cell]))
            #once this calculation is each done for a column, add this new subsetted counts for each cell to the newcounts df
	newdf = pandas.concat(newcols,axis=1,sort=False)
        #so concatenating each of those newly appended columns of data into one dataframe
	indexonlydf = pandas.DataFrame(index=dfname.index)
        #the original index
	newdf = pandas.concat([newdf, indexonlydf], axis=1,sort=False)
	newdf.fillna(0, inplace=True)
        #adding the original index (so genes with 0 counts now reapper)
	return newdf

def subsampletocellnumber(Finalcellnumber,dfname):
	colstokeep = np.random.choice(dfname.columns, replace=False, size=Finalcellnumber)
	newdf = dfname[colstokeep]
	return newdf

def mainsubsample(dfs, readnumber, outputdfNames,outputDIR):
#instead of cellnumber being an input, I may want to just specify a fraction of the min cells to output for each subsample
#so then I'd automatically end up with 1/3 or 1/5 of the max number of cells available at that specified depth for the 4 samples?
	dfs2 = []
	for dataframe in dfs:
		newdf = subsampletoreadnumber(readnumber,dataframe)
		dfs2.append(newdf)
	mincellsleft = min([df.shape[1] for df in dfs2])
	dfs3=[]
	for dataframe,outName in zip(dfs2,outputdfNames):
		newdf = subsampletocellnumber(mincellsleft, dataframe)
		newdf.to_pickle(outputDIR+outName)
	return mincellsleft
#		dfs3.append(newdf)
#	return dfs3	
#think I just want to save the new subsampled DFs but not output or return the list of these DFs? Can decide later.


if __name__=="__main__":
#       try :
	print(argv)
	ReadNumber= int(argv[1])
	root1=argv[2]
	root2=argv[3]
	root3=argv[4]
	root4=argv[5]
	Directory=argv[6]
	
	
	file1=Directory+root1
	file2=Directory+root2
	file3=Directory+root3
	file4=Directory+root4
	df1 = pd.read_pickle(file1)
	df2 = pd.read_pickle(file2)
	df3 = pd.read_pickle(file3)
	df4 = pd.read_pickle(file4)
	FullDenseMatrixList=[df1, df2, df3, df4]
	
	SubsampleBarcode=np.random.randint(1000)	
	nameEnd='_'+str(ReadNumber)+'reads_'+str(SubsampleBarcode)+'.pkl'
	name1=root1[:-4]+nameEnd
	name2=root2[:-4]+nameEnd
	name3=root3[:-4]+nameEnd
	name4=root4[:-4]+nameEnd
	outputdfNameList=[name1, name2, name3, name4]

	SubsampledMatrix=mainsubsample(FullDenseMatrixList, ReadNumber, outputdfNameList, Directory)

#                outNormalizedFile = inputCSVfileA[:-4]+"normalizedToLastKBgene.csv"
#                outWindowedFile = inputCSVfileA[:-4]+"Windowed.csv"
#                outClusterredFile = inputCSVfileA[:-4]+"Clusterred.csv"



###note:to run this, need to activate virtualenvironment for jupyter notebook by typing:
###module load python/3.6.3
###then to run command type python3 Sparse2DenseMatrix.py <rootname>




