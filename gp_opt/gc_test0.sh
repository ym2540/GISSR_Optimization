#!/bin/sh
#
#SBATCH --account=apam         # Replace ACCOUNT with your group account name
#SBATCH --job-name=GC_test0     # The job name.
#SBATCH -c 1                      # The number of cpu cores to use
#SBATCH --time=0-12:00                 # Runtime in D-HH:MM
#SBATCH --mem-per-cpu=5gb         # The memory the job will use per cpu core
 
module load anaconda

python test_gc.py
 
#End of script