__author__    = "Vivek Balasubramanian <vivek.balasubramanian@rutgers.edu>"
__copyright__ = "Copyright 2016, http://radical.rutgers.edu"
__license__   = "MIT"

from radical.entk import EoP, AppManager, Kernel, ResourceHandle

from echo import echo_kernel
from randval import rand_kernel
from sleep import sleep_kernel

ENSEMBLE_SIZE=2
INPUT_PAR_Q = [20 for x in range(1, ENSEMBLE_SIZE+1)]
ITER = [1 for x in range(1, ENSEMBLE_SIZE+1)]

class Test(EoP):

	def __init__(self, ensemble_size, pipeline_size):
		super(Test,self).__init__(ensemble_size, pipeline_size)

	def stage_1(self, instance):

		global INPUT_PAR
		global ENSEMBLE_SIZE

		if instance <= ENSEMBLE_SIZE:

			k1 = Kernel(name="sleep")
			k1.arguments = ["--file=output.txt","--text=simulation","--duration={0}".format(INPUT_PAR_Q[instance-1])]
			k1.cores = 1

			# File staging can be added using the following
			#k1.upload_input_data = []
			#k1.copy_input_data = []
			#k1.link_input_data = []
			#k1.copy_output_data = []
			#k1.download_output_data = []

			return k1

		else:

			m1 = Kernel(name="randval")
			m1.arguments = ["--upperlimit=20"]

			m1.copy_input_data = []

			for inst in range(1, ENSEMBLE_SIZE+1):

				m1.copy_input_data += ['$ITER_{0}_STAGE_1_TASK_{1}/output.txt'.format(ITER[instance-1],inst)]

			return m1


	def branch_1(self, instance):


		if instance <= ENSEMBLE_SIZE:
			ITER[instance-1] += 1

		else:
			flag = self.get_output(stage=1, task=ENSEMBLE_SIZE+1)
			print 'Output of analysis in stage 1 = {0}'.format(flag)



if __name__ == '__main__':

	# Create pattern object with desired ensemble size, pipeline size
	pipe = Test(ensemble_size=ENSEMBLE_SIZE+1, pipeline_size=2)

	# Create an application manager
	app = AppManager(name='Adap_sampling')

	# Register kernels to be used
	app.register_kernels(echo_kernel)
	app.register_kernels(sleep_kernel)

	# Add workload to the application manager
	app.add_workload(pipe)
	

	# Create a resource handle for target machine
	res = ResourceHandle(resource="local.localhost",
				cores=4,
				#username='vivek91',
				#project = 'TG-MCB090174',
				#queue='development',
				walltime=10,
				database_url='mongodb://rp:rp@ds015335.mlab.com:15335/rp')

	# Submit request for resources + wait till job becomes Active
	res.allocate(wait=True)

	# Run the given workload
	res.run(app)

	# Deallocate the resource
	res.deallocate()
	