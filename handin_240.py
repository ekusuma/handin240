#!/usr/bin/python
# handin_240.py
#
# Main handin script for students to use to hand in their homework files. Needs
# a .cfg file to know how to handle each file (see the usage in README.md for
# details).
#
# Usage:
#   - cd into the directory with all of the necessary files
#   - Run script with the homework number as the argument:
#       ./handin_240 hw8
#   - If the student wishes to submit an incomplete homework (i.e. with certain
#     files missing or unable to compile) they may run the script with the -f flag

import os;
import optparse;
from env_test import *;
# Uncomment this line when rolling out for production
#from env import *;

###################### Some cool output formatting stuff #######################
class bcolors:
    HEADER = "\033[95m";
    OKBLUE = "\033[94m";
    OKGREEN = "\033[92m";
    WARNING = "\033[93m";
    FAIL = "\033[91m";
    ENDC = "\033[0m";
    BOLD = "\033[1m";
    UNDERLINE = "\033[4m";

# Some useful constants in the scope of this script
ERR_NOEXIST     = 0;
ERR_NOCOMPILE   = 1;
ERR_FAILTEST    = 2;

# A line of 80 *'s, to mark beginning and end of a header
HEADER_LEN = 80;
HEADER_LINE = "*" * HEADER_LEN + "\n";

# Generic error handler. If fatal is true, then the error will cause the program
# to terminate. Note that if cleanup is necessary in the case of an error (i.e.
# deleting temporary directories), then fatal should be set to false.
def error(message, fatal=False):
    print(bcolors.FAIL + "ERROR: " + bcolors.ENDC + message);
    if (fatal):
        exit(255);
    else:
        return 255;

# Generic warning handler.
def warning(message):
    print(bcolors.WARNING + "WARNING: " +bcolors.ENDC + message);

def writeHeaderLine(header):
    maxLen = HEADER_LEN - 2;    # Beginning and ending "*"
    remaining = maxLen - len(header);
    firstHalf = remaining // 2;
    secondHalf = remaining - firstHalf;
    headerLine = "*" + (" " * firstHalf) + header + (" " * secondHalf) + "*" + "\n";
    return headerLine;

# Returns a tuple of (options, args) parsed from the command line.
# Raises an error (and exits) if no arg for hwNum is given.
def getArgs():
    usage = "usage: %prog [-f] hwNum";
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-f", "--force", action="store_true", dest="force",
                      help="force handin even with bad files");
    (options, args) = parser.parse_args();
    if (len(args) != 1):
        parser.error("Must specify homework number as arg");
    return (options, args);

def checkValidOp(opString):
    # For use if there is an error
    badOp = "\nOffending instruction: '" + opString + "'";
    opArr = opString.split();
    if (len(opArr) < 2):
        error("Not enough args in config file" + badOp, fatal=True);
    handler = opArr[0];
    if (not isValidHandlerChar(handler)):
        error("Invalid handler char in config file" + badOp, fatal=True);

def parseConfig(configPath):
    if (not os.path.exists(configPath)):
        error("no such config file. Are you sure the hw number is correct?", fatal=True);
    configFile = open(configPath, "r");
    opArray = configFile.read().strip().split("\n");

    # Check validity of parsed operations
    for (i, line) in enumerate(opArray):
        # Remove line if empty or a comment
        if ((len(line) == 0) or (line[0] == "#")):
            opArray.pop(i);
            continue;
        checkValidOp(line);

    configFile.close();
    return opArray;

def isValidHandlerChar(handler):
    if ((len(handler) != 1) or (handler not in HANDLER_CHARS)):
        return False;
    else:
        return True;

def getOpError(mainFile, errType):
    if (errType == ERR_NOEXIST):
        errMessage = "file does not exist";
    elif (errType == ERR_NOCOMPILE):
        errMessage = "failed to compile";
    elif (errType == ERR_FAILTEST):
        errMessage = "failed TA testbench";
    else:
        errMessage = "unspecified error"
    return mainFile + ": " + bcolors.FAIL + errMessage + bcolors.ENDC;

def checkExistence(opArr):
    hasError = not os.path.exists("./" + opArr[1]);
    return hasError;

# TODO: checkCompilation(), checkTATB()

