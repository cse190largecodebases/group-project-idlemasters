import unittest
from idlelib.highlight import HighlightParagraph
from idlelib.iomenu import IOBinding
from idlelib.idle_test.mock_idle import Editor
from tkinter import Tk, Text
import tkinter
import os

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
        self.io_binding = IOBinding(self.editor)

    def tearDown(self):
        self.root.destroy()  # Destroy the Tkinter root window

    def test_toggle_highlight(self):
        start = '1.0'
        end = '2.0'
        color = "light blue"
        self.highlighter.toggle_highlight(color, start, end)

        #check if the selected region is correctly highlighted
        idx = start
        while idx != end:
            self.assertIn('highlight_light blue', self.text.tag_names(idx))
            idx = self.text.index('%s+1c' % idx)
        
        #simulate unhighlighting
        color = "white"
        self.highlighter.toggle_highlight(color)

        #check if the selected region is correctly unhighlighted
        idx = start
        while idx != end:
            self.assertNotIn('highlight_lightblue', self.text.tag_names(start))
            idx = self.text.index('%s+1c' % idx)
        
    #check if the highlighted region is still highlighted after reopens
    def test_highlight_reopen(self):
        pass
        # start = '1.0'
        # end = '2.0'
        # color = "light blue"
        # self.highlighter.toggle_highlight(color, start, end)

        # # Create a temporary file and save the contents of the text widget using IOBinding
        # temp_filename = "temp_highlight.txt"
        # self.io_binding.save(temp_filename)

        # # Close the temporary file
        # self.io_binding.close()

        # # Close the current text widget
        # self.root.destroy()

        # # Create a new text widget and load the contents from the temporary file
        # self.root = Tk()
        # self.root.withdraw()
        # self.text = Text(self.root)
        # self.text.load(temp_filename)

        # # Reinitialize the HighlightParagraph instance with the new text widget
        # self.editor = Editor(text=self.text)
        # self.highlighter = HighlightParagraph(self.editor)

        # # Verify that the highlighted region is still highlighted
        # idx = start
        # while idx != end:
        #     self.assertIn('highlight_light blue', self.text.tag_names(idx))
        #     idx = self.text.index('%s+1c' % idx)

        # # Clean up the temporary file
        # os.remove(temp_filename)

    #check if next_highlight is working correctly
    def test_next_highlight(self):
        start1 = '1.0'
        end1 = '2.0'
        color = "light blue"
        self.highlighter.toggle_highlight(color, start1, end1)

        start2 = '3.0'
        end2 = '4.0'
        color = "red"
        self.highlighter.toggle_highlight(color, start2, end2)

        event = tkinter.Event()
        event.widget = self.text
        self.highlighter.next_highlight(event)
        self.assertEqual(self.text.index("insert"), start1)

        
        # event2 = tkinter.Event()  # Create another event object
        # event2.widget = self.text
        # self.highlighter.next_highlight(event2)
        # self.assertEqual(self.text.index("insert"), start2)



        

        

if __name__ == '__main__':
    unittest.main()
