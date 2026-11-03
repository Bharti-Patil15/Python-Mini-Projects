
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, font
from datetime import datetime

current_file = None
is_dirty = False
dark_mode = False


def new_file():
    if check_unsaved():
        text.delete(1.0, tk.END)
        root.title("Simple Text Editor")


def open_file():
    if not check_unsaved():
        return

    file_path = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )

    if file_path:
        try:
            with open(file_path, 'r', encoding="utf-8") as file:
                content = file.read()

            text.delete(1.0, tk.END)
            text.insert(tk.END, content)

            global current_file, is_dirty
            current_file = file_path
            is_dirty = False
            text.edit_modified(False)
            root.title("Simple Text Editor")
            update_count()

        except OSError as error:
            messagebox.showerror("Error", str(error))


def save_file():
    global current_file, is_dirty

    if current_file is None:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )

        if not file_path:
            return False

        current_file = file_path

    try:
        with open(current_file, 'w', encoding="utf-8") as file:
            file.write(text.get(1.0, "end-1c"))

        is_dirty = False
        root.title("Simple Text Editor")
        messagebox.showinfo("Save File", "File saved successfully!")
        return True

    except OSError as error:
        messagebox.showerror("Error", str(error))
        return False


def save_as():
    global current_file

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )

    if file_path:
        current_file = file_path
        return save_file()

    return False


def check_unsaved():
    if is_dirty:
        answer = messagebox.askyesnocancel(
            "Unsaved Changes",
            "Do you want to save your changes?"
        )

        if answer is True:
            return save_file()
        elif answer is False:
            return True
        else:
            return False

    return True


def undo():
    try:
        text.edit_undo()
    except tk.TclError:
        pass


def redo():
    try:
        text.edit_redo()
    except tk.TclError:
        pass


def find_replace():
    window = tk.Toplevel(root)
    window.title("Find and Replace")
    window.geometry("350x200")

    tk.Label(window, text="Find Word").pack()

    find_entry = tk.Entry(window)
    find_entry.pack(pady=5)

    tk.Label(window, text="Replace With").pack()

    replace_entry = tk.Entry(window)
    replace_entry.pack(pady=5)

    def find_word():
        word = find_entry.get()
        text.tag_remove("found", "1.0", tk.END)

        if not word:
            return

        start = "1.0"

        while True:
            position = text.search(word, start, tk.END)

            if not position:
                break

            end = f"{position}+{len(word)}c"
            text.tag_add("found", position, end)
            start = end

        text.tag_config("found", background="yellow", foreground="black")

    def replace_word():
        old_word = find_entry.get()
        new_word = replace_entry.get()

        if not old_word:
            return

        content = text.get("1.0", "end-1c")
        new_content = content.replace(old_word, new_word)

        text.delete("1.0", tk.END)
        text.insert("1.0", new_content)
        text.tag_remove("found", "1.0", tk.END)

    tk.Button(window, text="Find", command=find_word).pack(pady=3)
    tk.Button(window, text="Replace All", command=replace_word).pack(pady=3)


def toggle_dark_mode():
    global dark_mode

    dark_mode = not dark_mode

    if dark_mode:
        text.config(bg="#1e1e1e", fg="white", insertbackground="white")
        root.config(bg="#333333")
        status.config(bg="#333333", fg="white")
    else:
        text.config(bg="white", fg="black", insertbackground="black")
        root.config(bg="SystemButtonFace")
        status.config(bg="SystemButtonFace", fg="black")


def update_count():
    content = text.get("1.0", "end-1c")

    words = len(content.split())
    characters = len(content)

    status.config(text=f"Words: {words} | Characters: {characters}")


def change_font_size():
    size = simpledialog.askinteger(
        "Font Size",
        "Enter font size:",
        minvalue=6,
        maxvalue=72
    )

    if size:
        text.config(font=("Arial", size))


def toggle_bold():
    current = font.Font(font=text["font"])
    current.configure(
        weight="bold" if current.actual("weight") == "normal" else "normal"
    )
    text.config(font=current)


def toggle_italic():
    current = font.Font(font=text["font"])
    current.configure(
        slant="italic" if current.actual("slant") == "roman" else "roman"
    )
    text.config(font=current)


def toggle_underline():
    current = font.Font(font=text["font"])
    current.configure(underline=not current.actual("underline"))
    text.config(font=current)


def insert_datetime():
    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    text.insert(tk.INSERT, current_time)


def auto_save():
    global is_dirty

    if current_file is not None and is_dirty:
        try:
            with open(current_file, 'w', encoding="utf-8") as file:
                file.write(text.get("1.0", "end-1c"))

            is_dirty = False
            root.title("Simple Text Editor")
            status.config(text="Auto Saved Successfully")

        except OSError:
            status.config(text="Auto Save Failed")

    root.after(30000, auto_save)


def on_text_change(event=None):
    global is_dirty

    if text.edit_modified():
        is_dirty = True
        root.title("Simple Text Editor *")
        update_count()
        text.edit_modified(False)


def exit_editor():
    if check_unsaved():
        root.destroy()


root = tk.Tk()
root.title("Simple Text Editor")
root.geometry("800x600")

menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_editor)

edit_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Edit", menu=edit_menu)

edit_menu.add_command(label="Undo", command=undo)
edit_menu.add_command(label="Redo", command=redo)
edit_menu.add_separator()

edit_menu.add_command(
    label="Cut",
    command=lambda: text.event_generate("<<Cut>>")
)

edit_menu.add_command(
    label="Copy",
    command=lambda: text.event_generate("<<Copy>>")
)

edit_menu.add_command(
    label="Paste",
    command=lambda: text.event_generate("<<Paste>>")
)

edit_menu.add_separator()
edit_menu.add_command(label="Find and Replace", command=find_replace)

view_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="View", menu=view_menu)

view_menu.add_command(label="Dark Mode", command=toggle_dark_mode)

format_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Format", menu=format_menu)

format_menu.add_command(label="Font Size", command=change_font_size)
format_menu.add_command(label="Bold", command=toggle_bold)
format_menu.add_command(label="Italic", command=toggle_italic)
format_menu.add_command(label="Underline", command=toggle_underline)

insert_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Insert", menu=insert_menu)

insert_menu.add_command(label="Date and Time", command=insert_datetime)

text = tk.Text(
    root,
    wrap=tk.WORD,
    font=("Arial", 12),
    fg="black",
    bg="white",
    undo=True
)

text.pack(expand=True, fill=tk.BOTH)

status = tk.Label(
    root,
    text="Words: 0 | Characters: 0",
    anchor="w",
    relief=tk.SUNKEN
)

status.pack(side=tk.BOTTOM, fill=tk.X)

text.bind("<<Modified>>", on_text_change)

root.bind("<Control-n>", lambda event: new_file())
root.bind("<Control-o>", lambda event: open_file())
root.bind("<Control-s>", lambda event: save_file())
root.bind("<Control-Shift-S>", lambda event: save_as())
root.bind("<Control-z>", lambda event: undo())
root.bind("<Control-y>", lambda event: redo())
root.bind("<Control-f>", lambda event: find_replace())
root.bind("<Control-b>", lambda event: toggle_bold())
root.bind("<Control-i>", lambda event: toggle_italic())

root.after(30000, auto_save)

root.protocol("WM_DELETE_WINDOW", exit_editor)

root.mainloop()
