import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import threading
from transcript import download_transcript


def generate():
    url = url_entry.get().strip()
    if not url:
        return

    btn.config(state="disabled")
    text_area.delete("1.0", tk.END)
    text_area.insert(tk.END, "Fetching transcript...")

    mode = mode_var.get()
    include_timestamps = mode == "With Timestamps"
    sentences = mode == "Sentences"

    def fetch():
        try:
            result = download_transcript(url, include_timestamps, sentences)
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, result)
        except Exception as e:
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, f"Error: {e}")
        finally:
            btn.config(state="normal")

    threading.Thread(target=fetch, daemon=True).start()


def save_to_file():
    content = text_area.get("1.0", tk.END).strip()
    if not content:
        return
    path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
    )
    if path:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)


root = tk.Tk()
root.title("YouTube Transcript Downloader")
root.geometry("800x600")
root.minsize(600, 400)

frame = ttk.Frame(root, padding=10)
frame.pack(fill="x")

ttk.Label(frame, text="YouTube URL:").pack(side="left")
url_entry = ttk.Entry(frame)
url_entry.pack(side="left", fill="x", expand=True, padx=(5, 5))

mode_var = tk.StringVar(value="Sentences")
mode_dropdown = ttk.Combobox(frame, textvariable=mode_var, state="readonly", width=18,
                             values=["With Timestamps", "No Timestamps", "Sentences"])
mode_dropdown.pack(side="left", padx=(0, 5))

btn = ttk.Button(frame, text="Generate", command=generate)
btn.pack(side="left", padx=(0, 5))

save_btn = ttk.Button(frame, text="Save to File", command=lambda: save_to_file())
save_btn.pack(side="left")

text_area = tk.Text(root, wrap="word", padx=10, pady=10)
text_area.pack(fill="both", expand=True, padx=10, pady=(0, 10))

scrollbar = ttk.Scrollbar(text_area, command=text_area.yview)
scrollbar.pack(side="right", fill="y")
text_area.config(yscrollcommand=scrollbar.set)

root.mainloop()
