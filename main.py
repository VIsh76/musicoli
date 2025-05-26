from musicoli import TagSelector, ShowJSONUI, get_artists_by_genres
import tkinter as tk
import json


def launch_ui2(filepath="datas/_tmp.json"):
    # Hide UI1 window
    app1.save_preset(default=True)
    root_ui1.withdraw()

    # Create a new top-level window for UI2
    ui2_window = tk.Toplevel()

    def on_ui2_close():
        ui2_window.destroy()
        # Show back the UI1 main window
        root_ui1.deiconify()

    with open(filepath, 'r') as file:
        data = json.load(file)
        include = data['include']
        exclude = data['exclude']
    artists_data = get_artists_by_genres(include, exclude)
    ShowJSONUI(ui2_window, artists_data=artists_data,  on_close=on_ui2_close)

def main():
    global root_ui1, app1
    filepath =  "datas/_tmp.json"
    genre_txt_file = "datas/all_genre.txt"  # <-- Your file name here
    root_ui1 = tk.Tk()
    root_ui1.title("Select Genres")
    root_ui1.geometry("600x700")

    app1 = TagSelector(root_ui1, genre_txt_file, filepath)
    open_ui2_button = tk.Button(root_ui1, text="Search", command=launch_ui2)
    open_ui2_button.pack()
    root_ui1.mainloop()

if __name__ == "__main__":
    main()
