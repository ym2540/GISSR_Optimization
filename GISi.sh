#!/bin/sh
#
#SBATCH --account=apam
#SBATCH --job-name=GISi
#SBATCH -c 1
#SBATCH --time 4:00:00
#SBATCH --mem-per-cpu=1gb

python main_opt_loop_new.py 163 163 5.0 2040 1529