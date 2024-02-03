
import os
from PIL import Image
import customtkinter as ctk
from tkinter import messagebox
import connection_test
from mp import mpfshell
from tkinter import ttk
import tkinter as tk

# Constants and Configuration
TEST_MODE = False  # Set to True if testing without Abel TasTman connection
APP_TITLE = "TasTman Configuration Tool"
APP_GEOMETRY = "960x480"
WIFI_ADDRESS = 'ws:192.168.4.1, 123456'
IMAGE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        print('initializing')
        self.title(APP_TITLE)
        self.geometry(APP_GEOMETRY)

        self.shell = mpfshell.MpFileShell()
        if not TEST_MODE:
            self.check_wifi()
            self.shell.do_open(WIFI_ADDRESS)
            self.check_shell_connect()

        self.current_file_list = set()
        self.start_backend_loop()
        self.initialize_ui()
        self.select_frame_by_name("home")
        self.populate_file_explorer()
        self.font = ctk.CTkFont(family="Urbanist", size=14)

    def initialize_ui(self):
        self.load_images()
        self.create_navigation_frame()
        self.create_frames()

    def check_wifi(self):
        if not connection_test.is_wifi_connected(connection_test.get_wifi_ssid()):
            if not messagebox.askretrycancel("Error", "Please connect to Abel TasTman wifi first"):
                exit()

    def check_shell_connect(self):
        if not self.shell.do_check_connection():
            if not messagebox.askretrycancel("error", "Abel TasTman not connected"):
                exit()

    def check_connection(self):
        self.check_wifi()
        self.check_shell_connect()

    def load_images(self):
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(IMAGE_PATH, "logoSSS.png")), size=(26, 26))
        self.large_test_image = ctk.CTkImage(Image.open(os.path.join(IMAGE_PATH, "large_test_image.png")), size=(500, 150))
        self.home_image = ctk.CTkImage(light_image=Image.open(os.path.join(IMAGE_PATH, "home_dark.png")))
        self.chat_image = ctk.CTkImage(light_image=Image.open(os.path.join(IMAGE_PATH, "data_icon.png")), size=(20, 20))
        self.add_user_image = ctk.CTkImage(light_image=Image.open(os.path.join(IMAGE_PATH, "settings_icon.png")), size=(20, 20))

    def create_navigation_frame(self):
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
           # Configure the row weights of the parent to ensure the navigation frame takes full height
        self.grid_rowconfigure(0, weight=1)  # This makes the first row (where navigation_frame is) take full height

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="  Abel TasTman tool", image=self.logo_image,
                                                             compound="left", font=ctk.CTkFont(size=15, weight="bold", family='Urbanist'))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, font= ("Urbanist",14), anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Data",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, font= ("Urbanist",14), anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Configure",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, font= ("Urbanist",14), anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

    def create_frames(self):
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = ctk.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        # create second frame
        self.second_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid(row=0, column=1, sticky="nsew")  # Adjust grid settings for expansion
        self.grid_columnconfigure(1, weight=1)  # Allow the column to expand
        try:
            self.create_file_explorer()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file explorer: {e}")

        # create third frame
        self.third_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.third_frame.grid(row=0, column=2, sticky="nsew")
        self.grid_columnconfigure(2, weight=1)
        self.create_third_frame()
        #self.custombutton = ctk.CTkLabel(self.second_frame, text=self.shell.do_ls(''), text_color="#601E88", anchor="w", justify="left", font=("Urbanist", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))

    def create_third_frame(self):
        # SSID input field
        self.ssid_entry = ctk.CTkEntry(self.third_frame, placeholder_text="SSID")
        self.ssid_entry.grid(row=0, column=0, padx=10, pady=10)

        # Interval input field
        self.interval_var = tk.StringVar()
        vcmd = (self.register(self.validate_interval), "%P")
        self.interval_entry = ctk.CTkEntry(self.third_frame, placeholder_text="Interval", textvariable=self.interval_var, validate="key", validatecommand=vcmd)
        self.interval_entry.grid(row=1, column=0, padx=10, pady=10)

        # Label for displaying error message
        self.interval_error_label = ctk.CTkLabel(self.third_frame, text="")
        self.interval_error_label.grid(row=1, column=1, padx=10, pady=10)

        # Energy saving mode toggle
        self.energy_saving_mode = ctk.CTkSwitch(self.third_frame, text="Energy Saving Mode")
        self.energy_saving_mode.grid(row=2, column=0, padx=10, pady=10)

        # Save button
        self.save_button = ctk.CTkButton(self.third_frame, text="Save", command=self.save_configuration)
        self.save_button.grid(row=3, column=0, padx=10, pady=10)

    def validate_interval(self, P):
        is_valid = True
        if str.isdigit(P):
            try:
                print('intry', P)
                value = int(P)
                is_valid = 1 <= value <= 1000
            except ValueError:
                is_valid = False
        else:
            is_valid = False

        if P == '': #Check at save if any of the values is empty and notify that that is not allowed
            is_valid = True

        # Update error message label
        if not is_valid:
            self.interval_error_label.configure(text="Invalid number (0-1000 only)")
        else:
            self.interval_error_label.configure(text="")

        return is_valid

    def save_configuration(self):
        # Get values from UI components
        ssid = self.ssid_entry.get()
        interval = self.interval_entry.get()
        energy_mode = True if self.energy_saving_mode.get() else False

        # Write configuration to a file
        with open("configuration.txt", "w") as file:
            file.write(f"SSID: {ssid}\n")
            file.write(f"Interval: {interval}\n")
            file.write(f"Energy Saving Mode: {energy_mode}\n")

        messagebox.showinfo("Configuration Saved", "Your configuration has been saved successfully.")

    def create_file_explorer(self):
        # Create a Treeview widget
        self.tree = ttk.Treeview(self.second_frame)
        self.tree["columns"] = ("filename")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("filename", anchor=tk.W, width=120)
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("filename", text="Filename", anchor=tk.W)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.second_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        try:
            self.populate_file_explorer()
        except Exception as e:
            # Handle exceptions during file loading
            messagebox.showerror("Error", f"Failed to load files: {e}")


        # Add buttons for download and remove
        self.download_button = ctk.CTkButton(self.second_frame, text="Download", command=self.download_file)
        self.download_button.pack(pady=5)
        self.remove_button = ctk.CTkButton(self.second_frame, text="Remove", command=self.remove_file)
        self.remove_button.pack(pady=5)
        self.remove_button = ctk.CTkButton(self.second_frame, text="Refresh", command=self.populate_file_explorer)
        self.remove_button.pack(pady=5)

    def populate_file_explorer(self):
        try:
            self.shell.do_cd('database/')
            new_file_list = set(self.shell.do_ls(''))  # Getting the new file list
            new_file_list.remove('..')
        except Exception as e:
            print(f'Error fetching file list: {e}')
            new_file_list = set()

        added_files = new_file_list - self.current_file_list
        removed_files = self.current_file_list - new_file_list

        # Update tree if there are changes
        if added_files or removed_files:
            # Clear the tree and repopulate
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            for file in new_file_list:
                self.tree.insert("", tk.END, values=(file,))

            # Update the current file list
            self.current_file_list = new_file_list
        else:
            print("No changes in file list.")

    def download_file(self):
        selected_items = self.tree.selection()
        if selected_items:
            for item in selected_items:
                file_to_download = self.tree.item(item, 'values')[0]
                print(file_to_download)
                self.shell.do_get(file_to_download)
            # Code to handle file download
        self.populate_file_explorer()

    def remove_file(self):
        selected_items = self.tree.selection()
        if selected_items:
            if messagebox.askokcancel(title = 'Permanently delete?', message = 'Are you sure you want to delete the selected files?'):
                for item in selected_items:
                    file_to_remove = self.tree.item(item, 'values')[0]
                    print(file_to_remove)
                    self.shell.do_rm(file_to_remove)
            # Code to handle file removal
            #are you sure notification
        self.populate_file_explorer()

    def select_frame_by_name(self, name):
                # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def start_backend_loop(self):
        if not TEST_MODE:
            self.check_connection()

        self.after(2000, self.start_backend_loop)
    
    def closing(self):
        print('closing the program')
        self.shell.do_close('')

if __name__ == "__main__":
    app = App()
    app.mainloop()
    app.closing()
