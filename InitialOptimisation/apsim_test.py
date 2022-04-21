from apsim import ApsimRunner, ApsimOptions
import os
from pathlib import Path
from shutil import which
from unittest import TestCase

class ApsimTests(TestCase):
    def testWriteParameterFileInvalidData(self):
        """
        Test calling writeParameterFile() with invalid data.
        """
        with self.assertRaises(ValueError):
            apsim = ApsimRunner()
            apsim._writeParameterFile(4)

    def testWriteParameterFile(self):
        params = {
            "x": 0,
            "y": 1,
            "z": 2
        }
        keys = list(params)

        apsim = ApsimRunner()
        fileName = apsim._writeParameterFile(params)
        try:
            with open(fileName, 'r') as file:
                lines = file.readlines()
                self.assertEqual(len(keys), len(lines))
                for i, line in enumerate(lines):
                    expected = '%s = %s\n' % (keys[i], params[keys[i]])
                    self.assertEqual(expected, line)
        finally:
            os.remove(fileName)

    def testGetDbFileName(self):
        self.checkGetDbFileName('apsimx')
        self.checkGetDbFileName('apsim')
        self.checkGetDbFileName('txt')

    def checkGetDbFileName(self, ext):
        f = 'x/y/z.%s' % ext
        expected = 'x/y/z.db'
        self.assertEqual(expected, ApsimRunner()._getDbFileName(f))

    def getApsimCli(self):
        models = which('Models')
        if not os.path.exists(models):
            raise FileNotFoundError('Apsim CLI not found on path')
        return models

    def getSampleApsimFile(self):
        repoPath = Path(__file__).parent.parent.absolute()
        return os.path.join(repoPath, 'apsim-inputs', 'sorghum-simple', 'sorg.apsimx')

    def testRun(self):
        """
        Test a complete run with no changes. Ensure output is read correctly.
        """
        models = self.getApsimCli()
        apsimfile = self.getSampleApsimFile()
        opts = ApsimOptions(models, apsimfile)
        runner = ApsimRunner()
        outputNames = ['Sorghum.Grain.Wt', 'Sorghum.AboveGround.Wt', 'Sorghum.Leaf.LAI']
        tableName = 'DailyReport'
        outputs = runner.run(opts, dict(), outputNames, tableName)

        # Number of columns should be # outputs + 1 (for simulation name).
        self.assertEqual(len(outputNames) + 1, len(outputs.columns))

        for i in range(0, len(outputs.columns)):
            data = outputs[outputs.columns[i]]
            self.assertEqual(517, len(data), msg = '%s: wrong number of outputs' % outputs.columns[i])

    def testRunWithChanges(self):
        """
        Test a complete run, changing sowing population.
        """
        models = self.getApsimCli()
        apsimFile = self.getSampleApsimFile()
        opts = ApsimOptions(models, apsimFile)

        popns = [2, 10]

        for popn in popns:
            changes = dict()
            changes['[SowingRule].Script.Population'] = popn
            outputNames = ['Sorghum.SowingData.Population']
            tableName = 'HarvestReport'

            runner = ApsimRunner()
            outputs = runner.run(opts, changes, outputNames, tableName)

            self.assertEqual(2, len(outputs.columns))
            popnColumn = outputs[outputNames[0]]
            self.assertEqual(1, len(popnColumn))
            self.assertEqual(popn, popnColumn[0])