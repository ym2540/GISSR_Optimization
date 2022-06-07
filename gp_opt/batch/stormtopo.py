
from __future__ import print_function
from __future__ import absolute_import

import os
import numpy
import datetime

import batch.batch

import setrun

days2seconds = lambda days: days * 60.0**2 * 24.0

class StormTopoJob(batch.batch.Job):
    r""""""

    def __init__(self, storm_num, topo_num, storm_base_path='./', storms_path='./storms', topo_base_path='./', topo_path='./topos'):

        super(StormTopoJob, self).__init__()

        # Add extra job parameters
        self.omp_num_threads = 32
        # self.mic_omp_num_threads = 1
        # self.mic_affinity = "none"
        self.time = "12:00:00"
        # TODO:  check to see what the queue should be
        self.queue = None

        self.type = ""
        self.name = ""
        self.prefix = str(storm_num).zfill(5)
        self.storm_num = storm_num
        self.topo_num = topo_num
        self.executable = "xgeoclaw"

        self.account = "apam"

        # Create base data object
        
        self.rundata = setrun.setrun()

        # Storm specific data
        self.storm_file_path = os.path.abspath(os.path.join(storms_path, 
                                                        "%s.storm" % storm_num))

        # Set storm file
        self.rundata.surge_data.storm_file = self.storm_file_path

        # Topo path
        self.topo_file_path = os.path.abspath(os.path.join(topo_path, "%s.tt3" % topo_num))

        # Topo data
        self.rundata.topo_data.topofiles.append([3, 1, 6, self.rundata.clawdata.t0, self.rundata.clawdata.tfinal, self.topo_file_path])

        # Change time frame of simulation...
        # self.rundata.clawdata.t0 = days2seconds()
        # self.rundata.clawdata.tfinal = days2seconds()


    def __str__(self):
        output = super(StormTopoJob, self).__str__()
        output += "\n  Storm Number: %s" % self.storm_num
        output += "\n  Topo Number: %s " % self.topo_num
        return output


    def write_data_objects(self):
        r""""""

        # Write out all data files
        super(StormTopoJob, self).write_data_objects()

        # If any additional information per storm is needed do it here
        # ...
