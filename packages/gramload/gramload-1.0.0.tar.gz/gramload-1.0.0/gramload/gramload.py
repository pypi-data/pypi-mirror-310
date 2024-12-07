import instaloader
import time
from random import randint
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
import os
import json
import threading
import sys

cancel_download = False

def download_profile_with_delay(username, dirname, login_user=None, login_pass=None):
    global cancel_download
    L = instaloader.Instaloader()
    L.dirname_pattern = f"{dirname}/{username}"
    
    if login_user and login_pass:
        try:
            L.login(login_user, login_pass)
            print("Logged in successfully")
            root.after(0, status_label.config, {"text": "Logged in successfully"})
        except instaloader.exceptions.BadCredentialsException:
            root.after(0, messagebox.showerror, "Login Error", "Invalid login credentials")
            root.after(0, status_label.config, {"text": "Invalid login credentials"})
            return
        except instaloader.exceptions.TwoFactorAuthRequiredException:
            root.after(0, messagebox.showerror, "Login Error", "Two-factor authentication required")
            root.after(0, status_label.config, {"text": "Two-factor authentication required"})
            return
        except instaloader.exceptions.ConnectionException as e:
            root.after(0, messagebox.showerror, "Login Error", f"Connection error: {e}")
            root.after(0, status_label.config, {"text": f"Connection error: {e}"})
            return
        except instaloader.exceptions.InstaloaderException as e:
            root.after(0, messagebox.showerror, "Login Error", f"Instaloader error: {e}")
            root.after(0, status_label.config, {"text": f"Instaloader error: {e}"})
            return

    try:
        print(f"Preparing to download profile: {username}")
        root.after(0, status_label.config, {"text": f"Preparing to download profile: {username}"})
        
        profile = instaloader.Profile.from_username(L.context, username)
        posts = list(profile.get_posts())
        root.after(0, progress_bar.config, {"maximum": len(posts)})
        
        for index, post in enumerate(posts):
            if cancel_download:
                root.after(0, messagebox.showinfo, "Cancelled", "Download cancelled")
                root.after(0, status_label.config, {"text": "Download cancelled"})
                root.after(0, progress_bar.config, {"value": 0})
                return
            if post.typename == 'GraphImage' or post.typename == 'GraphVideo':
                print(f"Downloading post {index + 1}/{len(posts)}")
                root.after(0, status_label.config, {"text": f"Downloading post {index + 1}/{len(posts)}"})
                L.download_post(post, target=profile.username)
                time.sleep(randint(1, 5))
            root.after(0, progress_bar.config, {"value": index + 1})
        
        root.after(0, messagebox.showinfo, "Success", f"Downloaded profile: {username}")
        root.after(0, status_label.config, {"text": f"Downloaded profile: {username}"})
    except instaloader.exceptions.ConnectionException as e:
        print(f"Connection error: {e}")
        root.after(0, status_label.config, {"text": f"Connection error: {e}"})
        time.sleep(60)  
        download_profile_with_delay(username, dirname, login_user, login_pass)
    except instaloader.exceptions.LoginRequiredException:
        root.after(0, messagebox.showerror, "Login Error", "Login required. Please provide login credentials.")
        root.after(0, status_label.config, {"text": "Login required. Please provide login credentials."})
    except instaloader.exceptions.InstaloaderException as e:
        print(f"Instaloader error: {e}")
        root.after(0, messagebox.showerror, "Error", f"Instaloader error: {e}")
        root.after(0, status_label.config, {"text": f"Error: {e}"})

def start_download():
    global cancel_download
    cancel_download = False
    username = entry_username.get()
    dirname = entry_dir.get()
    login_user = entry_login_user.get()
    login_pass = entry_login_pass.get()

    if not username or not dirname:
        messagebox.showerror("Input Error", "Username and destination directory are required")
        return

    with open('config.json', 'w') as config_file:
        json.dump({'last_dir': dirname, 'last_username': login_user, 'last_password': login_pass}, config_file)

    threading.Thread(target=download_profile_with_delay, args=(username, dirname, login_user, login_pass)).start()

def cancel_download_process():
    global cancel_download
    cancel_download = True
    root.after(0, progress_bar.config, {"value": 0})

def browse_directory():
    dirname = filedialog.askdirectory()
    if dirname:
        entry_dir.delete(0, tk.END)
        entry_dir.insert(0, dirname)

def quit_application():
    global cancel_download
    cancel_download = True
    root.quit()
    root.destroy()
    sys.exit()

def main():
    global root, entry_username, entry_dir, entry_login_user, entry_login_pass, progress_bar, status_label

    root = tk.Tk()
    root.title("GramLoad")
    root.geometry("500x360") 
    root.resizable(False, False)

    window_width = 500
    window_height = 360
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    frame = tk.Frame(root)
    frame.pack(expand=True)

    tk.Label(frame, text="Target Username:").grid(row=0, column=0, padx=5, pady=5)
    entry_username = tk.Entry(frame)
    entry_username.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame, text="Destination Directory:").grid(row=1, column=0, padx=5, pady=5)
    entry_dir = tk.Entry(frame)
    entry_dir.grid(row=1, column=1, padx=5, pady=5)
    tk.Button(frame, text="Browse", command=browse_directory).grid(row=1, column=2, padx=5, pady=5)

    tk.Label(frame, text="Login Username (optional):").grid(row=2, column=0, padx=5, pady=5)
    entry_login_user = tk.Entry(frame)
    entry_login_user.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame, text="Login Password (optional):").grid(row=3, column=0, padx=5, pady=5)
    entry_login_pass = tk.Entry(frame, show="*")
    entry_login_pass.grid(row=3, column=1, padx=5, pady=5)

    tk.Button(frame, text="Download", command=start_download).grid(row=4, column=0, columnspan=3, pady=10)

    progress_bar = Progressbar(frame, orient=tk.HORIZONTAL, length=400, mode='determinate')
    progress_bar.grid(row=5, column=0, columnspan=3, pady=10)

    status_label = tk.Label(frame, text="")
    status_label.grid(row=6, column=0, columnspan=3, pady=5)

    tk.Button(frame, text="Cancel", command=cancel_download_process).grid(row=7, column=0, columnspan=3, pady=10)

    tk.Button(frame, text="Quit", command=quit_application).grid(row=8, column=0, columnspan=3, pady=10)

    if os.path.exists('config.json'):
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            entry_dir.insert(0, config.get('last_dir', ''))
            entry_login_user.insert(0, config.get('last_username', ''))
            entry_login_pass.insert(0, config.get('last_password', ''))

    root.mainloop()

if __name__ == "__main__":
    main()