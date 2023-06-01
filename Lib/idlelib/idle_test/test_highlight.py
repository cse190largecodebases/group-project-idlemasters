import unittest
from tkinter import Tk
from idlelib.highlight import HighlightParagraph
from idlelib.idle_test.mock_idle import Editor, Func

class MockText:
    def __init__(self):
        self.index_calls = []

    def index(self, index):
        self.index_calls.append(index)
        line_number = int(index.split('.')[0])
        next_line_number = line_number + 1
        return f"{next_line_number}.0"


class Editor:
    def __init__(self, root):
        self.text = MockText()
        self.allow_highlight = True
        self.menudict = {}
        self.color_menu = {}


class HighlightParagraphTestCase(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.editor = Editor(self.root)
        self.highlighter = HighlightParagraph(self.editor)
        self.editor.menudict = {'edit': Func(return_self=True)}
        self.editor.color_menu = Func(return_self=True)

    def tearDown(self):
        self.root.destroy()

    def test_toggle_highlight(self):
        start, end = '1.0', '2.0'
        color = "light blue"
        self.editor.get_selection_indices = Func(result=(start, end))
        self.highlighter.toggle_highlight(color)
        self.assertEqual(self.editor.text.index_calls, ['1.0', '2.0', '3.0'])  # Verify the index calls
        self.assertEqual(self.editor.text.tag_add.called, 1)
        self.assertEqual(self.editor.text.tag_config.called, 1)

if __name__ == '__main__':
    unittest.main()
