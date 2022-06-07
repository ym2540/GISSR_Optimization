import sys
import os
import shutil

import pandas as pd

import batch


class GC_batch:

    def __init__(self, jobs):
        """
        input:
            jobs: list of dicts - [{storm_id:int, topo_id:int x:float, phi:dict of storm params}, ... ,  ]
        """

        self.jobs = jobs

    def create_storms(self):
        for job in self.jobs:
            # CREATE STORM WITH NAME job["storm_id"].storm in batch storm dir
            storm = job["storm_id"] + ".storm"
            path = os.path.join('storms/', storm)
            shutil.copyfile('ike.storm', path) # Obviously TODO

    def create_topos(self):
        for job in self.jobs:
            # CREATE TOPO WITH NAME job["topo_id"].t33 in batch topos dir
            topo = job["topo_id"] + ".tt3"
            path = os.path.join("topos/", topo)
            shutil.copyfile('beach_nowall.tt3', path)

    def create_all(self):
        self.create_topos()
        self.create_storms()

    def run(self):
        Jobs = []
        for job in self.jobs:
            Job = batch.StormTopoJob(self.storm_id, self.topo_id)
            Job.type = "batch_jobs"
            Jobs.append(Job)

        Controller = batch.HabaneroBatchController(jobs=Jobs)
        Controller.plot = False
        Controller.wait = True
        Controller.run()


class GC_job:
    # TODO setrun_templ
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
        file.write("#SBATCH --mail-type=ALL\n")
        file.write("#SBATCH --mail-user=av3081@columbia.edu\n")
        file.write("#SBATCH -N 1\n")
        file.write("#SBATCH -c 32\n")
        file.write("#SBATCH --time=0-12:00\n")
        file.write("#SBATCH --mem=187G\n\n")

        #file.write("export FFLAGS=\'-02 fopenmp\'") hardcoded in Makefile_template

        file.write("export OMP_NUM_THREADS=32\n\n")

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
