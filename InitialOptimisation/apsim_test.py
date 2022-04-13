from apsim import ApsimRunner, ApsimOptions
import os
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

    def testRun(self):
        """
        Test a complete run with output reading as well.
        """
        models = '/home/drew/code/ApsimX/bin/Debug/netcoreapp3.1/Models'
        repoPath = '/home/drew/code/CropGen'
        apsimfile = os.path.join(repoPath, 'apsim-inputs', 'sorghum-simple', 'sorg.apsimx')
        opts = ApsimOptions(models, apsimfile)
        runner = ApsimRunner()
        outputNames = ['Sorghum.Grain.Wt', 'Sorghum.AboveGround.Wt', 'Sorghum.Leaf.LAI']
        tableName = 'DailyReport'
        outputs = runner.run(opts, dict(), outputNames, tableName)
        keys = list(outputs)
        self.assertEqual(outputNames, keys)
        for i in range(0, len(keys)):
            data = outputs[keys[i]]
            self.assertEqual(517, len(data), msg = '%s: wrong number of outputs' % keys[i])

