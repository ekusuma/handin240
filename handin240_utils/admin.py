from handin240_utils.utils import bcolors, ConfigError

import subprocess as sp
import os

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

# Sets AFS permissions such that the student may no longer write to the directory
def closeStudentPerms(studentID, path):
    fsCmd = ["fs", "seta", "-dir", path, "-clear", "-acl"]
    peoplePerms = [
        "system:web-srv-users", "rl",
        "ee240:ta", "all",
        "ee240:staff", "all",
        "ee240", "all",
        "system:administrators", "all",
        studentID, "read"
    ]
    fsCmd += peoplePerms

    retVal = None
    devnull = open(os.devnull, "w")
    try:
        subprocess.check_call(fsCmd, stderr=devnull)
    except subprocess.CalledProcessError, e:
        retVal = studentID
    devnull.close()

    return retVal

def closeStudentDirs(basePath, dirs):
    badIDs = []
    for studentDir in dirs:
        path = basePath + "/" + studentDir
        retVal = closeStudentPerms(studentDir, path)
        if (retVal != None):
            badIDs.append(studentDir)
    if (len(badIDs) != 0):
        printBadIDs(badIDs)

