import tkinter as tk
from tkinter import ttk, filedialog
import json

class TagSelector:
    def __init__(self, master, genre_file, default_filepath):
        self.master = master
        self.default_filepath = default_filepath
        self.all_tags = self.load_tags_from_file(genre_file)
        self.all_tags = sorted(self.all_tags, key=len)
        self.filtered_tags = self.all_tags.copy()

        self.include_vars = {}
        self.exclude_vars = {}

        self.create_widgets()

    def load_tags_from_file(self, path):
        with open(path, 'r') as f:
            tags = [line.strip() for line in f if line.strip()]
        return tags

    def create_widgets(self):
        # Search bar
        search_frame = ttk.Frame(self.master)
        search_frame.pack(fill='x', padx=5, pady=5)

        search_label = ttk.Label(search_frame, text="Search Tags:")
        search_label.pack(side="left")

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side="left", fill="x", expand=True, padx=5)
        search_entry.bind("<KeyRelease>", self.update_filter)

        # Scrollable area
        frame = ttk.Frame(self.master)
        frame.pack(fill='both', expand=True)

        self.canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Control buttons
        button_frame = ttk.Frame(self.master)
        button_frame.pack(fill='x', pady=5)

        ttk.Button(button_frame, text="Select All Include", command=self.select_all_include).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear All", command=self.clear_all).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Save Preset", command=self.save_preset).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Load Preset", command=self.load_preset).pack(side="left", padx=5)

        #ttk.Button(self.master, text="Save Search", command=self.submit).pack(pady=10)

        # Draw initial tag list
        self.draw_tag_list()

    def draw_tag_list(self):
        # Clear old widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Step 1: Always show selected tags (include or exclude)
        selected_tags = [
            tag for tag in self.all_tags
            if self.include_vars.get(tag, tk.BooleanVar()).get() or
               self.exclude_vars.get(tag, tk.BooleanVar()).get()
        ]

        # Step 2: Then show search results (but max 10)
        search_text = self.search_var.get().lower()
        search_matches = [
                tag for tag in self.all_tags
                if search_text in tag.lower() and tag not in selected_tags]
        search_matches = search_matches[:20]

        # Final list to display
        display_tags = selected_tags + search_matches

        for tag in display_tags:
            include_var = self.include_vars.get(tag, tk.BooleanVar())
            exclude_var = self.exclude_vars.get(tag, tk.BooleanVar())
            self.include_vars[tag] = include_var
            self.exclude_vars[tag] = exclude_var

            row = ttk.Frame(self.scrollable_frame)
            row.pack(fill='x', pady=2)

            label = ttk.Label(row, text=tag, width=30, anchor="w")
            label.pack(side="left")

            include_cb = ttk.Checkbutton(
                row, text="Include", variable=include_var,
                command=lambda t=tag: self.on_include(t)
            )
            include_cb.pack(side="left")

            exclude_cb = ttk.Checkbutton(
                row, text="Exclude", variable=exclude_var,
                command=lambda t=tag: self.on_exclude(t)
            )
            exclude_cb.pack(side="left")


    def on_include(self, tag):
        if self.include_vars[tag].get():
            self.exclude_vars[tag].set(False)

    def on_exclude(self, tag):
        if self.exclude_vars[tag].get():
            self.include_vars[tag].set(False)

    def update_filter(self, event=None):
        search_text = self.search_var.get().lower()
        self.filtered_tags = [tag for tag in self.all_tags if search_text in tag.lower()]
        self.draw_tag_list()

    def select_all_include(self):
        for tag in self.all_tags:
            self.include_vars[tag].set(True)
            self.exclude_vars[tag].set(False)

    def clear_all(self):
        for tag in self.all_tags:
            self.include_vars[tag].set(False)
            self.exclude_vars[tag].set(False)

    def save_preset(self, default=False):
        include_tags = [tag for tag, var in self.include_vars.items() if var.get()]
        exclude_tags = [tag for tag, var in self.exclude_vars.items() if var.get()]
        preset = {
            "include": include_tags,
            "exclude": exclude_tags
        }
        if default:
            file_path = self.default_filepath
        else:
            file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(preset, f, indent=4)
            print(f"Preset saved to {file_path}")

    def load_preset(self, ask):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, 'r') as f:
                preset = json.load(f)
            self.clear_all()
            for tag in preset.get("include", []):
                if tag in self.include_vars:
                    self.include_vars[tag].set(True)
            for tag in preset.get("exclude", []):
                if tag in self.exclude_vars:
                    self.exclude_vars[tag].set(True)
            print(f"Preset loaded from {file_path}")

    def submit(self):
        include_tags = [tag for tag, var in self.include_vars.items() if var.get()]
        exclude_tags = [tag for tag, var in self.exclude_vars.items() if var.get()]
        print("Include:", include_tags)
        print("Exclude:", exclude_tags)
        self.save_preset(default=True)
        #self.master.quit()
        #return include_tags, exclude_tags

# Example usage
if __name__ == "__main__":
    filepath =  "datas/_tmp.json"
    genre_txt_file = "all_genre.txt"  # <-- Your file name here
    root = tk.Tk()
    root.title("Select Genres")
    root.geometry("600x700")
    app = TagSelector(root, genre_txt_file, filepath)
    root.mainloop()
    with open(filepath, 'r') as file:
        data = json.load(file)
        includes = data['include']
        excludes = data['exclude']



