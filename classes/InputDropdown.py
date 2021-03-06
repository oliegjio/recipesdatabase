from tkinter import *
from classes.BaseClass import *
from classes.CustomEntry import *

class InputDropdown(Frame, BaseClass):

    def __init__(self, parent, **kw):
        Frame.__init__(self, parent)
        BaseClass.__init__(self)

        self.parent = parent
        if kw['width']: self._width = kw['width']

        self._search_var = StringVar()
        self._search_var.trace('w', lambda name, index, mode: self._update_list())
        self._entry = CustomEntry(
            self,
            textvariable=self._search_var,
            width=self._width
        )
        self._entry.pack()
        self._entry.bind('<FocusIn>', self._entry_focus_in)
        self._entry.bind('<FocusOut>', self._focus_out)
        self._entry.bind('<Button-1>', self._focus_in)
        self.get_root().bind('<Button-1>', self._focus_out)

    def _update_list(self):
        search_term = self._search_var.get()
        
        listbox_data = ['Apple', 'Cake', 'Egg']

        self._listbox.delete(0, END)

        for item in listbox_data:
            if search_term.lower() in item.lower():
                self._listbox.insert(END, item)

    def _entry_focus_in(self, event):
        if getattr(self, '_listbox', False): return

        self._listbox = Listbox(
            self.get_root(),
            width=self._width,
            font=(self.default_font, 12)
        )
        self._listbox.bind('<<ListboxSelect>>', self._listbox_select)
        self._listbox.place(x=self.winfo_x() + 1, y=self.winfo_y() + 25)
        self._update_list()

    def _entry_focus_out(self, event):
        print('Focus out')
        if getattr(self, '_listbox', False) and (event.widget == self._entry or event.widget == self._listbox): return
        if getattr(self, '_listbox', False):
            self._destroy_list()
            self._entry_remove_focus()

    def _destroy_list(self):
        self._listbox.destroy()
        self._listbox = None

    def _entry_remove_focus(self):
        self.get_root().focus()

    def _listbox_select(self, event):
        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection[0])

        self._destroy_list()
