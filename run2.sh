#!/bin/sh
#
#SBATCH --account=apam
#SBATCH --job-name=run_
# SBATCH --gres=gpu:1             # Request 1 gpu (Up to 4 on K80s, or up to 2 on P100s are valid).
#SBATCH -c 1                     # The number of cpu cores to use.
#SBATCH --time 0:20:00              # The time the job will take to run.
#SBATCH --mem-per-cpu=1gb        # The memory the job will use per cpu core.
#SBATCH --mail-type=ALL

python main_opt_loop_new.py 0 80 1
