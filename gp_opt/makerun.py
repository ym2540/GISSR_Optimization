import sys
import os
import shutil
import pandas as pd


class GC_job:

    def __init__(self, id_, setrun_templ_path='setrun_template.py', makefile_templ_path='Makefile_template'):
        self.id_ = str(id_)
        self.job_path = os.path.join('jobs/', self.id)
        self.script_name = 'GC_' + str(self.id_) + '.sh'
        self.setrun_templ_path = setrun_templ_path
        self.makefile_templ_path = makefile_templ_path
        os.mkdir(self.job_path)

    def run_job(self):
        script_path = os.path.join(self.job_path, self.script_name)
        self.create_makefile()
        self.create_setrun()
        self.create_script()
        cmd = 'sbatch ' + script_path
        os.system(cmd)

    def create_script(self):
        path = os.path.join(self.job_path, self.script_name)
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

    def create_setrun(self):
        path = os.path.join(self.job_path, 'setrun.py')
        shutil.copyfile(self.setrun_templ_path, path)

    def create_makefile(self):
        path = os.path.join(self.job_path, 'Makefile')
        shutil.copyfile(self.makefile_templ_path, path)
    
    def create_all(self):
        self.create_makefile()
        self.create_setrun()
        self.create_script()
        self.run_job()


def make_storm_file(id_, phi):
    """
    Input:
        id: id of job
        phi: storm parameters
    Output:
        storm_path: path to new storm file with given phi params

    Creates a new storm file with specified storm params.
    """


def make_topo_file(id_, x):
    """
    Input:
        id: id of job
        h: height of wall
    Output:
        topo_path: path to new topo file with given wall height (h)

    Creates new topo file with wall height as specified
    NEEDS: A basic topo file with wall h=0 and location of wall #TODO
    """


def make_all(id_, x, phi):
    storm_path = make_storm_file(id_, phi)
    topo_path = make_topo_file(id_, x)
    df = pd.DataFrame([storm_path, topo_path], columns=['storm_path', 'topo_path'])
    path = os.path.join('jobs', id_, 'paths.csv')
    df.to_csv(path)
