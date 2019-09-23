import ConfigParser
import subprocess as sp
import sys
import os
import json
import csv

class ConfigError(Exception):
    def __init__(self, message):
        self.message = "ConfigError: " + message
        super(Exception, self).__init__(self.message)

# Colors!
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[33m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def warning_msg(msg):
        warn = bcolors.WARNING + "WARNING: " + msg + bcolors.ENDC
        print(warn)
        return warn

    @staticmethod
    def error_msg(msg):
        err = bcolors.ERROR + "ERROR: " + msg + bcolors.ENDC
        print(err)
        return err

    @staticmethod
    def stripFormatting(s):
        contents = s

        # Remove formatting characters
        contents = contents.replace(bcolors.HEADER, "")
        contents = contents.replace(bcolors.OKBLUE, "")
        contents = contents.replace(bcolors.OKGREEN, "")
        contents = contents.replace(bcolors.WARNING, "")
        contents = contents.replace(bcolors.FAIL, "")
        contents = contents.replace(bcolors.ENDC, "")
        contents = contents.replace(bcolors.BOLD, "")
        contents = contents.replace(bcolors.UNDERLINE, "")

        return contents

def get_env(config_file):
    conf = ConfigParser.ConfigParser()
    conf.read(config_file)
    env = dict()
    try:
        # first parse all of the defaults
        for item in conf.defaults():
            env[item[0]] = item[1]
        # hopefully won't be clobbered by defaults
        for section in conf.sections():
            for item in conf.items(section):
                env[item[0]] = item[1]
    except Exception as e:
        print('Error parsing script config file:')
        print(e)
        # Will exit, so be careful with cleanup
        sys.exit(1)
    return env

def parseCSVField(csvPath, field='Andrew ID'):
    csvReader = csv.DictReader(csvPath)
    studentList = []
    for row in csvReader:
        studentList.append(row[field])
    return studentList

def searchCfg(hwNum, cfg_dir):
    fileName = hwNum + '_cfg.json'
    fileList = os.listdir(cfg_dir)
    for f in fileList:
        if (f.lower() == fileName.lower()):
            return '{}/{}'.format(cfg_dir, f)
    raise ConfigError('no config for {}'.format(hwNum))

def parseConfig(configPath):
    """Parses the config JSON file. See README for how these config files must
    be formatted/defined as.

    Raises an error if the path is invalid.

    Args:
        configPath (str): A path leading to the config JSON file. Must be a
            .json file.

    Returns:
        On success:
            (dict): A dictionary that has the parsed JSON mapped onto it. See
                the json module for details on how this is defined.

    """
    if (not os.path.exists(configPath)):
        error("no such config file. Are you sure the hw number is correct?", fatal=True)
    configFile = open(configPath, "r")
    try:
        config = json.load(configFile)
        return config
    except Exception, e:
        msg = "Error parsing config file:\n{}\n\nPlease contact course staff.".format(e)
        raise ConfigError(msg)
    finally:
        configFile.close()

def checkJson(jsonPath):
    jsonFile = open(jsonPath, 'r')
    try:
        json.load(jsonFile)
    except Exception as e:
        msg = 'error with {}: \n{}'.format(jsonPath, e)
        raise ConfigError(msg)

class Operation:
    def __init__(self):
        self.number = None
        self.existFiles = None
        self.compileFiles = None
        self.testFiles = None
        self.specificModules = None
        self.hasErrors = False
        self.err = ""
        self.useWildcard = False

    def clearErrors(self):
        self.hasErrors = False
        self.err = ""

    def checkWildcard(self):
        """Checks the list of files for wildcard specifiers, then adds files
        that satisfy the wildcard(s) to the list.

        Args:
            Nothing.

        Returns:
            Nothing.

        """
        tempExistFiles = set()
        tempCompileFiles = set()

        if (self.existFiles != None):
            for f in self.existFiles:
                if ("*" in f):
                # Add all the wildcard files
                    self.useWildcard = True
                    allFiles = set(glob.glob(f))
                    tempExistFiles = tempExistFiles.union(allFiles)
                else:
                    tempExistFiles.add(f)
            # Convert to a list, alphabetical order
            self.existFiles = sorted(list(tempExistFiles))
        if (self.compileFiles != None):
            for f in self.compileFiles:
                if ("*" in f):
                    allFiles = set(glob.glob(f))
                    tempCompileFiles = tempCompileFiles.union(allFiles)
                else:
                    tempCompileFiles.add(f)
            self.compileFiles = sorted(list(tempCompileFiles))

    def parseProblem(self, p):
        if (p["number"] != None):
            self.number = p["number"]
        if (p["files"] != None):
            self.existFiles = p["files"]
        if (p["compileFiles"] != None):
            self.compileFiles = p["compileFiles"]
        if (p["testFiles"] != None):
            self.testFiles = p["testFiles"]
        if (p["specificModules"] != None):
            self.specificModules = p["specificModules"]
        self.checkWildcard()

    def getOpError(self, mainFile, errType):
        """Create a formatted error message depending on what was wrong with the
        file.

        Args:
            mainFile (str): Name of a bad file.
            errType (int): Error type to classify problem with file.

        Returns:
            (str): Formatted string to display as an error.

        """
        if (errType == ERR_NOEXIST):
            errMessage = "file does not exist"
        elif (errType == ERR_NOCOMPILE):
            errMessage = "failed to compile"
        elif (errType == ERR_FAILTEST):
            errMessage = "failed TA testbench"
        else:
            errMessage = "unspecified error"
        return mainFile + ": " + bcolors.FAIL + errMessage + bcolors.ENDC

    def checkExistence(self):
        """Checks if every file in a file list exists within the current
        directory. Also lists what files do not exist, if any.

        Args:

        Returns:

        """
        for f in self.existFiles:
            if (not os.path.exists("./" + f)):
                self.hasErrors = True
                error = self.getOpError(f, ERR_NOEXIST) + "\n"
                self.err += error

    def removeOldDir(self, fileList, oldDir):
        return ", ".join(fileList).replace("{}/".format(oldDir), "")

    def compilationErrHandler(self, fileList, oldDir, err):
        self.hasErrors = True
        files = self.removeOldDir(fileList, oldDir)
        error = self.getOpError(files, ERR_NOCOMPILE) + "\n"
        self.err += error
        self.err += err.output + "\n"

    def checkCompilation(self):
        """Tries to compile files from a list using VCS (or vLogan+VCS), and
        checks to see if any compilation errors arise.

        Utilizes a temporary directory called `temp240handin`. As of now, this
        function will actually overwrite that directory if it already exists, so
        hope that the user doesn't have a folder with that name.

        If there is an error, it will also print the compiler message to stdout.

        Args:

        Returns:

        """
        # Preserve old directory to return to
        oldDir = os.getcwd()
        # Actual files are located in a different directory, so:
        fileList = []
        for fileName in self.compileFiles:
            fileList.append("{}/{}".format(oldDir, fileName))
        # Use tempfile's temporary directory creation. We must delete after done
        tempDir = tempfile.mkdtemp()
        os.chdir(tempDir)

        try:
            if (self.specificModules != None):
                # Command to run vlogan with files
                vloganCmd = ["vlogan", "-q", "-sverilog", "-nc"] + fileList
                try:
                    out = subprocess.check_output(vloganCmd, stderr=subprocess.STDOUT)
                except subprocess.CalledProcessError, e:
                    self.compilationErrHandler(fileList, oldDir, e)
                    return
                for module in self.specificModules:
                    vcsCmd = ["vcs", "-q", "-sverilog", "-nc", module]
                    try:
                        out = subprocess.check_output(vcsCmd, stderr=subprocess.STDOUT)
                    except subprocess.CalledProcessError, e:
                        self.compilationErrHandler(fileList, oldDir, e)
            else:
                vcsCmd = ["vcs", "-q", "-sverilog", "-nc"] + fileList
                try:
                    out = subprocess.check_output(vcsCmd)
                except subprocess.CalledProcessError, e:
                    self.compilationErrHandler(fileList, oldDir, e)
            return
        except (KeyboardInterrupt):
            raise
        finally:
            # Cleanup
            os.chdir(oldDir)
            shutil.rmtree(tempDir)

    # TODO: checkTATB()

    def do(self):
        """Performs an operation based on the op's attributes.

        Args:

        Returns:

        """
        if (self.existFiles != None):
            self.checkExistence()
            if (self.hasErrors):
                return self.err + "\n"
        if (self.compileFiles != None):
            self.checkCompilation()
            if (self.hasErrors):
                return self.err + "\n"
        return ""

def makeOpArray(config):
    opArray = []
    # Sort problem config array by problem number
    config = sorted(config, key=lambda p: p["number"])
    for problem in config:
        op = Operation()
        op.parseProblem(problem)
        opArray.append(op)
    return opArray

def writeHeaderLine(header, filled=False):
    """Used to write a line in the header for the errors.log file.

    Args:
        header (string): Text to write in one line of the header.

    Returns:
        (string): Formatted header line string.

    """
    headerLen = 80
    maxLen = headerLen - 2;         # -2 for beginning and ending "*"
    header = " " + header + " "
    remaining = maxLen - len(header)
    firstHalf = remaining // 2
    secondHalf = remaining - firstHalf
    if (filled):
        filler = "*"
    else:
        filler = " "
    headerLine = "*" + (filler * firstHalf) + header + (filler * secondHalf) + \
                 "*" + "\n"
    return headerLine

def getOutputHeader(studentID):
    headerLine = 80 * "*" + "\n"
    outputHeader = headerLine
    outputHeader += writeHeaderLine("18240: " + HW_NUM)
    outputHeader += writeHeaderLine("Error log for: " + studentID)
    outputHeader += headerLine
    return outputHeader

def createErrLog(contents, path="."):
    fd = open(path + "/errors.log", "w")
    toWrite = bcolors.stripFormatting(contents)
    fd.write(toWrite)
    fd.close()

def checkStudent(studentDir, opArray):
    personalOutput = getOutputHeader(studentDir)
    hasAnyErrors = False
    oldDir = os.getcwd()
    os.chdir(studentDir)

    print("\tChecking compile for {}".format(studentDir))
    for op in opArray:
        op.clearErrors()
        errString = op.do()
        if (op.hasErrors):
            hasAnyErrors = True
            personalOutput += writeHeaderLine("Problem {}".format(op.number), True)
            personalOutput += errString
    if (hasAnyErrors):
        createErrLog(personalOutput)

    os.chdir(oldDir)
    return (hasAnyErrors, personalOutput)

def writeResults(strArr):
    path = "{}/{}_results.txt".format(RESULTS_DIR, HW_NUM)
    if (len(strArr) < 1):
        return
    fd = open(path, "w")
    toWrite = "\n\n".join(strArr)
    toWrite = stripFormatting(toWrite)
    fd.write(toWrite)
    fd.close()
    print("Errored students written to {}".format(path))

def checkStudents(handinDir, studentList):
    global HW_NUM
    # Parse config file and do relevant operations
    cfgPath = searchCfg("{}_cfg.json".format(HW_NUM))
    # Take the proper (case-sensitive) hwNum
    HW_NUM = cfgPath[cfgPath.rindex("/")+1:cfgPath.index("_cfg.json")]
    config = parseConfig(CFG_DIR + "/" + HW_NUM + "_cfg.json")
    if (config == None):
        exit(255)
    opArray = makeOpArray(config)
    oldCwd = os.getcwd()
    os.chdir(handinDir)

    errorStudents = []
    for student in studentList:
        hasErrors = False
        (hasErrors, errOut) = checkStudent(student, opArray)
        if (hasErrors):
            errorStudents.append(errOut)
    os.chdir(oldCwd)
    return errorStudents

