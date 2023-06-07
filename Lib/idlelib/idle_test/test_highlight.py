import unittest
from idlelib.highlight import HighlightParagraph
from idlelib.iomenu import IOBinding
from idlelib.idle_test.mock_idle import Editor
from idlelib.filelist import FileList
from tkinter import Tk, Text
import json
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
        # mock the flist
        self.editor.flist = FileList(self.root)
        self.editor.flist.dict['test'] = self.editor
        

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
            self.assertNotIn('highlight_light blue', self.text.tag_names(start))
            idx = self.text.index('%s+1c' % idx)
        
    #check if the highlighted region is still highlighted after reopens
    def test_highlight_save(self):
        start = '1.0'
        end = '2.0'
        color = "light blue"
        self.highlighter.toggle_highlight(color, start, end)
        self.highlighter.save_highlight("test")
        
        # the data path for jason file 
        file_path = "data.json"  
        
        # read the json file 
        with open(file_path, 'r') as file:
            data = json.load(file)

        right_tag_list = [['1.0', '2.0'], [], [], [], [], [], []]
        self.assertEqual(data["test"], right_tag_list)
    
    
    def test_highlight_reopen(self):  
        start = '1.0'
        end = '2.0'
        #check if the selected region is correctly unhighlighted
        idx = start
        while idx != end:
            self.assertNotIn('highlight_light blue', self.text.tag_names(start))
            idx = self.text.index('%s+1c' % idx)
            
        # reload the highlight
        self.highlighter.reload_highlight("test")
        
        #check if the selected region is correctly highlighted
        idx = start
        while idx != end:
            self.assertIn('highlight_light blue', self.text.tag_names(idx))
            idx = self.text.index('%s+1c' % idx)
        

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
