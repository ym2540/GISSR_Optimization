#!/bin/sh
#
#SBATCH --account=apam
#SBATCH --job-name=loopmrs
# SBATCH --gres=gpu:1             # Request 1 gpu (Up to 4 on K80s, or up to 2 on P100s are valid).
#SBATCH -c 1                     # The number of cpu cores to use.
#SBATCH --time 1:00:00              # The time the job will take to run.
#SBATCH --mem-per-cpu=1gb        # The memory the job will use per cpu core.
#SBATCH --mail-type=ALL

module load anaconda/3-5.1

let COUNT=0
for i in `seq 0 16`;
do
	for j in `seq $i 16`;
	do
		for k in `seq 1 10`;
		do
			for l in `seq 1 1`;
			do
                                python makerun.py $i $j $k $l $COUNT
                                let COUNT=COUNT+1
                                sbatch GISi.sh
				sleep 0.1s
				#if [ $COUNT -eq 999 ]
				#then
				#	sleep 3m
				#fi
			done
		done
	done
done
