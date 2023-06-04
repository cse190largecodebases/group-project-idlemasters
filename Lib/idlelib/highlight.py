"""Format all or a selected region (line slice) of text.

Region formatting options: paragraph, comment block, indent, deindent,
comment, uncomment, tabify, and untabify.

File renamed from paragraph.py with functions added from editor.py.
"""
import re
import itertools

from tkinter.messagebox import askyesno
from tkinter.simpledialog import askinteger
from idlelib.config import idleConf

LIGHT_BLUE = "light blue"
LIGHT_RED = "#FF7F7F"
LIGHT_YELLOW = "#FFFFBF"
LIGHT_GREEN = "#88FF88"
LIGHT_ORANGE = "#FFBF80"
LIGHT_PURPLE = "#BF80FF"
UNHIGHLIGHT = "white"

class HighlightParagraph:

    def __init__(self, editwin):
        self.editwin = editwin
        self.privious_findNext = '0.0'
        # Define all highlight colors here
        self.all_colors = [LIGHT_BLUE, LIGHT_RED, LIGHT_YELLOW, LIGHT_GREEN, LIGHT_ORANGE, LIGHT_PURPLE, UNHIGHLIGHT]
        # Convert color names to valid tag names (no # sign)
        self.all_tags = ['highlight_' + color.replace('#', '') for color in self.all_colors]
        
    def create_color_menu(self):
        self.editwin.menudict['edit'].add_cascade(label="Highlight Line Region", menu=self.editwin.color_menu)
        if self.editwin.allow_highlight:
            self.editwin.color_menu.add_command(label="blue", command=lambda: self.toggle_highlight(LIGHT_BLUE))
            self.editwin.color_menu.add_command(label="red", command=lambda: self.toggle_highlight(LIGHT_RED))
            self.editwin.color_menu.add_command(label="yellow", command=lambda: self.toggle_highlight(LIGHT_YELLOW))
            self.editwin.color_menu.add_command(label="green", command=lambda: self.toggle_highlight(LIGHT_GREEN))
            self.editwin.color_menu.add_command(label="orange", command=lambda: self.toggle_highlight(LIGHT_ORANGE))
            self.editwin.color_menu.add_command(label="purple", command=lambda: self.toggle_highlight(LIGHT_PURPLE))
            self.editwin.color_menu.add_command(label="Unhighlight", command=lambda: self.toggle_highlight(UNHIGHLIGHT))
            self.editwin.text.bind("<<next-highlight>>", self.next_highlight)
            self.editwin.text.bind("<<find-first-highlight>>", self.find_first_highlight_event)
        else:
            self.editwin.update_menu_state('edit', "Highlight Line Region", 'disabled')
            self.editwin.update_menu_state('edit', "Find Next Highlight", 'disabled')
            self.editwin.update_menu_state('edit', "Find First Highlight", 'disabled')
    
    def find_first_highlight_event(self, event):
        self.privious_findNext = '0.0'
        self.next_highlight(None)
        return 'break'
        
    def next_highlight(self, event):
        # list to save the tag data
        tag_list = []
        
        # get all type of tag data
        for tag in self.all_tags:
            tag_range = list(self.editwin.text.tag_ranges(tag))
            tag_range_string = [str(element) for element in tag_range]
            tuple_tag = [(tag_range_string[i], tag_range_string[i+1]) for i in range(0, len(tag_range_string), 2)]
            tag_list.append(tuple_tag)
            
        combine_tag_list = sorted(list(itertools.chain.from_iterable(tag_list)), key=lambda x: (int(x[0].split('.')[0]), int(x[0].split('.')[1])))
        
        
        next_tag = None
        # find the next tag
        for tag in combine_tag_list:
            row = int(tag[0].split('.')[0])
            col = int(tag[0].split('.')[1])
            if row == int(self.privious_findNext.split('.')[0]) and col > int(self.privious_findNext.split('.')[1]):
                next_tag = tag[0]
                break
            elif row > int(self.privious_findNext.split('.')[0]):
                next_tag = tag[0]
                break
        # if reach to the end, go to the first tag
        if next_tag == None:
            next_tag = combine_tag_list[0][0]
            
        
        self.editwin.text.tag_remove("sel", "1.0", "end")
        self.editwin.text.mark_set("insert", next_tag)
        self.editwin.text.see("insert")
        self.editwin.set_line_and_column()
        self.privious_findNext = next_tag
        return 'break'
    
    def toggle_highlight(self, color):
        # get the selected region
        start, end = self.editwin.get_selection_indices()
        if start and end:
            # Create unique tag for each color
            color_tag = 'highlight_' + color.replace('#', '')
            
            # Iterate over all text in selected region
            idx = start
            while idx != end:
                # Get all tags at this index
                tags = self.editwin.text.tag_names(idx)
                
                # If there is a highlight tag, remove it
                for tag in tags:
                    if tag in self.all_tags:
                        self.editwin.text.tag_remove(tag, idx)
                
                # Move to next character
                idx = self.editwin.text.index(f"{idx}+1c")
            
            # Add the new highlight tag to the selected region
            self.editwin.text.tag_add(color_tag, start, end)
            self.editwin.text.tag_config(color_tag, background=color)
            if color == "white":
                self.editwin.text.tag_remove(color_tag, start, end)
            self.editwin.text.tag_raise("sel")
        return "break"




