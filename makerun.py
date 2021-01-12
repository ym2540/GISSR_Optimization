import sys

fname = str(sys.argv[5])
i = int(sys.argv[1])
j = int(sys.argv[2])
k = int(sys.argv[3])
l = int(sys.argv[4])

f = open("GISi.sh", "w")
f.write("#!/bin/sh\n")
f.write("#\n")
f.write("#SBATCH --account=apam\n")
f.write("#SBATCH --job-name=GISi\n")
f.write("#SBATCH -c 1\n")
f.write("#SBATCH --time 4:00:00\n")
f.write("#SBATCH --mem-per-cpu=1gb\n\n")

ws = int(i*163.0/16.0)
we = int(j*163.0/16.0)
wh = 0.5*k
wall_year = 2040 

f.write("python main_opt_loop_new.py "+str(ws)+" "+str(we)+" "+str(wh)+" "+str(wall_year)+" "+fname) 
