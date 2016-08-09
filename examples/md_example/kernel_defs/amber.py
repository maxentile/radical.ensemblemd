#!/usr/bin/env python

"""A kernel that creates a new ASCII file with a given size and name.
"""

__author__    = "The ExTASY project"
__copyright__ = "Copyright 2015, http://www.extasy-project.org/"
__license__   = "MIT"

from copy import deepcopy

from radical.ensemblemd.exceptions import ArgumentError
from radical.ensemblemd.exceptions import NoKernelConfigurationError
from radical.ensemblemd.engine import get_engine
from radical.ensemblemd.kernel_plugins.kernel_base import KernelBase

# ------------------------------------------------------------------------------

_KERNEL_INFO = {

    "name":         "custom.amber",
    "description":  "Molecular Dynamics with Amber software package http://ambermd.org/",
    "arguments":   {"--mininfile=":
                        {
                            "mandatory": False,
                            "description": "Input parameter filename"
                        },
                    "--mdinfile=":
                        {
                            "mandatory": False,
                            "description": "Input parameter filename"
                        },
                    "--topfile=":
                        {
                            "mandatory": False,
                            "description": "Input topology filename"
                        },
                    "--crdfile=":
                        {
                            "mandatory": False,
                            "description": "Input coordinate filename"
                        },
                    "--cycle=":
                        {
                            "mandatory": False,
                            "description": "Cycle number"
                        }
                    },
    "machine_configs": 
    {

        "ncsa.bw_local":
        {
            "environment"   : {},
            "pre_exec" : ["module use --append /projects/sciteam/gkd/modules","module load openmpi","source /projects/sciteam/gkd/virtenvs/mpi4py/20151210_OMPI20151210-DYN/bin/activate","export PATH=$PATH:/projects/sciteam/gkd/amber/bin"],
            "executable" : ["sander"],
            "uses_mpi"   : True
        }            
    }
}


# ------------------------------------------------------------------------------
#
class kernel_amber(KernelBase):

    def __init__(self):

        super(kernel_amber, self).__init__(_KERNEL_INFO)
     	"""Le constructor."""
        		
    # --------------------------------------------------------------------------
    #
    @staticmethod
    def get_name():
        return _KERNEL_INFO["name"]
        

    def _bind_to_resource(self, resource_key):
        
        if resource_key not in _KERNEL_INFO["machine_configs"]:
            if "*" in _KERNEL_INFO["machine_configs"]:
                # Fall-back to generic resource key
                resource_key = "*"
            else:
                raise NoKernelConfigurationError(kernel_name=_KERNEL_INFO["name"], resource_key=resource_key)

        cfg = _KERNEL_INFO["machine_configs"][resource_key]

        #change to pmemd.MPI by splitting into two kernels
        if self.get_arg("--mininfile=") is not None:
            arguments = [
                           '-O',
                            '-i',self.get_arg("--mininfile="),
                            '-o','min%s.out'%self.get_arg("--cycle="),
                            '-inf','min%s.inf'%self.get_arg("--cycle="),
                            #'-r','md%s.crd'%self.get_arg("--cycle="),
                            '-r','md%s.rst'%self.get_arg("--cycle="),
                            '-p',self.get_arg("--topfile="),
                            '-c',self.get_arg("--crdfile="),
                            #'-ref','min%s.crd'%self.get_arg("--cycle=")
                            '-ref','min%s.rst7'%self.get_arg("--cycle=")
                        ]
        else:
            arguments = [
                            '-O',
                            '-i',self.get_arg("--mdinfile="),
                            '-o','md%s.out'%self.get_arg("--cycle="),
                            '-inf','md%s.inf'%self.get_arg("--cycle="),
                            #'-x','md%s.ncdf'%self.get_arg("--cycle="),
                            '-x','md%s.nc'%self.get_arg("--cycle="),
                            '-r','md%s.rst'%self.get_arg("--cycle="),
                            '-p',self.get_arg("--topfile="),
                            #'-c','md%s.crd'%self.get_arg("--cycle="),
                            '-c','md%s.rst'%self.get_arg("--cycle="),
                        ]
       
        self._executable  = cfg["executable"]
        self._arguments   = arguments
        self._environment = cfg["environment"]
        self._uses_mpi    = False
        self._pre_exec    = cfg["pre_exec"] 

# ------------------------------------------------------------------------------
