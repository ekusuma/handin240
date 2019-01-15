# env.py
#
# Environment variables (such as paths) that are useful for the handin tool. If
# intended directories do change over time, redefine their values here.
#
# This env file is meant for the staff-facing files, and has to be updated with
# paths relevant for the staff scripts. THIS FILE IS DIFFERENT FROM THE env.py
# IN THE STUDENT BRANCH.
#
# Edric Kusuma (ekusuma)

# Main course directory in AFS space
#COURSE_DIR = "/afs/ece.cmu.edu/class/ee240";
# Directory for test use
COURSE_DIR = "/afs/ece.cmu.edu/class/ee240/STAFF/ekusuma/240handin/course";

# Directory where student submissions should be entered
HANDIN_DIR = COURSE_DIR + "/handin";

# Directory where homework files will be (currently unused)
HANDOUT_DIR = COURSE_DIR + "/handout";

# Course staff directory (students do NOT have access to here!)
STAFF_DIR = COURSE_DIR + "/STAFF";

# Location of current student roster
ROSTER = STAFF_DIR + "/roster_s19.csv";

# Location of homework cfg files
CFG_DIR = STAFF_DIR + "/scripts/handinCfgs";
