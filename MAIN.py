import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import MyParser


def popup_window(in_text):
    window = tk.Toplevel()

    label = tk.Label(window, text=in_text)
    label.pack(fill='x', padx=150, pady=55)

    button_close = tk.Button(window, text="OK!", command=window.destroy)
    button_close.pack(fill='x')

    
def open_file():
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete(1.0, tk.END)
    with open(filepath, "r") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    window.title(f"Executor - {filepath}")

def save_file():
    """Save the current file as a new file."""
    filepath = asksaveasfilename(
        defaultextension="txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = txt_edit.get(1.0, tk.END)
        output_file.write(text)
    window.title(f"Executor- {filepath}")

def RUN():
    text = txt_edit.get(1.0, tk.END)
    
    text=text.replace('\n',' ')
    text=text[:-1]
    print('Running following:',text)
    interpreter=MyParser.INTERPRET(text)
    
    ret = MyParser.RUN_PROGRAM(interpreter)
    final_string=""
    for txt in ret:
        final_string=str(final_string)+str(txt)+"\n"
        
    popup_window(str(final_string))
    
    
window = tk.Tk()
window.title("Executor")
window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

txt_edit = tk.Text(window)
fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
btn_open = tk.Button(fr_buttons, text="Open", command=open_file)
btn_save = tk.Button(fr_buttons, text="Save", command=save_file)
btn_run = tk.Button(fr_buttons, text="Run", command=RUN)

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5)
btn_run.grid(row=2, column=0, sticky="ew", padx=5)

fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")

window.mainloop()
