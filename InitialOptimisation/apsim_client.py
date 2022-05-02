from ctypes import POINTER, Structure, addressof, c_byte, c_char, c_double, c_uint, c_uint32, cdll, create_string_buffer, pointer, sizeof
from ctypes import c_ushort, c_int, c_void_p, c_char_p, c_int32
from multiprocessing.dummy import Array
from pandas import DataFrame
from struct import unpack

class Replacement(Structure):
    """
    Wrapper around the replacement struct in the apsim client library.
    """
    _fields_ = [
        ("path", c_char_p),
        ("paramType", c_int32),
        ("value", c_char_p),
        ("value_len", c_int)
    ]

class Output(Structure):
    """
    Wrapper around the output_t struct in the apsim client library.
    """
    _fields_ = [
        # ("data", c_char_p),
        ("data", POINTER(c_byte)),
        ("len", c_uint32)
    ]

class ApsimClient:
    """
    ## ApsimClient

    Wrapper around the apsim client library, used for running apsim
    via an apsim server instance.

    ## Remarks

    Should think about holding the socket connection open for the lifetime
    of the class instance, rather than connecting/disconnecting for each run.

    Need to also think about memory management and ensure that we don't have
    any leaks.
    """

    def __init__(self):
        """
        Create a new apsim client instance.
        """
        self.__client = self.__getApsimClient()

    def __getApsimClient(self):
        """
        Get an apsim client handle, used to manage connections to the apsim server.
        """
        client = cdll.LoadLibrary("libapsimclient.so")
        client.connectToRemoteServer.restype = c_int
        client.connectToServer.restype = c_int
        client.createDoubleReplacement.restype = c_void_p
        client.createDoubleReplacement.argtypes = [c_char_p, c_double]
        client.runWithChanges.argtypes = [c_int, POINTER(POINTER(Replacement)), c_uint]

        client.readOutput.restype = POINTER(POINTER(Output))
        return client 

    def __connectToRemoteServer(self, ipAddress, port):
        """
        Connect to a remote apsim server instance.

        @param ipAddres: IP Address of the server.
        @param port:     Port on which the server is listening.

        @return socket connection.
        """
        c_ip = create_string_buffer(ipAddress.encode('UTF-8'))
        c_port = c_ushort(port)
        return self.__client.connectToRemoteServer(c_ip, c_port)

    def __disconnectFromServer(self, socket):
        """
        Disconnect from an apsim server instance.

        @param socket: socket connection returned from the connect() method.
        """
        self.__client.disconnectFromServer(c_int(socket))

    def __createDoubleReplacement(self, path, value):
        """
        Create a double replacement object.
        """
        # Create a null-terminated string.
        c_path = create_string_buffer(path.encode('UTF-8'))
        c_value = c_double(value)
        repl = Replacement.from_address(self.__client.createDoubleReplacement(c_path, c_value))
        return repl

    def __freeReplacement(self, replacement):
        """
        Free the replacement memory.
        """
        self.__client.replacement_free(pointer(replacement))

    def __convertToReplacements(self, parameters):
        """
        Convert the specified changes into an array of replacement objects.
        """
        # For now, I'm assuming all changes are numeric (ie no date/array changes).
        result = []
        for name, value in parameters.items():
            result.append(self.__createDoubleReplacement(name, value))
        return result

    def __readOutput(self, sock, outputNames, tableName):
        """
        Read outputs from apsim.

        @param sock:      Socket connection to server.
        @param outputs:   Array of output variable names to be read.
        @param tableName: Name of the table from which to read.

        @return:          Dataframe of results.
        """
        numCols = len(outputNames)
        if numCols < 1:
            raise ValueError("Must request at least one output variable")

        c_sock = c_int(sock)
        c_table = create_string_buffer(tableName.encode('UTF-8'))
        c_numParams = c_uint32(numCols)

        c_params_t = c_char_p * numCols
        c_params = c_params_t()
        buffers = []
        for i in range(0, numCols):
            buf = create_string_buffer(outputNames[i].encode('UTF-8'))
            c_params[i] = addressof(buf)
            buffers.append(buf) # Delay destruction

        # This will return a C array of output pointers (output_t**).
        outputs = self.__client.readOutput(c_sock, c_table, c_params, c_numParams)

        numRows = outputs[0].contents.len // sizeof(c_double)
        df = DataFrame(columns = outputNames)
        for i in range(0, numRows):
            for j in range(0, numCols):
                # Each output object contains a byte array of all rows of data for this
                # parameter. We need to take the i-th slice, where i is the row number,
                # and the slice width will be sizeof(double).
                startIndex = i * sizeof(c_double) # 0, 8, 16, ...
                endIndex = startIndex + sizeof(c_double) # 8, 16, 24, ...
                raw = outputs[j].contents.data[startIndex:endIndex]
                bits = b''.join([c_byte(x) for x in raw])

                # Server protocol is little-endian.
                value = unpack('<d', bits)[0]

                df.at[i, outputNames[j]] = value
        return df

    def __runOnServer(self, replacements, sock):
        """
        Run apsim.

        @param replacements: Changes to be applied before the simulation run.
        @param outputs:      Array of names of outputs to be read from the server.
        @param tableName:    Table from which outputs should be read.
        @param sock:         Socket connection to server.

        @return:             Dataframe containing one column per output plus an extra
                             column containing simulation names.
        """
        n = len(replacements)

        socket = c_int(sock)
        numChanges = c_uint(len(replacements))

        # Convert array of replacement objects to C array.
        replacement_p_p = POINTER(Replacement) * n
        changes = replacement_p_p()
        for i in range(0, n):
            changes[i] = pointer(replacements[i])

        # Send RUN command.
        self.__client.runWithChanges(socket, changes, numChanges)

    def run(self, parameters, outputs, tableName, serverIP, serverPort):
        """
        Run apsim using apsim server mechanism

        @param opts:       APSIM options (an ApsimOptions instance)
        @param parameters: Parameters to be changed. This should be a dict in
                           which the keys are the parameter names, and the
                           values are the parameter values
        @param outputs:    Array of names of outputs to be read.
        @param tableName:  Name of the table from which outputs should be read.
        @param serverIP:   IP Address of the server as a string
        @param serverPort: Port on which the server is listening.
        @return            Dataframe containing one column per output plus an
                           extra column containing simulation names.
        """

        # Connect to the server.
        sock = self.__connectToRemoteServer(serverIP, serverPort)

        try:
            # Convert changes to data structures recognised by the client library.
            replacements = self.__convertToReplacements(parameters)

            try:
                # Run apsim.
                self.__runOnServer(replacements, sock)

                # Read results.
                return self.__readOutput(sock, outputs, tableName)
            finally:
                # Free replacements memory
                for r in replacements:
                    self.__freeReplacement(r)
        finally:
            # Disconnect from the server.
            self.__disconnectFromServer(sock)
