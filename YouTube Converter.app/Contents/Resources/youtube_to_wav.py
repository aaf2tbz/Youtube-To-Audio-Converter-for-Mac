#!/usr/bin/env python3
import subprocess
import sys
import os
import tkinter as tk
from tkinter import filedialog, ttk
import threading

os.environ["PATH"] = "/opt/homebrew/bin:/usr/local/bin:" + os.environ.get("PATH", "")

HOMEBREW_BIN = "/opt/homebrew/bin"
YTDLP_PATH = f"{HOMEBREW_BIN}/yt-dlp"
FFMPEG_PATH = f"{HOMEBREW_BIN}/ffmpeg"
BREW_PATH = f"{HOMEBREW_BIN}/brew"

DEPS: dict[str, bool | None] = {"yt-dlp": None, "ffmpeg": None}
success_popup = None

QUALITY_OPTIONS = {
    "mp3": ["128 kbps", "192 kbps", "256 kbps", "320 kbps"],
    "m4a": ["128 kbps", "192 kbps", "256 kbps", "320 kbps"],
    "wav": ["Lossless (16-bit)", "Lossless (24-bit)"],
    "mp4": ["360p", "480p", "720p", "1080p", "1440p", "2160p (4K)"]
}

class CustomButton(tk.Frame):
    def __init__(self, parent, text, command=None, bg="#bdc3c7", fg="#2c3e50", **kwargs):
        super().__init__(parent, bg=bg, **kwargs)
        self.command = command
        self.bg_color = bg
        self.fg_color = fg
        self.disabled = False
        
        self.label = tk.Label(
            self, text=text, bg=bg, fg=fg,
            font=("Helvetica", 10), cursor="hand2"
        )
        self.label.pack(padx=20, pady=5)
        
        self.bind("<Button-1>", self._on_click)
        self.label.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.label.bind("<Enter>", self._on_enter)
        self.label.bind("<Leave>", self._on_leave)
    
    def _on_click(self, event):
        if not self.disabled and self.command:
            self.command()
    
    def _on_enter(self, event):
        if not self.disabled:
            self.config(bg=self._lighten(self.bg_color))
            self.label.config(bg=self._lighten(self.bg_color))
    
    def _on_leave(self, event):
        if not self.disabled:
            self.config(bg=self.bg_color)
            self.label.config(bg=self.bg_color)
    
    def _lighten(self, color):
        if color.startswith("#"):
            r = min(255, int(color[1:3], 16) + 20)
            g = min(255, int(color[3:5], 16) + 20)
            b = min(255, int(color[5:7], 16) + 20)
            return f"#{r:02x}{g:02x}{b:02x}"
        return color
    
    def set_colors(self, bg, fg):
        self.bg_color = bg
        self.fg_color = fg
        self.config(bg=bg)
        self.label.config(bg=bg, fg=fg)
    
    def set_state(self, state):
        self.disabled = (state == "disabled")

def check_dependency(name):
    if name == "yt-dlp":
        return os.path.exists(YTDLP_PATH)
    else:
        return os.path.exists(FFMPEG_PATH)

def check_all_deps():
    DEPS["yt-dlp"] = check_dependency("yt-dlp")
    DEPS["ffmpeg"] = check_dependency("ffmpeg")
    return all(DEPS.values())

def install_deps(callback=None):
    def run_install():
        missing = [k for k, v in DEPS.items() if not v]
        if not missing:
            if callback:
                callback(True, "All dependencies already installed")
            return
        
        has_brew = os.path.exists(BREW_PATH)
        
        for dep in missing:
            try:
                if has_brew:
                    cmd = [BREW_PATH, "install", dep]
                elif dep == "yt-dlp":
                    cmd = [sys.executable, "-m", "pip", "install", "yt-dlp"]
                else:
                    if callback:
                        callback(False, f"Cannot install {dep}: Homebrew required for ffmpeg")
                    return
                
                subprocess.run(cmd, check=True)
                DEPS[dep] = check_dependency(dep)
            except subprocess.CalledProcessError as e:
                if callback:
                    callback(False, f"Failed to install {dep}: {e}")
                return
            except Exception as e:
                if callback:
                    callback(False, f"Error installing {dep}: {e}")
                return
        
        if callback:
            callback(True, "Dependencies installed successfully!")
    
    thread = threading.Thread(target=run_install, daemon=True)
    thread.start()
    return thread

