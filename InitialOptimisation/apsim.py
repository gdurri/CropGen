from argparse import ArgumentTypeError
from collections import Counter
from subprocess import CalledProcessError, run, PIPE, STDOUT
from os import remove
from os.path import splitext, join
from pandas import read_sql_query
from tempfile import NamedTemporaryFile
import sqlite3

"""
Options related to an apsim run
"""
class ApsimOptions:
    """
    Create a new ApsimOptions instance.

    @param exe: path to the Models executable
    @param apsimFile: path to the .apsimx file to be run

    todo: we could support lots more options here
    """
    def __init__(self, exe, apsimFile):
        self.exe = exe
        self.apsimFile = apsimFile

"""
This class encapsulates the running of apsim and reading results.

Currently the run method works by calling the apsim CLI (Models.exe). In the
long run we will probably want to move to using the apsim server feature, as
the CLI is relatively inefficient for an optimisation workload.
"""
class ApsimRunner:
    def _writeParameterFile(self, parameters):
        """
        Write an apsim parameters file and return the filename.
        https://apsimnextgeneration.netlify.app/usage/editfile/
        """
        if not isinstance(parameters, dict):
            raise ValueError('parameters should be a dict')

        with NamedTemporaryFile(mode = 'w', encoding = 'utf8', delete = False) as file:
            for name, value in parameters.items():
                file.write('%s = %s\n' % (name, value))
            return file.name

    def _getDbFileName(self, apsimFile):
        """
        Get the name of the .db file for a given .apsimx file

        @param apsimFile: path to the .apsimx file.
        """
        return '%s.db' % splitext(apsimFile)[0]

    def _readOutputs(self, dbFile, outputNames, tableName):
        """
        Read outputs from apsim

        @param dbFile:      Path to the .db file.
        @param outputNames: array of the names of outputs to be read.
        @param tableName:   Name of the report table.
        @return             dataframe containing one column per output name,
                            plus an extra column containing simulation names.
        """

        # Ensure outputNames contains no duplicates.
        outputsList = Counter(outputNames)
        duplicates = [x for x in outputsList if outputsList[x] > 1]
        if len(duplicates) > 0:
            raise Exception("Attempted to read %d duplicate outputs (%s), this is probably a mistake" % (len(duplicates), duplicates))

        # Read outputs from DB.
        with sqlite3.connect(dbFile) as conn:
            # Construct comma-separated list of variable names.
            # Need to enclose each variable names in square brackets, in case
            # they contain spaces (or, more frequently, periods).
            variables = ', '.join(['[%s]' % x for x in outputNames])
            query = 'SELECT %s, s.Name as SimulationName FROM [%s], _Simulations s WHERE SimulationID = s.ID' % (variables, tableName)
            return read_sql_query(query, conn)

    def _runInternal(self, opts, parameterFile):
        """
        Run apsim with the specified parameter file. This function is intended
        for internal use only, and should not be called from outside this class.
        This function does not read results. This function will throw if apsim
        runs with errors.
        """
        # Arguments to be passed to the Models invocation.
        arguments = [
            '--edit "%s"' % parameterFile,
            opts.apsimFile
        ]

        # Run apsim. This will raise an exception if apsim if apsim returns a
        # non-zero exit code (ie if apsim runs with error).
        try:
            run(
                executable = opts.exe,
                args = arguments,
                encoding = 'utf8', # stdout/stderr encoding
                check = True, # Automatically throw an exception upon apsim error
                stdout = PIPE, # This configuration will cause stdout and stderr
                stderr = STDOUT # to be written to a single stream.
            )
        except CalledProcessError as e:
            # stderr was piped to stdout.
            raise Exception("APSIM ran with errors:\n%s" % e.stdout) from e

    def run(self, opts, parameters, outputs, tableName):
        """
        Run apsim
        
        @param opts:       APSIM options (an ApsimOptions instance)
        @param parameters: Parameters to be changed. This should be a dict in
                           which the keys are the parameter names, and the
                           values are the parameter values
        @param outputs:    Array of names of outputs to be read.
        @param tableName:  Name of the table from which outputs should be read.
        @return            Dataframe containing one column per output plus an
                           extra column containing simulation names.
        """

        # Validate input arguments.
        if not isinstance(opts, ApsimOptions):
            raise ArgumentTypeError("opts must be an ApsimOptions instance")

        # Generate parameter file for apsim.
        parameterFile = self._writeParameterFile(parameters)

        try:
            # Run apsim.
            self._runInternal(opts, parameterFile)
        finally:
            # Delete temp file
            remove(parameterFile)

        # Read outputs from .db file.
        dbFile = self._getDbFileName(opts.apsimFile)
        return self._readOutputs(dbFile, outputs, tableName)
