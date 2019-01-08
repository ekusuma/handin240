#!/usr/bin/env python3
import reportlab, os

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
import reportlab.rl_config

from contextlib import contextmanager

# Remember to remove _test suffix for production
from env_test import *

#Open my file, still using the "with" context manager goodness, but
# able to detect if the file isn't found (or other errors)
# See PEP 343 for more background
@contextmanager
def opened_with_error(filename, mode='r'):
    try:
        f = open(filename, mode)
    except IOError as err:
        yield None, err
    else:
        try:
            yield f, None
        finally:
            f.close

class HW_Code_Maker:
    """ Make the HWX_code.pdf file for turnin on Gradescope.

    This class encapsulates the functionality to make the HWX_code.pdf
    file.  Such a file is a single PDF with each problem's file(s)
    pretty-printed.  Many problems do not require code, and so nothing
    will be included in this PDF file for those problems.  Some problems
    have a single file and a few have multiple files.

    The resulting PDF will have pages for each file, in order of the
    problem.

    To use, initialize the object with a homework dictionary describing
    the problems in that homework assignment.  Then, call the make_code
    method.
    """

    LINE_SPACING = 10  # points
    TOP_MARGIN   = .5 * inch # points
    LEFT_MARGIN  = .5 * inch # points
    BOTTOM_MARGIN = .5 * inch # points
    BOTTOM_OF_PAGE = 792 - BOTTOM_MARGIN

    def __init__(self, **kwargs):
        """ Initialize with a dictionary describing the HW problems.

        Keyword Arguments: (both are required)
        number : a string used as the homework number.  Typically 0-A
        problems : an ordered list of problem description dictionaries.
                   Exact format is defined in method print_file().
        """
        self.hw_number = kwargs['number']
        self.problems  = kwargs['problems']
        self.line_number = 1
        self.init_xy()
        self.canvas = None

    def init_xy(self):
        """ Set the x and y attributes to be the top of the page. """
        self.x = HW_Code_Maker.LEFT_MARGIN
        self.y = HW_Code_Maker.TOP_MARGIN

    def make_code(self):
        """ Make the PDF file with all homework code files printed. """
        filename = 'hw{}_code.pdf'.format(self.hw_number)
        self.canvas = canvas.Canvas(filename,
                                    bottomup=0,
                                    pagesize=reportlab.lib.pagesizes.letter)
        # Need to add to the searchpath, so we can use a font that we specify
        reportlab.rl_config.TTFSearchPath.append(FONT_DIR)
        sFont = TTFont('SourceCodePro', 'SourceCodePro-Regular.ttf')
        pdfmetrics.registerFont(sFont)
        self.canvas.setFont('SourceCodePro', 10)

        for problem in self.problems:
            if problem['files']:
                for filename in problem['files']:
                    self.page_number = 1
                    self.print_file(filename, problem)
        self.canvas.save()

    def draw_text_object(self, a_string, color_style=None):
        """ Draw a string onto the PDF page at the current position.

        Arguments:
        a_string : which will be printed
        color_style : one of 'None', 'Header', 'Warning'
                      Indicates the string should be black, green or red.

        Returns: Nothing

        Note: The y attribute is updated such that the next string to be
              printed will be on a following line.
        """
        text_object = self.canvas.beginText()
        text_object.setTextOrigin(self.x, self.y)
        text_object.setFont('SourceCodePro', 10)
        if color_style == 'Header':
            text_object.setFillColor(colors.green)
        elif color_style == 'Warning':
            text_object.setFillColor(colors.red)
        else:
            text_object.setFillColor(colors.dimgrey)
        text_object.textLine(text=a_string)
        self.canvas.drawText(text_object)
        self.y += HW_Code_Maker.LINE_SPACING

    def draw_header(self, a_filename, prob_dict):
        """ Draw the header at the top of each page.

        The header is one or two lines at the top of each page in the PDF.
        Printed in Green, the header contains information about the problem,
        point values, drill status and filename.
        If the file has taken more than one page, the following headers
        will include a page number.

        Arguments:
        a_filename : the filename of the file being printed.  Note that this
                     is necessary outside of the prob_dict, as there could
                     be multiple files in the problem and we want to know
                     which is currently printing.
        prob_dict : the dictionary describing the problem.  Full documentation
                    of this dictionary is in the print_file method.

        Returns: Nothing
        """
        self.init_xy()
        prob_number = prob_dict['number']
        prob_drill  = prob_dict['drill']
        prob_points = prob_dict['points']
        if self.page_number == 1:
            to_print = 'Problem {}: [{} points]'.format(prob_number, prob_points)
            if prob_drill:
                to_print = to_print + ' Drill problem'
            self.draw_text_object(to_print, 'Header')
            to_print = 'Filename: {}'.format(a_filename)
            self.draw_text_object(to_print, 'Header')
        else:
            self.canvas.showPage()
            filename_length = len(a_filename)
            middle_length = 84 - 12 - filename_length - 1
            format_string = 'Filename: {{}} {{:>{}}} {{}}'.format(middle_length)
            to_print = format_string.format(a_filename, 'Page #:', self.page_number)
            self.draw_text_object(to_print, 'Header')
        self.y += HW_Code_Maker.LINE_SPACING # include a blank line
        self.page_number += 1


    def print_file(self, a_filename, prob_dict):
        """ Print a single file into the PDF on one or more pages.

        Each file is 'pretty-printed' in a fixed-width font, with line numbers
        added at the left side.  Note that the line numbers are assumed to
        never be greater than two digits.

        As each line is printed, it is checked for two errors (currently).
        If the line has one or more errors, then it will be printed in Red:
        1) Are there any tab characters on the line.  If so, the tabs are
           replaced by double spaces and an error message is printed after
           the line.
        2) Is the line (with tabs replaced) longer than 80 characters?  If
           so, the first 77 characters of the line are printed, followed
           by three periods ('...').  An error message is then printed which
           specifies how many characters are in the full line.
        Note: a single line could have both errors.

        If the file does not exist, then a red error message is printed
        which states so.

        Arguments:
        a_filename : the filename of the file being printed.  Note that this
                     is necessary outside of the prob_dict, as there could
                     be multiple files in the problem and we want to know
                     which is currently printing.
        prob_dict : a dictionary describing the current homework problem.

        Returns : Nothing

        The dictionary contains the following required keys:
        number : A string with the number of the homework assignment.
        drill : A boolean.  True if this problem is a drill problem.
                            False otherwise.
        points : An integer specifying the number of points for the problem.
        files : A list of filenames required for the problem.  Each element
                in the list is a string.  The elements should be ordered as
                the files should be printed.
                If the problem does not require any files, then this value
                should be a None (i.e. a NoneType)
        """
        self.line_number = 1
        self.draw_header(a_filename, prob_dict)

        with opened_with_error(a_filename) as (f_in, err):
            if err:
                line = 'File {} was not found'.format(a_filename)
                self.draw_text_object(line, color_style='Warning')
            else:
                for line in f_in:
                    if self.y > HW_Code_Maker.BOTTOM_OF_PAGE:
                        self.draw_header(a_filename, prob_dict)
                    contains_tabs = False
                    color_style = 'None'
                    if '\t' in line:
                        contains_tabs = True
                        line = line.replace('\t', '  ')
                        color_style = 'Warning'
                    line = line.rstrip()
                    line_length = len(line)
                    if line_length > 80:
                        to_print = '{:3d} {}...'.format(self.line_number, line[:77]) #truncates to 80 characters.  Ironic comment
                        self.draw_text_object(to_print, color_style='Warning')
                        to_print = 'Line length of {} (max is 80)'.format(line_length)
                        self.draw_text_object(to_print, color_style='Warning')
                    else:
                        to_print = '{:3d} {}'.format(self.line_number, line)
                        self.draw_text_object(to_print, color_style)

                    if contains_tabs:
                        self.draw_text_object('Line contains tabs' +
                               ' (each tab replaced by 2 spaces in this print)',
                               color_style)
                    self.line_number += 1
        self.canvas.showPage()