def show_success(filepath):
    global success_popup
    if success_popup:
        success_popup.destroy()
    
    success_popup = tk.Toplevel(root)
    success_popup.title("Success")
    success_popup.geometry("350x120")
    success_popup.resizable(False, False)
    success_popup.transient(root)
    success_popup.grab_set()
    
    success_popup.geometry(f"+{root.winfo_x() + 50}+{root.winfo_y() + 80}")
    
    tk.Label(
        success_popup, 
        text="Download Complete!", 
        font=("Helvetica", 12, "bold"),
        fg="green"
    ).pack(pady=(15, 5))
    
    tk.Label(
        success_popup, 
        text=f"Saved to:\n{filepath}",
        wraplength=300
    ).pack(pady=5)
    
    close_btn = CustomButton(
        success_popup, text="Close",
        command=success_popup.destroy,
        bg="#4a90d9", fg="white"
    )
    close_btn.pack(pady=10)

def show_error(title, message):
    global success_popup
    if success_popup:
        success_popup.destroy()
    
    success_popup = tk.Toplevel(root)
    success_popup.title(title)
    success_popup.geometry("350x120")
    success_popup.resizable(False, False)
    success_popup.transient(root)
    success_popup.grab_set()
    
    success_popup.geometry(f"+{root.winfo_x() + 50}+{root.winfo_y() + 80}")
    
    tk.Label(
        success_popup, 
        text=title, 
        font=("Helvetica", 12, "bold"),
        fg="red"
    ).pack(pady=(15, 5))
    
    tk.Label(
        success_popup, 
        text=message,
        wraplength=300
    ).pack(pady=5)
    
    close_btn = CustomButton(
        success_popup, text="Close",
        command=success_popup.destroy,
        bg="#c0392b", fg="white"
    )
    close_btn.pack(pady=10)

def update_quality_options(event=None):
    selected_format = format_var.get()
    quality_combo['values'] = QUALITY_OPTIONS.get(selected_format, [])
    quality_combo.current(0)

def update_button_state(event=None):
    check_all_deps()
    url = url_entry.get().strip()
    name = name_entry.get().strip()
    
    if url and name and DEPS["yt-dlp"] and DEPS["ffmpeg"]:
        download_btn.set_colors("#4a90d9", "white")
    else:
        download_btn.set_colors("#bdc3c7", "#2c3e50")

def download_and_convert():
    if not check_all_deps():
        show_error("Missing Dependencies", "Please install dependencies first.")
        return
    
    url = url_entry.get().strip()
    filename = name_entry.get().strip()
    
    if not url:
        show_error("Error", "Please enter a YouTube URL")
        return
    
    if not filename:
        show_error("Error", "Please enter a filename")
        return
    
    selected_format = format_var.get()
    for ext in [".mp3", ".m4a", ".wav", ".mp4"]:
        filename = filename.replace(ext, "")
    
    output_path = filedialog.askdirectory(title="Select output folder")
    if not output_path:
        return
    
    download_btn.set_state("disabled")
    download_btn.set_colors("#7f8c8d", "white")
    status_label.config(text="Downloading and converting...", fg="blue")
    root.update()
    
    def run_download():
        try:
            output_template = os.path.join(output_path, f"{filename}.{selected_format}")
            quality = quality_var.get()
            
            cmd = [YTDLP_PATH]
            
            if selected_format in ["mp3", "m4a", "wav"]:
                cmd.extend(["-x", "--audio-format", selected_format])
                
                if selected_format == "mp3":
                    if "320" in quality:
                        cmd.extend(["--audio-quality", "0"])
                    elif "256" in quality:
                        cmd.extend(["--audio-quality", "1"])
                    elif "192" in quality:
                        cmd.extend(["--audio-quality", "2"])
                    else:
                        cmd.extend(["--audio-quality", "4"])
                
                elif selected_format == "m4a":
                    if "320" in quality:
                        cmd.extend(["--audio-quality", "0"])
                    elif "256" in quality:
                        cmd.extend(["--audio-quality", "1"])
                    elif "192" in quality:
                        cmd.extend(["--audio-quality", "2"])
                    else:
                        cmd.extend(["--audio-quality", "4"])
                
                elif selected_format == "wav":
                    pass
            
            elif selected_format == "mp4":
                resolution_map = {
                    "360p": "360",
                    "480p": "480",
                    "720p": "720",
                    "1080p": "1080",
                    "1440p": "1440",
                    "2160p (4K)": "2160"
                }
                res = resolution_map.get(quality, "720")
                cmd.extend([
                    "-f", f"bestvideo[height<={res}]+bestaudio/best[height<={res}]",
                    "--merge-output-format", "mp4"
                ])
            
            cmd.extend(["-o", output_template, url])
            
            result = subprocess.run(cmd, capture_output=True, text=True, env=os.environ)
            
            if result.returncode == 0:
                actual_file = output_template
                if not os.path.exists(actual_file):
                    for f in os.listdir(output_path):
                        if f.startswith(filename) and f.endswith(f".{selected_format}"):
                            actual_file = os.path.join(output_path, f)
                            break
                
                root.after(0, lambda: status_label.config(
                    text=f"Done! Saved to: {actual_file}", fg="green"
                ))
                root.after(0, lambda: show_success(actual_file))
            else:
                error_msg = result.stderr or result.stdout or "Unknown error"
                if len(error_msg) > 150:
                    error_msg = error_msg[:150] + "..."
                root.after(0, lambda: status_label.config(text="Error", fg="red"))
                root.after(0, lambda: show_error("Error", error_msg))
        except Exception as e:
            root.after(0, lambda: status_label.config(text="Error", fg="red"))
            root.after(0, lambda: show_error("Error", str(e)))
        finally:
            root.after(0, lambda: download_btn.set_state("normal"))
            root.after(0, update_button_state)
    
    threading.Thread(target=run_download, daemon=True).start()

