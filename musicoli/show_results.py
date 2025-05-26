import tkinter as tk
from tkinter import ttk
import webbrowser


class ShowJSONUI:
    def __init__(self, master, artists_data, on_close=None):
        self.master = master
        self.artists_data = artists_data
        self.on_close = on_close

        self.master.title("Artist Viewer")

        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', self.update_display)

        self.search_entry = tk.Entry(self.master, textvariable=self.search_var, font=("Arial", 14))
        self.search_entry.pack(fill="x", padx=10, pady=10)

        self.frame = tk.Frame(self.master)
        self.frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.frame)
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.display_artists()

        self.master.protocol("WM_DELETE_WINDOW", self.handle_close)

    def display_artists(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        search_text = self.search_var.get().lower()

        for artist in self.artists_data:
            artist_name = artist["name"]
            artist_genres = ", ".join(artist["genres"])

            if search_text in artist_name.lower() or any(search_text in genre.lower() for genre in artist["genres"]):
                # Artist name with nice font and color
                artist_label = tk.Label(self.scrollable_frame, text=artist["name"], font=("Arial", 14, "bold"), fg="#1E90FF", anchor="w", bg="#f0f0f0")
                artist_label.pack(fill="x", padx=10, pady=5)

                # Genres on the same line with a lighter color
                genres_label = tk.Label(self.scrollable_frame, text=artist_genres, font=("Arial", 12), fg="#555555", anchor="w", bg="#f0f0f0")
                genres_label.pack(fill="x", padx=10, pady=2)

                artist_label.bind("<Button-1>", lambda e, name=artist_name: self.open_google(name))


    def open_google(self, artist_name):
        query = f"{artist_name} music"
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open_new_tab(url)

    def update_display(self, *args):
        self.display_artists()

    def handle_close(self):
        if self.on_close:
            self.on_close()
        self.master.destroy()


import tkinter as tk

def main():
    root = tk.Tk()

    # Example data
    artists_data = [
        {"name": "Band A", "genres": ["rock", "indie"]},
        {"name": "Band B", "genres": ["metal", "rock"]},
        {"name": "Band C", "genres": ["pop", "dance"]},
    ]

    app = ShowJSONUI(root, artists_data)
    root.mainloop()

if __name__ == "__main__":
    main()
