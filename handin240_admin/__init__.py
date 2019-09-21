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

    def error_msg(msg):
        err = bcolors.ERROR + "ERROR: " + msg + bcolors.ENDC
        print(err)
        return err

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

# Sets AFS permissions such that the student may write to the directory
# Admins have usual admin permissions, and other students may not access
def openStudentPerms(studentID, path, dryrun=False, verbose=False):
    fsCmd = ['fs', 'seta', '-dir', path, '-clear', '-acl']
    peoplePerms = [
        'system:web-srv-users', 'rl',
        'ee240:ta', 'all',
        'ee240:staff', 'all',
        'ee240', 'all',
        'system:administrators', 'all',
        studentID, 'write'
    ]
    fsCmd += peoplePerms

    retVal = None
    devnull = open(os.devnull, 'w')
    try:
        if (verbose):
            print(' '.join(fsCmd))
        if (not dryrun):
            sp.check_call(fsCmd, stderr=devnull)
    except sp.CalledProcessError, e:
        retVal = studentID
    devnull.close()

    return retVal

def printBadIDs(idList):
    print('\n{}Error:{} unable to set perms for'.format(bcolors.FAIL, bcolors.ENDC))
    for id in idList:
        print('\t' + id)
    print('Please check that ID is correct, and that student is in the ECE system.')

# Creates a directory for each student inside of the basePath directory. ids
# must be an array of student IDs.
def createStudentDirs(basePath, ids, dryrun=False, verbose=False):
    badIDs = []
    for student in ids:
        path = basePath + '/' + student.lower()
        if ((not dryrun) and (not os.path.exists(path))):
            os.mkdir(basePath + '/' + student.lower())
        elif (verbose):
            print('\tHandin dir already exists for ' + student.lower() + ', skipping')
        retVal = openStudentPerms(student, path, dryrun)
        if (retVal != None):
            badIDs.append(student)
    if (len(badIDs) != 0):
        printBadIDs(badIDs)

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

def checkJson(jsonPath):
    jsonFile = open(jsonPath, 'r')
    try:
        json.load(jsonFile)
    except Exception as e:
        msg = 'error with {}: \n{}'.format(jsonPath, e)
        raise ConfigError(msg)
