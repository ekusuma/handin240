# env.py
#
# Environment variables (such as paths) that are useful for the handin tool. If
# intended directories do change over time, redefine their values here.
#
# Edric Kusuma (ekusuma)

# Main course directory in AFS space
COURSE_DIR = "/afs/ece.cmu.edu/class/ee240";

# Directory where student submissions should be entered
HANDIN_DIR = COURSE_DIR + "/handin";

# Directory where homework files will be
HANDOUT_DIR = COURSE_DIR + "/handout";

# Course staff directory (students do NOT have access to here!)
STAFF_DIR = COURSE_DIR + "/STAFF";

# Location of current student roster
ROSTER = STAFF_DIR + "/roster_s19.csv";

# Location of homework cfg files
CFG_DIR = HANDOUT_DIR + "/hwConfigs";

# Path to repo's folder
REPO_DIR_STUDENT = "/afs/ece.cmu.edu/class/ee240/bin/handin240_repo";
REPO_DIR_STAFF = STAFF_DIR + "/scripts/handin240_repo"

# Location of font files for ReportLab
FONT_DIR = REPO_DIR_STUDENT + "/lib";
