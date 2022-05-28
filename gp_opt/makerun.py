import sys
import os

class GC_job:

    def __init__(self, id_, topo_file, storm_file):
        self.id_ = str(id_)
        self.topo_file = topo_file
        self.storm_file = storm_file
        self.job_path = os.pth.join('jobs/', self.id)
        os.mkdir(self.job_path)

    def run_job(self):
        script_name = 'GC_' + str(self.id_) + '.sh'
        script_path = os.path.join(self.job_path, script_name)
        self.create_makefile()
        self.create_setrun()
        self.create_script()
        cmd = 'sbatch ' + script_path
        os.system(cmd)

    def create_makefile(self):
        path = os.path.join(self.job_path, 'Makefile')
        file = open(path, 'w')
        file.write("#!/bin/sh\n")
        file.write("#\n")
        file.write("#SBATCH --account=apam\n")
        file.write("#SBATCH --job-name=GC_" + self.id_ + "\n")
        file.write("#SBATCH -c 1\n")
        file.write("#SBATCH --time 0:01:00\n")
        file.write("#SBATCH --mem-per-cpu=5G\n\n")

        file.write("make new\n")
        file.write("make .output\n")


def make_storm_file(id_, phi):
    """
    Input:
        id: id of job
        phi: storm parameters
    Output:
        storm_path: path to new storm file with given phi params

    Creates a new storm file with specified storm params
    """


def make_topo_file(id_, h):
    """
    Input:
        id: id of job
        h: height of wall
    Output:
        topo_path: path to new topo file with given wall height (h)

    Creates new topo file with wall height as specified
    NEEDS: A basic topo file with wall h=0 and location of wall #TODO
    """