def main():
    prob1  = {'number' :  '1', 'drill' : True, 'points' : 3, 'files' : None}
    prob2  = {'number' :  '2', 'drill' : True, 'points' : 1, 'files' : None}
    prob3  = {'number' :  '3', 'drill' : True, 'points' : 1, 'files' : None}
    prob4  = {'number' :  '4', 'drill' : True, 'points' : 2, 'files' : None}
    prob5  = {'number' :  '5', 'drill' : True, 'points' : 3, 'files' : None}
    prob6  = {'number' :  '6', 'drill' : True, 'points' : 4, 'files' : None}
    prob7  = {'number' :  '7', 'drill' : True, 'points' : 4,
              'files' : ['hw1prob7.sv']}
    prob8  = {'number' :  '8', 'drill' : True, 'points' : 4, 'files' : None}
    prob9  = {'number' :  '9', 'drill' : True, 'points' : 4,
              'files' : ['hw1prob9.sv']}
    prob10 = {'number' : '10', 'drill' : True, 'points' : 6,
              'files' : ['hw1prob10.sv']}
    prob11 = {'number' : '11', 'drill' : False, 'points' : 6, 'files' : None}
    prob12 = {'number' : '12', 'drill' : False, 'points' : 4, 'files' : None}
    prob13 = {'number' : '13', 'drill' : False, 'points' : 6, 'files' : None}
    prob14 = {'number' : '14', 'drill' : False, 'points' : 6,
              'files' : ['hw1prob14.sv']}
    prob15 = {'number' : '15', 'drill' : False, 'points' : 10,
              'files' : ['hw1prob15.sv', 'hw1prob15_sim.txt']}
    hw_dict = {'number' : '1',
               'problems' : [prob1, prob2, prob3, prob4, prob5, prob6, prob7,
                             prob8, prob9, prob10, prob11, prob12, prob13,
                             prob14, prob15]}
    maker = HW_Code_Maker(**hw_dict)
    maker.make_code()

if __name__ == '__main__':
  main()
