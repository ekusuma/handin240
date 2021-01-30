# 18240 Handin Tool
A handin utility tool for 18240 assignments. Meant to streamline student
workflow with respect to code submissions with the intent of removing Autolab
from the flow entirely, as well as make the lives of the (best) TAs easier. Also
includes some utility scripts that would be useful for the new workflow.

Written in Python, ported to Python3.

## Repository Organization
The repository is organized into the following branches:

| Branch Name    | Description                                                         |
| -------------: | ------------------------------------------------------------------- |
| `master`       | Track overall project, some example files, and define env variables |
| `dev/staff`    | Development branch for staff-facing files                           |
| `dev/student`  | Development branch for student-facing files                         |
| `prod/staff`   | Production branch for staff-facing files (to host on AFS)           |
| `prod/student` | Production branch for student-facing files (to host on AFS          |

All development is to be done on the `dev/*` branches. Once new features are
complete **and have been tested**, they may be merged to their respective `prod/*`
branch.

The `master` branch is just here to document the roadmap of the project as a
whole (i.e. both student and staff branches). Files in [lib/](lib/) serve as
helpful reference files, as well as the font(s) needed for Reportlab to
function.

For usage of scripts, *please see the relevant branches' READMEs*.

## Todos
### Overall Todos
- ~~Write different READMEs for both staff and student branches~~
- ~~Get basic setup done in AFS~~
- ~~Refactor scripts into object-oriented, for ease of use~~
- Define TATB directory and usage
- ~~Convert Python scripts into executables~~
- ~~Edit `.cfg` file spec to match pretty-print code script~~

### Staff Todos
- ~~Add functionality to edit existing cfg files~~
- ~~Find a way to supress stdout~~
- ~~Change `close_handin` to also run compile checks on student code~~
- ~~Create script to modify AFS permissions for each student directory~~

### Student Todos
- ~~Stop being lazy and actually document code~~
- ~~Implement a "dry run" feature that just does error checks~~
- Implement automatic tester
- ~~Add timestamp for each execution of handin (for stat tracking)~~
- ~~Find a way to supress stdout/stderr~~
- ~~Error handling when necessary files do not exist~~
- ~~Check if script works if files are within STAFF directory~~ *Nope, we'll have
  to deploy student files in the public course space*
- ~~Implement compilation success checker~~
- Add ability to check module headers (*currently broken*)

## Installation
1. Ensure [config.ini](config.ini) is defined (things like course folder,
   handin, staff folder, etc), and push to `master`.
2. `cd` to the folder where the **student** scripts should be deployed
3. Clone the student repo

```bash
$ cd $STUDENT_BIN_DIR
$ git clone git@git.ece.cmu.edu:ekusuma/240-handin.git -b prod/student
```
4. Checkout the `config.ini` file from `master` to student repo

```bash
$ git checkout master config.ini
```
5. `cd` to the folder where the **staff** scripts should be deployed
6. Clone the staff repo

```bash
$ cd $STAFF_BIN_DIR
$ git clone git@git.ece.cmu.edu:ekusuma/240-handin.git -b prod/staff
```
7. Checkout the `config.ini` file from `master` to staff repo

```bash
$ git checkout master config.ini
```

## Specification
Student workflow should (roughly) be as follows:
1. Do homework involving "PDFed" answers and "Code" answers. Code answers will
be in a set of `.sv`, `.timing`, `.asm`, etc files. There may be multiple code answer
files, of varying types. The PDFed answer file is a scan of the student’s
handwritten work, for instance. **There will only ever be a single PDFed file.**
2. Student places code files in a directory in their own AFS space. This is
probably where they’ve been working anyway, as they need access to VCS, as240,
etc.
3. Student runs our handin script, as they now do. The script is a python
program. We envision lots of cool things that this script will eventually
do.
4. Student discovers there is a new file in the AFS directory - a PDF file
with a name like `HW3_code.pdf`. This file is a "pretty" version of their
code files.
5. Student copies `HWX_code.pdf` to a local machine, where the "PDFed"
file exists.
6. Student goes to gradescope and submits each file to a separate
homework assignment: HW3 and HW3-code, for instance.
7. After homework is graded, they go to gradescope to get their grades on the
two portions of the homework. The HWX-code assignment contains the pretty pdf,
which has been annotated with style or other comments. The HWX-code assignment
has rubrics not only for style, but also for all of the functionality tests that
have been graded.

Some potential features include:
- Detect the student’s Andrew ID
- Check that the current directory is in the student’s space (actually, that
it isn’t in the class space and is a writeable directory)
- Check that each required file exists.
- Copy each required file into the handin directory in the course space
- Use `reportlab` to make a pretty pdf with each code file printed
on a different page.
- Test the file and report results:
    - We will need to find some workaround involving permissions. Students need
      to be able to read the TA testbenches, but if they can then too much
      information would be disclosed. Perhaps a `.svp` inside of the `handout`
      directory is the way to go?
    - What happens here will vary depending on the type of question. At the very
    least, it would check for proper compilation. It could try using our
    testbench on the student’s design. It might use a simple testbench, as
    opposed to a deeper grading testbench.
    - It would be nice if all of the VCS garbage output was captured and parsed
    without the student seeing it.  Ideally, the student would just get a report
    that looks something like:
```
Problem 3: Your file (hw6prob3.sv) does not compile.
Problem 4: 3 of 4 tests passed
Problem 7: File hw6prob7.timing was not found
The file hw6_code.pdf was created. Make sure to submit this file to gradescope!
```

Potential utility scripts that aren't used for students:
- Parse a roster of Andrew IDs to create folders for their submissions for a
  given homework.
- Add the ability to automatically configure `fs` so student has R/W permissions
- Also the ability to disable those permissions once the deadline passes
