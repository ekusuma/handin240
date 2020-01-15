# 18240 Handin Tool (student ver.)
A handin utility tool for 18240 assignments. Meant to streamline student
workflow with respect to code submissions with the intent of removing Autolab
from the flow entirely, as well as make the lives of the (best) TAs easier.

Written in Python, updated to Python3

If you have any problems/questions *please read this in its entirety first*. If
you still have problems/questions, then put up a post on Piazza or contact Edric
at <ekusuma@cmu.edu>.

## Usage
**IMPORTANT!!!**

Before you can use this script, *you must perform some setup*. Thankfully this
setup only needs to be done once.

### Initialization
First of all, you'll have to make some edits to your `.bashrc` and
`.bash_profile` (hopefully you'll have already done this beforehand, preferrably
in preparation for Lab0).

1. **If you are not doing this on a computer in the ECE lab:** SSH into an ECE
   machine. There is a Unix guide on Canvas if you're confused as to what SSH
   means.
2. Edit your `.bashrc` by typing (do not type in the `$`!)

```bash
$ vim ~/.bashrc
```
If you are not familiar with Vim, then guide on Canvas also goes through this.
Otherwise you can just Google how to use Vim.
3. Add the following line to your `.bashrc`

```
source /afs/ece/class/ece240/bin/setup_240
```
4. Edit your `.bash_profile` by typing

```bash
$ vim ~/.bash_profile
```
5. Add the following lines to your `.bash_profile`

```
if [ -f $HOME/.bashrc ]; then
    source $HOME/.bashrc
fi
```

If you did this correctly, then the next time you log on (you'll have to close
and reopen your terminal) you should be able to type the following commands
without receiving an error:
```bash
$ which vcs
$ which quartus
$ which vlogan
$ which handin240
```

Now that you've done this, simply run
```bash
$ init_handin240
```
and you'll have installed all the necessary dependencies for the handin script.

### Using the handin script
To actually perform a handin, first make sure you are in a folder that has
**all** of the files you need to hand in for the homework. Then run
```bash
$ handin240 hwNum
```
Where `hwNum` is the number of the homework you are trying to submit. For
example, to submit hw1 you would type into your terminal
```bash
$ handin240 hw1
```

The handin script will do the following:
1. Checks to see that the file exists.
2. If necessary, checks to see that the file compiles.
3. Submits all files to your handin directory in AFS.
4. Creates a PDF of your code **that you must submit to Gradescope**. The name
   of this PDF will be `hwNum_code.pdf`.

To reiterate: **DO NOT FORGET TO SUBMIT THE PDF TO GRADESCOPE!** Remember that
homework assignments have both code *and* a written component. Don't forget, or
you won't receive credit for your work! You'll need to either `scp` or use some
other file transfer program to copy the PDF to your machine, so that you can
submit to Gradescope.

### Handing in bad files
You may notice that if you try to hand in code that either does not exist, or
does not compile, the handin aborts. This is intentional. As per course policy:
**code that does not compile will receive zero points**. No exceptions.

Of course, sometimes you simply don't have time to finish all of an assignment.
We get it, it happens all too often. If you want to handin an incomplete
assignment then run the script with the `-f` flag:
```bash
$ handin240 hwNum -f
```
and this will force the handin with incomplete files.

Additionally, you may opt to skip the compilation step by using the `-s` option.
This is best used if you had just compiled the files on your own before
attempting to submit. If you skipped the compilation step and your code doesn't
compile, again **you will get a zero**.

Again, **do not forget to submit the PDF to Gradescope**!
