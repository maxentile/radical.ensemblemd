""" Tests cases
"""
import os
import sys
import unittest

from radical.ensemblemd.exceptions import *
from radical.ensemblemd.tests.helpers import *

#-----------------------------------------------------------------------------
#
class ExecutionContextAPITestCases(unittest.TestCase):
    # silence deprecation warnings under py3

    def setUp(self):
        # clean up fragments from previous tests
        pass

    def tearDown(self):
        # clean up after ourselves 
        pass

    #-------------------------------------------------------------------------
    #
    def test__import(self):
        """ Tests whether we can import the execution context classes.
        """
        from radical.ensemblemd import StaticExecutionContext
        from radical.ensemblemd import DynamicExecutionContext

    #-------------------------------------------------------------------------
    #
    def test__static_execution_context_api(self):

        from radical.ensemblemd import StaticExecutionContext

        sec = StaticExecutionContext()

        try: 
            sec.execute("wrong_type")
        except Exception, ex:
            test_exception(exception=ex, expected_type=TypeError)