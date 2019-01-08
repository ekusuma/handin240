# env.py
#
# Environment variables (such as paths) that are useful for the handin tool. If
# intended directories do change over time, redefine their values here.
#
# Edric Kusuma (ekusuma)

# List of legal handler chars
HANDLER_CHARS = [
    "e",    # Exists
    "c",    # Compiles
    "t"     # Passes tests
];

# Main course directory in AFS space
#COURSE_DIR = "/afs/ece.cmu.edu/class/ee240";
# Directory for test use
COURSE_DIR = "/afs/ece.cmu.edu/class/ee240/STAFF/ekusuma/240handin/course";

# Directory where student submissions should be entered
HANDIN_DIR = COURSE_DIR + "/handin";
# Directory where homework files will be
HANDOUT_DIR = COURSE_DIR + "/handout";

# Course staff directory (students do NOT have access to here!)
STAFF_DIR = COURSE_DIR + "/STAFF";

# Location of current student roster
ROSTER = STAFF_DIR + "/roster_s19.txt";

# Location of homework cfg files
CFG_DIR = STAFF_DIR + "/ekusuma/hw_configs";

# Location of font files for ReportLab
FONT_DIR = STAFF_DIR + "/ekusuma/240handin/lib";
