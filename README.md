# 18240 Handin Tool (staff ver.)
A handin utility tool for 18240 assignments. Meant to streamline student
workflow with respect to code submissions with the intent of removing Autolab
from the flow entirely, as well as make the lives of the (best) TAs easier. Also
includes some utility scripts that would be useful for the new workflow.

This branch contains scripts pertinent for staff workflow:
1. Creating handin directories for students for a given homework
2. Close said handin directories
3. Grant extensions for specific students for a given homework
4. Create homework configuration files

Written in Python, intended for ver. 2.7.5.

## Usage
### Handin directory utilities
#### Handin creation
**Requires a roster of students, in CSV.** The CSV must have an `Andrew ID`
column. Name of this roster can be redefined in `env.py`.

To create a handin directory, simply run:
```bash
$ ./open_handin hwNum
```
Where `hwNum` is the homework assignment to create a directory for, i.e.
```bash
$ ./open_handin hw5
```
By default, the script looks for the student roster defined in `env.py`. To pass
in a separate roster file, run the script with flag `-r` and pass in the path
to the roster, i.e.
```bash
$ ./open_handin -r /path/to/roster.txt hw5
```
The creation script also sets AFS permissions using `fs`, such that admins and
course staff may administrate each student handin directory, but only the
student may have write access.

Specifically:
```bash
$ fs seta -dir $studentDir -clear -acl system:web-srv-users rl ee240:ta all ee240:staff all ee240 all system:administrators all $studentID write
```
#### Handin closing
When the homework deadline has passed, course staff may replace each student's
write permissions with read permissions (to prevent late submissions) by running
the following:
```bash
$ ./close_handin hwNum
```
The script will also run the handin on all of the students' directories to
generate an `errors.log` file, to make things easier on the grading TA. There
will also be a summary file in `$STAFF_DIR/handinResults/hwNum_results.txt`.

Unfortunately this script must be run *manually*, as currently there is no
reliable way to facilitate `cron` jobs on AFS. *Just make sure that someone runs
this whenever a homework deadline is passed.*

#### Granting extensions
If for whatever reason, some students need an extension, you can reopen their
handin directories by running:
```bash
$ ./extend_handin hwNum studentID1, studentID2, ...
```
Note that if you want to extend for all students, just run the `open_handin`
script again.

### Creating homework config files
To prevent typos/headaches with JSON editing, there is a utility script for
generating handin files:
```bash
$ ./create_cfg hwNum
```
This will create a file called `hwNum_cfg.json` in the config folder defined in
`env.py`.

As of now, the config folder is located in `/afs/ece.cmu.edu/class/ee240/handout/hwConfigs`.

#### Config file details
This section is for the details of how the config file must be formatted. Use
the associated utility script to prevent mistakes.

Homework config files must meet the following requirements:
- Placed in the directory specified in `env.py`
- Be of `.json` format
- Be named `hwNum_cfg.json`

Note that for specifying files to submit with the wildcard `*`, it is assumed
that these will not need to be compiled. Be careful when using it.

The JSON must be an *array* of objects that have the following attributes:

| Attribute        | Type            | Description                                                                                                        |
| ---------------: | --------------- | -------------------------------------------------------------------------------------------------------------------|
| `number`         | `int`           | Problem number (i.e. order in homework)                                                                            |
| `drill`          | `bool`          | Is the problem a drill problem?                                                                                    |
| `points`         | `int`           | Point value for problem                                                                                            |
| `files`          | `[str] or null` | List of filenames that student must submit                                                                         |
| `compileFiles`   | `[str] or null` | List of files that must compile together (these files will be what is passed into `vcs`)                           |
| `testFiles`      | `[str] or null` | List of TA testbench file(s) for autograding.  These must be placed in a specific directory (to be decided)        |
| `specificModule` | `str or null`   | Name of a **specific** module to compile, in case the file has multiple conflicting modules. Uses `vlogan` parsing |

For the last four attributes, if the attribute does not apply then they may be
`null`.

See the example file `lib/hw1_cfg.json` in the `master` branch for guidance.
