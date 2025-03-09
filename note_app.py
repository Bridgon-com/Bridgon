import tkinter as tk
from tkinter import filedialog, messagebox

def save_note():
    text = text_area.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Warning", "Note is empty!")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text)
        messagebox.showinfo("Success", "Note saved successfully!")

def load_note():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, file.read())

def clear_note():
    text_area.delete("1.0", tk.END)

# Initialize main window
root = tk.Tk()
root.title("Simple Note-Taking App")
root.geometry("400x500")

# UI Elements
text_area = tk.Text(root, wrap="word", font=("Arial", 12))
text_area.pack(expand=True, fill="both", padx=10, pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=5)

save_button = tk.Button(button_frame, text="Save", command=save_note)
save_button.pack(side=tk.LEFT, padx=5)

load_button = tk.Button(button_frame, text="Load", command=load_note)
load_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(button_frame, text="Clear", command=clear_note)
clear_button.pack(side=tk.LEFT, padx=5)

# Run the application
root.mainloop()