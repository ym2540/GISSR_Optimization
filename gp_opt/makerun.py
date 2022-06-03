import sys
import os
import shutil
import pandas as pd


class GC_job:
    ## TODO setrun_templ
    def __init__(self, id_, x, phi, setrun_templ_path='setrun_sloped_beach.py', makefile_templ_path='Makefile_template'):
        self.id_ = str(id_)
        self.phi = phi
        self.x = x
        self.job_path = os.path.join('jobs/', self.id_)
        self.script_name = 'GC_' + str(self.id_) + '.sh'
        self.setrun_templ_path = setrun_templ_path
        self.makefile_templ_path = makefile_templ_path
        if not os.path.exists(self.job_path):
            os.mkdir(self.job_path)

    def run(self):
        script_path = os.path.join(self.job_path, self.script_name)
        self.create_makefile()
        self.create_setrun()
        self.create_script()
        cmd = 'sbatch ' + script_path
        cmd = '(cd ' + self.job_path + ' ; sbatch ' + self.script_name + ')'
        os.system(cmd)

    def create_script(self):
        path = os.path.join(self.job_path, self.script_name)
        file = open(path, 'w')
        file.write("#!/bin/sh\n")
        file.write("#\n")
        file.write("#SBATCH --account=apam\n")
        file.write("#SBATCH --job-name=GC_" + self.id_ + "\n")
        file.write("#SBATCH -N 4\n")
        file.write("#SBATCH --time=0-12:00\n")
        file.write("#SBATCH --mem-per-cpu=5gb\n\n")

        file.write("make new\n")
        file.write("make .output\n")

    def create_setrun(self):
        path = os.path.join(self.job_path, 'setrun.py')
        if not os.path.exists(path):
            shutil.copyfile(self.setrun_templ_path, path)

    def create_makefile(self):
        path = os.path.join(self.job_path, 'Makefile')
        if not os.path.exists(path):
            shutil.copyfile(self.makefile_templ_path, path)


def make_storm_file(id_, phi):
    """
    Input:
        id: id of job
        phi: storm parameters
    Output:
        storm_path: path to new storm file with given phi params

    Creates a new storm file with specified storm params.
    """
    path = os.path.join('jobs/', str(id_), 'ike.storm')  # TODO name
    if not os.path.exists(path):
        shutil.copyfile('ike.storm', path)
    return path

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
    path = os.path.join('jobs/', str(id_), 'beach_nowall.tt3')  # TODO name
    if not os.path.exists(path):
        shutil.copyfile('beach_nowall.tt3', path)
    return path


def make_all(id_, x, phi):

    folder = os.path.join('jobs', str(id_))
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    storm_path = make_storm_file(id_, phi)
    topo_path = make_topo_file(id_, x)

    df = pd.DataFrame([[storm_path, topo_path]], columns=['storm_path', 'topo_path'])
    path = os.path.join('jobs', str(id_), 'paths.csv')
    df.to_csv(path)
