import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import datetime
import json

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("600x400")
        self.title('Notebook')
        self.notebook = []

        self.frame_main = tk.Frame(self)
        self.frame_main.pack(fill=tk.BOTH, expand=True)
        self.frame_main.config(bg='light gray')

        self.frame_notes = tk.Frame(self.frame_main)
        self.frame_notes.grid(row=1, column=3, rowspan=6, sticky='w')
        self.frame_notes.config(bg='gray') 
        
        tk.Button(self.frame_main, text='Create New Note', command=self.new_note).grid(padx=10, pady=10, row=1, column=1)
        tk.Button(self.frame_main, text='Open Notebook', command=self.open_notebook).grid(padx=10, pady=10, row=2, column=1)
        tk.Button(self.frame_main, text='Save Notebook\nand Refresh', command=self.save_notebook).grid(padx=10, pady=10, row=3, column=1)
        tk.Button(self.frame_main, text='Quit', command=self.destroy).grid(padx=10, pady=10, row=4, column=1)

    def new_note(self):
        NoteEdit(self, self.notebook, new=True)

    def clear_frame(self, target_frame):
        for widgets in target_frame.winfo_children():
            widgets.destroy()

    def show_notes(self):
        self.clear_frame(self.frame_notes)
        for note in self.notebook:
            new_note = MakeNote(master=self.frame_notes, note_dict=note, main_window=self)
            new_note.pack(padx=10, pady=10)
            new_note.config(height=3, width=40, wraplength=200, justify=tk.LEFT)

    def open_notebook(self):
        filepath = filedialog.askopenfilename(filetypes=[("json files", "*.json"), ("all files", "*.*")])
        with open(filepath, "r") as file:
            self.notebook = json.load(file)
        self.show_notes()

    def save_notebook(self):
        file = filedialog.asksaveasfile(defaultextension=".json", filetypes=[("json file", ".json")])
        json_out = json.dumps(self.notebook, indent=2)
        file.write(json_out)
        file.close()
        self.show_notes()

class NoteEdit(tk.Toplevel):
    def __init__(self, master, notebook, new=True, note_dict=None):
        super().__init__(master)
        self.geometry("600x400")
        self.title('Edit Note' if not new else 'New Note')
        self.frame_main = tk.Frame(self)
        self.frame_main.pack(fill=tk.BOTH, expand=True)
        self.frame_main.config(bg='light gray')

        self.notebook = notebook
        self.note_dict = note_dict if note_dict else {"title": "", "text": "", "code snippet": "", "link": "", "tags": "", "meta": ""}
        
        tk.Label(self.frame_main, text='Note Title:').grid(padx=10, pady=10, row=1, column=0, sticky='e')
        self.note_title = tk.Entry(self.frame_main, width=80)
        self.note_title.grid(padx=10, pady=10, row=1, column=1, sticky='w')
        self.note_title.insert(0, self.note_dict["title"])

        tk.Label(self.frame_main, text='Note Text:').grid(padx=10, pady=10, row=2, column=0, sticky='e')
        self.note_text = tk.Text(self.frame_main, height=5, width=60)
        self.note_text.grid(padx=10, pady=10, row=2, column=1)
        self.note_text.insert('1.0', self.note_dict["text"])

        tk.Label(self.frame_main, text='Code Snippet:').grid(padx=10, pady=10, row=3, column=0, sticky='e')
        self.note_snippet = tk.Text(self.frame_main, height=5, width=60)
        self.note_snippet.grid(padx=10, pady=10, row=3, column=1, sticky='w')
        self.note_snippet.insert('1.0', self.note_dict["code snippet"])

        tk.Label(self.frame_main, text='Note Link:').grid(padx=10, pady=10, row=4, column=0, sticky='e')
        self.note_link = tk.Entry(self.frame_main, width=80)
        self.note_link.grid(padx=10, pady=10, row=4, column=1, sticky='w')
        self.note_link.insert(0, self.note_dict["link"])

        tk.Label(self.frame_main, text='Note Tags:').grid(padx=10, pady=10, row=5, column=0, sticky='e')
        self.note_tags = tk.Entry(self.frame_main, width=80)
        self.note_tags.grid(padx=10, pady=10, row=5, column=1, sticky='w')
        self.note_tags.insert(0, self.note_dict["tags"])

        tk.Button(self.frame_main, text='Submit', command=self.submit).grid(padx=10, pady=10, row=6, column=1, sticky='w')
        tk.Button(self.frame_main, text='Close', command=self.destroy).grid(padx=10, pady=10, row=6, column=0)

    def submit(self):
        now = datetime.datetime.now()
        meta = f'Edited on {now.strftime("%Y-%m-%d %H:%M:%S")}'
        note = {
            "title": self.note_title.get(),
            "text": self.note_text.get("1.0", tk.END).strip(),
            "code snippet": self.note_snippet.get("1.0", tk.END).strip(),
            "link": self.note_link.get(),
            "tags": self.note_tags.get(),
            "meta": meta
        }

        if self.note_dict in self.notebook:
            self.notebook[self.notebook.index(self.note_dict)] = note
        else:
            self.notebook.append(note)

        self.master.show_notes()
        self.destroy()

class MakeNote(tk.Button):
    def __init__(self, master, note_dict, main_window):
        super().__init__(master, text=f"{note_dict['title']}\n{note_dict['meta']}", command=lambda: self.open_note(note_dict, main_window))
        self.note_dict = note_dict
        self.main_window = main_window

    def open_note(self, note_dict, main_window):
        NoteEdit(main_window, main_window.notebook, new=False, note_dict=note_dict)

if __name__ == '__main__':
    main_window = MainWindow()
    main_window.mainloop()