# env.py
#
# Environment variables (such as paths) that are useful for the handin tool. If
# intended directories do change over time, redefine their values here.
#
# Edric Kusuma (ekusuma)

# Path to repo's folder
REPO_DIR = "/afs/ece.cmu.edu/class/ee240/STAFF/ekusuma/240handin";

# Main course directory in AFS space
#COURSE_DIR = "/afs/ece.cmu.edu/class/ee240";
# Directory for test use
COURSE_DIR = "/afs/ece.cmu.edu/class/ee240/STAFF/ekusuma/240handin/course";

# Directory where student submissions should be entered
HANDIN_DIR = COURSE_DIR + "/handin";

# Directory where homework files will be
HANDOUT_DIR = COURSE_DIR + "/handout";

# Location of homework cfg files
CFG_DIR = HANDOUT_DIR + "/hwConfigs";

# Location of font files for ReportLab
FONT_DIR = REPO_DIR + "/lib";
