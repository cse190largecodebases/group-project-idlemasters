"""Format all or a selected region (line slice) of text.

Region formatting options: paragraph, comment block, indent, deindent,
comment, uncomment, tabify, and untabify.

File renamed from paragraph.py with functions added from editor.py.
"""
import re
from tkinter.messagebox import askyesno
from tkinter.simpledialog import askinteger
from idlelib.config import idleConf


class HighlightParagraph:
    def __init__(self, editwin):
        self.editwin = editwin
        
    def create_color_menu(self):
        self.editwin.menudict['edit'].add_cascade(label="Highlight Line Region", menu=self.editwin.color_menu)
        self.editwin.color_menu.add_command(label="blue", command=lambda: self.toggle_highlight("light blue"))
        self.editwin.color_menu.add_command(label="red", command=lambda: self.toggle_highlight("#FF7F7F"))
        self.editwin.color_menu.add_command(label="yellow", command=lambda: self.toggle_highlight("#FFFFBF"))
        self.editwin.color_menu.add_command(label="green", command=lambda: self.toggle_highlight("#88FF88"))
        self.editwin.color_menu.add_command(label="orange", command=lambda: self.toggle_highlight("#FFBF80"))
        self.editwin.color_menu.add_command(label="purple", command=lambda: self.toggle_highlight("#BF80FF"))
        self.editwin.color_menu.add_command(label="Unhighlight", command=lambda: self.toggle_highlight("white"))
    
    
    def toggle_highlight(self, color):
        # get the selected region
        start, end = self.editwin.get_selection_indices()
        if start and end:
            self.editwin.text.tag_add('highlight', start, end)
            self.editwin.text.tag_config('highlight', background=color)
            return "break"
        else:
            return "break"