def doOperation(opString, personalOutput):
    opArr = opString.split();
    handler = opArr[0];
    mainFile = opArr[1];
    hasErrors = False;

    if (handler == "t"):
        hasErrors = checkExistence(opArr);
        if (hasErrors):
            output = getOpError(mainFile, ERR_NOEXIST);
            print(output);
            personalOutput = personalOutput + output + "\n";
            return (hasErrors, personalOutput);
        (hasErrors, vcsOutput) = checkCompilation(opArr);
        if (hasErrors):
            output = getOpError(mainFile, ERR_NOCOMPILE);
            print(output + "\n" + vcsOutput);
            personalOutput = personalOutput + output + "\n" + vcsOutput;
            return (hasErrors, personalOutput);
        (hasErrors, simOutput) = checkTATB(opArr);
        if (hasErrors):
            output = getOpError(mainFile, ERR_FAILTEST);
            print(output + "\n" + simOutput);
            personalOutput = personalOutput + output + "\n" + simOutput;
            return (hasErrors, personalOutput);
    elif (handler == "c"):
        hasErrors = checkExistence(opArr);
        if (hasErrors):
            output = getOpError(mainFile, ERR_NOEXIST);
            print(output);
            personalOutput = personalOutput + output + "\n";
            return (hasErrors, personalOutput);
        (hasErrors, vcsOutput) = checkCompilation(opArr);
        if (hasErrors):
            output = getOpError(mainFile, ERR_NOCOMPILE);
            print(output + "\n" + vcsOutput);
            personalOutput = personalOutput + output + "\n" + vcsOutput;
            return (hasErrors, personalOutput);
    elif (handler == "e"):
        hasErrors = checkExistence(opArr);
        if (hasErrors):
            output = getOpError(mainFile, ERR_NOEXIST);
            print(output);
            personalOutput = personalOutput + output + "\n";
            return (hasErrors, personalOutput);

    return (hasErrors, personalOutput);

def createErrLog(contents, path="."):
    fd = open(path + "/errors.log", "w");
    fd.write(contents);
    fd.close();

def getOutputHeader(hwNum, studentID):
    outputHeader = HEADER_LINE;
    outputHeader += writeHeaderLine("18240: " + hwNum);
    outputHeader += writeHeaderLine("Error log for: " + studentID);
    outputHeader += HEADER_LINE;
    return outputHeader;

def doHandin():
    # TODO: complete this function
    return None;

def main():
    exitStatus = 0;
    (options, args) = getArgs();

    # Save relevant fields
    isForced = options.force;
    hwNum = args[0];
    selfID = os.getlogin();     # Get student's Andrew ID

    # Initialize error log output and error flag
    personalOutput = getOutputHeader(hwNum, selfID);
    hasAnyErrors = False;

    # Parse config file and do relevant operations
    opArray = parseConfig(CFG_DIR + "/" + hwNum + ".cfg");
    for op in opArray:
        (hasErrors, personalOutput) = doOperation(op, personalOutput);
        if (hasErrors):
            hasAnyErrors = True;

    # Result strings WITH COLORS \o/
    handinCreated = bcolors.OKGREEN + "Handin file created." + bcolors.ENDC;
    handinNotCreated = bcolors.FAIL + "Handin file not created." + bcolors.ENDC;

    # Check if handin had any errors
    if (hasAnyErrors):
        warning = bcolors.WARNING + "WARNING: " + bcolors.ENDC;
        print("\n" + warning + "errors detected! See errors.log for details.\n");
        createErrLog(personalOutput);
        if (not isForced):
            print(handinNotCreated);
            print("If you wish to submit an incomplete homework, then run the " +
            "handin script again with the '-f' flag.");
        else:
            print(warning + "you are attempting to submit a file with errors! " +
                  "You will NOT receive any credit for files with errors.\n");
            print("If this is intentional on your part, type 'yes' and press Enter.");
            agreement = raw_input("I agree to hand in files with errors: ");
            if (agreement == "yes"):
                doHandin();
                print("\n" + handinCreated);
            else:
                print("\n" + handinNotCreated);
    else:
        doHandin();
        print("\n" + handinCreated);

    return exitStatus;

exit(main());
