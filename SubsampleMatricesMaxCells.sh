#!/bin/bash
#SBATCH --job-name=subsampleDense                     # Job name
#SBATCH --mail-type=ALL                           # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=joseph.cardiello@colorado.edu                       # Where to send mail
#SBATCH --nodes=1                               # Number of nodes requested
#SBATCH --ntasks=1                              # Number of CPUs (processor cores/tasks)
#SBATCH --mem=25G                               # Memory limit
#SBATCH --time=01:00:00                         # Time limit hrs:min:sec
#SBATCH --partition=short                       # Partition/queue requested on server
#SBATCH --output=/scratch/Users/joca4543/190805_NB501447_0525_AHVFJNBGXB/results/2019_08_09/eofiles/%x.%j.out       # Standard output
#SBATCH --error=/scratch/Users/joca4543/190805_NB501447_0525_AHVFJNBGXB/results/2019_08_09/eofiles/%x.%j.err        # Standard error log

### Displays the job context
echo Job: $SLURM_JOB_NAME with ID $SLURM_JOB_ID
echo Running on host `hostname`
echo Job started at `date +"%T %a %d %b %Y"`
echo Directory is `pwd`
echo Using $SLURM_NTASKS processors across $SLURM_NNODES nodes

pwd; hostname; date

module load python/3.6.3
export PATH=$PATH:/scratch/Users/joca4543/virtualEnvironments
export PATH=$PATH:/scratch/Users/joca4543/virtualEnvironments/cellranger-3.1.0
export PATH=$PATH:/scratch/Users/joca4543/190805_NB501447_0525_AHVFJNBGXB/results/2019_08_09/sbatch/pythonScripts/

###Variables:
readnumb=$1
Directory="/scratch/Users/joca4543/190805_NB501447_0525_AHVFJNBGXB/results/2019_08_09/DenseAndSubsampledMatrices/"
root1='Ethan_ControlDense.pkl'
root2='Ethan_HSDense.pkl'
root3='Eric_ControlDense.pkl'
root4='Eric_HSDense.pkl'

python3 SubsampleMatricesMaxCells.py ${readnumb} ${root1} ${root2} ${root3} ${root4} ${Directory}


###to run this command type sbatch Sparse2DenseMatrix.sh <rootname>                                                                                         



