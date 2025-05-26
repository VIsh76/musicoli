import requests
import urllib.parse
import json
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import time

def get_artists_by_genres0(include_tags, exclude_tags):
    """
    Pop genra until found 1
    """
    artists_data = _search_artists_by_genres(include_tags, exclude_tags)
    time.sleep(100)
    new_artists_data = []
    while len(exclude_tags) > 0 and len(new_artists_data)==0:
        excluded_element = exclude_tags.pop()
        artists_data.append([{"name": f"No Artist Found with excluded", "genres": [f"{excluded_element}"]}])
        new_artists_data = _search_artists_by_genres(include_tags, exclude_tags)
    
    artists_data += new_artists_data
    with open('datas/artists_data.json', 'w', encoding='utf-8') as f:
        json.dump(artists_data, f, indent=4, ensure_ascii=False)
    return artists_data


def get_artists_by_genres(include_tags, exclude_tags):
    """
    Try with no exclusion
    """
    artists_data = _search_artists_by_genres(include_tags, exclude_tags)
    print
    if len(artists_data)==0:
        time.sleep(1)
        artists_data.append({"name": f"No Artist Found with excluded", "genres": [f"{exclude_tags}"]})
        new_artists_data = _search_artists_by_genres(include_tags, [])
        if len(new_artists_data) > 0:
            artists_data += new_artists_data
        else:
            artists_data.append({"name": f"No Artist Found with only included genres", "genres": [f"{include_tags}"]})

    with open('datas/artists_data.json', 'w', encoding='utf-8') as f:
        json.dump(artists_data, f, indent=4, ensure_ascii=False)
    return artists_data


def _search_artists_by_genres(include_tags, exclude_tags):
    base_url = "https://musicbrainz.org/ws/2/artist"
    
    # Build query
    query_parts = []
    for tag in include_tags:
        query_parts.append(f"tag:{tag}")
    for tag in exclude_tags:
        query_parts.append(f"NOT tag:{tag}")
    
    query = " AND ".join(query_parts)
    encoded_query = urllib.parse.quote(query)

    url = f"{base_url}?query={encoded_query}&fmt=json&limit=100"
    headers = {
        "User-Agent": "MyGenreApp/1.0 ( your-email@example.com )"
    }
    
    response = requests.get(url, headers=headers)
    print("Request:", url)
    with open("datas/debug.txt", 'w') as f:
        f.write(url)
    response.raise_for_status()
    data = response.json()

    artists = []
    for artist in data.get("artists", []):
        tags = artist.get("tags", [])
        if not tags:
            continue  # Skip if no tags
        
        artist_genres = [tag["name"] for tag in tags]
        
        # Check if all include_tags are present in artist's genres
        if all(tag in artist_genres for tag in include_tags):
            artist_info = {
                "name": artist["name"],
                "genres": artist_genres
            }
            artists.append(artist_info)

    return artists

# Example usage

# ---- Tkinter UI to show JSON in a readable format ----

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json

def show_json_ui(artists_data):
    # Set up the main window
    root = tk.Tk()
    root.title("Artists Data Viewer")
    root.geometry("800x600")  # Make the window larger
    root.configure(bg="#f0f0f0")  # Set background color

    # Create a canvas for scrolling
    canvas = tk.Canvas(root, bg="#f0f0f0")
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create the frame where the artist data will go
    frame = ttk.Frame(canvas)#, bg="#f0f0f0")
    canvas.create_window((0, 0), window=frame, anchor="nw")

    # Create search bar for filtering artists and genres
    def filter_artists():
        search_query = search_entry.get().lower()
        # Clear current display
        for widget in frame.winfo_children():
            widget.destroy()

        # Display filtered artists
        for artist in artists_data:
            artist_name = artist["name"].lower()
            genres = ", ".join(artist["genres"]).lower()

            # Check if search query matches artist name or genre
            if search_query in artist_name or search_query in genres:
                # Artist name with nice font and color
                artist_label = tk.Label(frame, text=artist["name"], font=("Arial", 14, "bold"), fg="#1E90FF", anchor="w", bg="#f0f0f0")
                artist_label.pack(fill="x", padx=10, pady=5)

                # Genres on the same line with a lighter color
                genres_label = tk.Label(frame, text=genres, font=("Arial", 12), fg="#555555", anchor="w", bg="#f0f0f0")
                genres_label.pack(fill="x", padx=10, pady=2)

        # Update scrollbar
        canvas.config(scrollregion=canvas.bbox("all"))

    # Search bar for artist name or genre
    search_frame = ttk.Frame(root, padding=10)
    search_frame.pack(fill="x", padx=10, pady=5)
    
    search_label = ttk.Label(search_frame, text="Search (artist name or genre):", font=("Arial", 12), background="#f0f0f0")
    search_label.pack(side="left")

    search_entry = ttk.Entry(search_frame, font=("Arial", 12))
    search_entry.pack(side="left", expand=True, fill="x", padx=5)
    
    search_button = ttk.Button(search_frame, text="Search", command=filter_artists, width=10)
    search_button.pack(side="left")

    # Display all artists initially
    filter_artists()

    # Place canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Save button to save the data
    def save_json():
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(artists_data, f, indent=4, ensure_ascii=False)
            print(f"File saved to {file_path}")
    
    save_button = ttk.Button(root, text="Save JSON", command=save_json, width=20)
    save_button.pack(side="bottom", pady=10)
    # Start the GUI
    root.mainloop()

# Display the JSON data in a UI
if __name__ =='__main__':
    include = ["rock"]
    exclude = ["metal", "pop"]
    artists_data = _search_artists_by_genres(include, exclude)
    show_json_ui(artists_data)