def update_deps_status():
    check_all_deps()
    missing = [k for k, v in DEPS.items() if not v]
    if missing:
        deps_label.config(
            text=f"Missing: {', '.join(missing)}",
            fg="red"
        )
        install_btn.config(state="normal")
    else:
        deps_label.config(text="All dependencies installed", fg="green")
        install_btn.config(state="disabled")
    update_button_state()

def handle_install():
    install_btn.config(state="disabled", text="Installing...")
    deps_label.config(text="Installing dependencies...", fg="blue")
    
    def on_complete(success, message):
        root.after(0, lambda: install_btn.config(text="Install Dependencies"))
        if success:
            root.after(0, lambda: deps_label.config(text=message, fg="green"))
        else:
            root.after(0, lambda: deps_label.config(text=message, fg="red"))
            root.after(0, lambda: show_error("Error", message))
            root.after(0, lambda: install_btn.config(state="normal"))
        root.after(0, update_deps_status)
    
    install_deps(on_complete)

root = tk.Tk()
root.title("YouTube Converter")
root.geometry("450x370")
root.resizable(False, False)

deps_frame = tk.Frame(root)
deps_frame.pack(pady=(10, 0), fill="x")

deps_label = tk.Label(deps_frame, text="Checking dependencies...", fg="blue")
deps_label.pack(side="left", padx=10)

install_btn = tk.Button(
    deps_frame, text="Install Dependencies",
    command=handle_install, bg="#e67e22", fg="white"
)
install_btn.pack(side="right", padx=10)

tk.Label(root, text="YouTube URL:").pack(pady=(10, 0))
url_frame = tk.Frame(root, bg="#3498db", padx=2, pady=2)
url_frame.pack(pady=2)
url_entry = tk.Entry(url_frame, width=50, bg="white", fg="black", insertbackground="black", relief="flat")
url_entry.pack(padx=2, pady=2)
url_entry.bind("<KeyRelease>", update_button_state)

tk.Label(root, text="Filename:").pack()
name_frame = tk.Frame(root, bg="#3498db", padx=2, pady=2)
name_frame.pack(pady=2)
name_entry = tk.Entry(name_frame, width=50, bg="white", fg="black", insertbackground="black", relief="flat")
name_entry.pack(padx=2, pady=2)
name_entry.bind("<KeyRelease>", update_button_state)

options_frame = tk.Frame(root)
options_frame.pack(pady=10, fill="x", padx=20)

tk.Label(options_frame, text="Format:").grid(row=0, column=0, padx=5, sticky="e")
format_var = tk.StringVar(value="mp3")
format_combo = ttk.Combobox(options_frame, textvariable=format_var, values=["mp3", "m4a", "wav", "mp4"], width=12, state="readonly")
format_combo.grid(row=0, column=1, padx=5)
format_combo.bind("<<ComboboxSelected>>", update_quality_options)

tk.Label(options_frame, text="Quality:").grid(row=0, column=2, padx=5, sticky="e")
quality_var = tk.StringVar()
quality_combo = ttk.Combobox(options_frame, textvariable=quality_var, width=15, state="readonly")
quality_combo.grid(row=0, column=3, padx=5)

update_quality_options()

download_btn = CustomButton(
    root, text="Download & Convert", command=download_and_convert,
    bg="#bdc3c7", fg="#2c3e50"
)
download_btn.pack(pady=15)

status_label = tk.Label(root, text="", fg="blue")
status_label.pack()

root.after(100, update_deps_status)
root.mainloop()
