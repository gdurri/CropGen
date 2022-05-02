from apsim_client import ApsimClient
import os
from pathlib import Path
from shutil import which
from unittest import TestCase

class ApsimClientTests(TestCase):
    def testRun(self):
        """
        Test a complete run with no changes. Ensure output is read correctly.
        """
        client = ApsimClient()
        outputNames = ['Sorghum.Grain.Wt', 'Sorghum.AboveGround.Wt', 'Sorghum.Leaf.LAI']
        tableName = 'DailyReport'
        outputs = client.run(dict(), outputNames, tableName, "127.0.0.1", 27746)

        # Number of columns should be # outputs + 1 (for simulation name).
        self.assertEqual(len(outputNames), len(outputs.columns))

        for i in range(0, len(outputs.columns)):
            data = outputs[outputs.columns[i]]
            # This .apsimx file produces 517 rows of daily outputs.
            self.assertEqual(517, len(data), msg = '%s: wrong number of outputs' % outputs.columns[i])

    def testRunWithChanges(self):
        """
        Test a complete run, changing sowing population.
        """
        popns = [2, 10]
        for popn in popns:
            changes = dict()
            changes['[SowingRule].Script.Population'] = popn
            outputNames = ['Sorghum.SowingData.Population', 'Yield', 'Biomass']
            tableName = 'HarvestReport'

            runner = ApsimClient()
            outputs = runner.run(changes, outputNames, tableName, "127.0.0.1", 27746)
            self.assertEqual(len(outputNames), len(outputs.columns))
            popnColumn = outputs[outputNames[0]]
            self.assertEqual(1, len(popnColumn))
            self.assertAlmostEqual(popn, popnColumn[0])