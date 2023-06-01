import unittest
from unittest.mock import MagicMock
from idlelib.highlight import HighlightParagraph
from idlelib.idle_test.mock_idle import Editor
from tkinter import Tk, Text

class HighlightParagraphTestCase(unittest.TestCase):
    def setUp(self):
        self.root = Tk()  # Create a Tkinter root window
        self.root.withdraw()
        self.text = Text(self.root)
        multiline_test_string = (
        "    '''The first line is under the max width.\n"
        "    The second line's length is way over the max width. It goes "
        "on and on until it is over 100 characters long.\n"
        "    Same thing with the third line. It is also way over the max "
        "width, but FormatParagraph will fix it.\n"
        "    '''\n")
        self.text.insert('1.0', multiline_test_string)
        self.editor = Editor(text=self.text)
        self.highlighter = HighlightParagraph(self.editor)
        

    def tearDown(self):
        self.root.destroy()  # Destroy the Tkinter root window

    def test_toggle_highlight(self):
        start, end = '1.0', '2.0'
        color = "light blue"
        self.highlighter.toggle_highlight(color)

        #check if the selected region is correctly highlighted
        self.assertIn('highlight_light blue', self.text.tag_names(start))
        
        #simulate unhighlighting
        color = "white"
        self.highlighter.toggle_highlight(color)

        #check if the selected region is correctly unhighlighted
        self.assertNotIn('highlight_lightblue', self.text.tag_names(start))
        
        

if __name__ == '__main__':
    unittest.main()
