#!/usr/bin/env python3
import subprocess
import sys
import os
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox

os.environ["PATH"] = "/opt/homebrew/bin:/usr/local/bin:" + os.environ.get("PATH", "")

HOMEBREW_BIN = "/opt/homebrew/bin"
YTDLP_PATH = f"{HOMEBREW_BIN}/yt-dlp"
FFMPEG_PATH = f"{HOMEBREW_BIN}/ffmpeg"
BREW_PATH = f"{HOMEBREW_BIN}/brew"

DEPS: dict[str, bool | None] = {"yt-dlp": None, "ffmpeg": None, "customtkinter": None}

COLORS = {
    "bg": "#1a1a2e",
    "card": "#16213e",
    "accent": "#e94560",
    "accent_hover": "#ff6b6b",
    "success": "#0f3460",
    "text": "#eaeaea",
    "text_muted": "#a0a0a0",
    "input_bg": "#0f0f23",
    "border": "#2d2d5a"
}

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

QUALITY_OPTIONS = {
    "mp3": ["128 kbps", "192 kbps", "256 kbps", "320 kbps"],
    "m4a": ["128 kbps", "192 kbps", "256 kbps", "320 kbps"],
    "wav": ["Lossless (16-bit)", "Lossless (24-bit)"],
    "mp4": ["360p", "480p", "720p", "1080p", "1440p", "2160p (4K)"]
}

def check_dependency(name):
    if name == "yt-dlp":
        return os.path.exists(YTDLP_PATH)
    elif name == "ffmpeg":
        return os.path.exists(FFMPEG_PATH)
    elif name == "customtkinter":
        try:
            import customtkinter
            return True
        except ImportError:
            return False
    return False

def check_all_deps():
    DEPS["yt-dlp"] = check_dependency("yt-dlp")
    DEPS["ffmpeg"] = check_dependency("ffmpeg")
    DEPS["customtkinter"] = check_dependency("customtkinter")
    return all(DEPS.values())

def install_deps(callback=None):
    def run_install():
        missing = [k for k, v in DEPS.items() if not v]
        if not missing:
            if callback:
                callback(True, "All dependencies ready")
            return
        
        has_brew = os.path.exists(BREW_PATH)
        
        for dep in missing:
            try:
                if dep == "customtkinter":
                    cmd = [sys.executable, "-m", "pip", "install", "--break-system-packages", dep]
                elif has_brew:
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
            callback(True, "Dependencies installed!")
    
    thread = threading.Thread(target=run_install, daemon=True)
    thread.start()
    return thread

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("YouTube Converter")
        self.geometry("520x580")
        self.minsize(420, 500)
        self.configure(fg_color=COLORS["bg"])
        
        self.success_popup = None
        
        self._create_widgets()
        self.after(100, self.update_deps_status)
    
    def _create_widgets(self):
        title = ctk.CTkLabel(
            self,
            text="YouTube Converter",
            font=("SF Pro Display", 28, "bold"),
            text_color=COLORS["text"]
        )
        title.pack(pady=(20, 4))
        
        subtitle = ctk.CTkLabel(
            self,
            text="Download & convert to any format",
            font=("SF Pro Display", 13),
            text_color=COLORS["text_muted"]
        )
        subtitle.pack(pady=(0, 16))
        
        self.deps_frame = ctk.CTkFrame(
            self,
            fg_color=COLORS["card"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"]
        )
        self.deps_frame.pack(fill="x", padx=20, pady=(0, 12))
        self.deps_frame.columnconfigure(0, weight=1)
        
        self.deps_label = ctk.CTkLabel(
            self.deps_frame,
            text="Checking dependencies...",
            font=("SF Pro Display", 12),
            text_color=COLORS["text_muted"]
        )
        self.deps_label.grid(row=0, column=0, padx=16, pady=12, sticky="w")
        
        self.install_btn = ctk.CTkButton(
            self.deps_frame,
            text="Install",
            font=("SF Pro Display", 12, "bold"),
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            corner_radius=8,
            width=90,
            height=32,
            command=self.handle_install
        )
        self.install_btn.grid(row=0, column=1, padx=16, pady=12)
        
        input_card = ctk.CTkFrame(
            self,
            fg_color=COLORS["card"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"]
        )
        input_card.pack(fill="x", padx=20, pady=(0, 12))
        
        url_label = ctk.CTkLabel(
            input_card,
            text="YouTube URL",
            font=("SF Pro Display", 12),
            text_color=COLORS["text"],
            anchor="w"
        )
        url_label.pack(fill="x", padx=16, pady=(16, 4))
        
        self.url_entry = ctk.CTkEntry(
            input_card,
            placeholder_text="https://youtube.com/watch?v=...",
            font=("SF Pro Display", 13),
            fg_color=COLORS["input_bg"],
            border_color=COLORS["border"],
            corner_radius=8,
            height=40,
            text_color=COLORS["text"]
        )
        self.url_entry.pack(fill="x", padx=16, pady=(0, 12))
        self.url_entry.bind("<KeyRelease>", self.update_button_state)
        
        name_label = ctk.CTkLabel(
            input_card,
            text="Filename",
            font=("SF Pro Display", 12),
            text_color=COLORS["text"],
            anchor="w"
        )
        name_label.pack(fill="x", padx=16, pady=(0, 4))
        
        self.name_entry = ctk.CTkEntry(
            input_card,
            placeholder_text="my_song",
            font=("SF Pro Display", 13),
            fg_color=COLORS["input_bg"],
            border_color=COLORS["border"],
            corner_radius=8,
            height=40,
            text_color=COLORS["text"]
        )
        self.name_entry.pack(fill="x", padx=16, pady=(0, 16))
        self.name_entry.bind("<KeyRelease>", self.update_button_state)
        
        options_card = ctk.CTkFrame(
            self,
            fg_color=COLORS["card"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"]
        )
        options_card.pack(fill="x", padx=20, pady=(0, 16))
        options_card.columnconfigure((0, 1, 2, 3), weight=1)
        
        format_label = ctk.CTkLabel(
            options_card,
            text="Format",
            font=("SF Pro Display", 12),
            text_color=COLORS["text"]
        )
        format_label.grid(row=0, column=0, padx=16, pady=(12, 4), sticky="w")
        
        self.format_var = ctk.StringVar(value="mp3")
        self.format_combo = ctk.CTkComboBox(
            options_card,
            variable=self.format_var,
            values=["mp3", "m4a", "wav", "mp4"],
            font=("SF Pro Display", 12),
            dropdown_font=("SF Pro Display", 12),
            fg_color=COLORS["input_bg"],
            border_color=COLORS["border"],
            button_color=COLORS["accent"],
            button_hover_color=COLORS["accent_hover"],
            dropdown_fg_color=COLORS["card"],
            corner_radius=8,
            height=32,
            state="readonly",
            command=self.update_quality_options
        )
        self.format_combo.grid(row=1, column=0, padx=16, pady=(0, 12), sticky="ew")
        
        quality_label = ctk.CTkLabel(
            options_card,
            text="Quality",
            font=("SF Pro Display", 12),
            text_color=COLORS["text"]
        )
        quality_label.grid(row=0, column=2, padx=16, pady=(12, 4), sticky="w")
        
        self.quality_var = ctk.StringVar()
        self.quality_combo = ctk.CTkComboBox(
            options_card,
            variable=self.quality_var,
            values=QUALITY_OPTIONS["mp3"],
            font=("SF Pro Display", 12),
            dropdown_font=("SF Pro Display", 12),
            fg_color=COLORS["input_bg"],
            border_color=COLORS["border"],
            button_color=COLORS["accent"],
            button_hover_color=COLORS["accent_hover"],
            dropdown_fg_color=COLORS["card"],
            corner_radius=8,
            height=32,
            state="readonly"
        )
        self.quality_combo.grid(row=1, column=2, columnspan=2, padx=16, pady=(0, 12), sticky="ew")
        self.quality_combo.set(QUALITY_OPTIONS["mp3"][0])
        
        self.download_btn = ctk.CTkButton(
            self,
            text="Download & Convert",
            font=("SF Pro Display", 16, "bold"),
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            corner_radius=12,
            height=56,
            command=self.download_and_convert
        )
        self.download_btn.pack(fill="x", padx=20, pady=(0, 12))
        
        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=("SF Pro Display", 12),
            text_color=COLORS["text_muted"]
        )
        self.status_label.pack(pady=(0, 12))
        
        self.update_button_state()
    
    def update_quality_options(self, event=None):
        selected_format = self.format_var.get()
        qualities = QUALITY_OPTIONS.get(selected_format, [])
        self.quality_combo.configure(values=qualities)
        self.quality_combo.set(qualities[0] if qualities else "")
    
    def update_button_state(self, event=None):
        check_all_deps()
        url = self.url_entry.get().strip()
        name = self.name_entry.get().strip()
        
        if url and name and DEPS["yt-dlp"] and DEPS["ffmpeg"]:
            self.download_btn.configure(
                fg_color=COLORS["accent"],
                state="normal"
            )
        else:
            self.download_btn.configure(
                fg_color="#3d3d5c",
                state="disabled"
            )
    
    def update_deps_status(self):
        check_all_deps()
        missing = [k for k, v in DEPS.items() if not v]
        if missing:
            self.deps_label.configure(
                text=f"⚠ Missing: {', '.join(missing)}",
                text_color="#ff6b6b"
            )
            self.install_btn.configure(state="normal")
        else:
            self.deps_label.configure(
                text="✓ Ready to convert",
                text_color="#4ade80"
            )
            self.install_btn.configure(state="disabled")
        self.update_button_state()
    
    def handle_install(self):
        self.install_btn.configure(state="disabled", text="Installing...")
        self.deps_label.configure(text="Installing dependencies...", text_color="#fbbf24")
        
        def on_complete(success, message):
            self.after(0, lambda: self.install_btn.configure(text="Install"))
            if success:
                self.after(0, lambda: self.deps_label.configure(text=message, text_color="#4ade80"))
            else:
                self.after(0, lambda: self.deps_label.configure(text=message, text_color="#ff6b6b"))
                self.after(0, lambda: self.show_error("Installation Error", message))
                self.after(0, lambda: self.install_btn.configure(state="normal"))
            self.after(0, self.update_deps_status)
        
        install_deps(on_complete)
    
    def show_success(self, filepath):
        if self.success_popup:
            self.success_popup.destroy()
        
        self.success_popup = ctk.CTkToplevel(self)
        self.success_popup.title("Success")
        self.success_popup.geometry("380x160")
        self.success_popup.resizable(False, False)
        self.success_popup.configure(fg_color=COLORS["bg"])
        self.success_popup.transient(self)
        self.success_popup.grab_set()
        
        self.success_popup.geometry(f"+{self.winfo_x() + 50}+{self.winfo_y() + 100}")
        
        ctk.CTkLabel(
            self.success_popup,
            text="Download Complete!",
            font=("SF Pro Display", 16, "bold"),
            text_color="#4ade80"
        ).pack(pady=(20, 8))
        
        ctk.CTkLabel(
            self.success_popup,
            text=f"Saved to:\n{filepath}",
            font=("SF Pro Display", 12),
            text_color=COLORS["text_muted"],
            wraplength=340
        ).pack(pady=8)
        
        ctk.CTkButton(
            self.success_popup,
            text="Done",
            font=("SF Pro Display", 13, "bold"),
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            corner_radius=8,
            width=100,
            command=self.success_popup.destroy
        ).pack(pady=16)
    
    def show_error(self, title, message):
        if self.success_popup:
            self.success_popup.destroy()
        
        self.success_popup = ctk.CTkToplevel(self)
        self.success_popup.title(title)
        self.success_popup.geometry("380x160")
        self.success_popup.resizable(False, False)
        self.success_popup.configure(fg_color=COLORS["bg"])
        self.success_popup.transient(self)
        self.success_popup.grab_set()
        
        self.success_popup.geometry(f"+{self.winfo_x() + 50}+{self.winfo_y() + 100}")
        
        ctk.CTkLabel(
            self.success_popup,
            text=title,
            font=("SF Pro Display", 16, "bold"),
            text_color="#ff6b6b"
        ).pack(pady=(20, 8))
        
        ctk.CTkLabel(
            self.success_popup,
            text=message,
            font=("SF Pro Display", 12),
            text_color=COLORS["text_muted"],
            wraplength=340
        ).pack(pady=8)
        
        ctk.CTkButton(
            self.success_popup,
            text="Close",
            font=("SF Pro Display", 13, "bold"),
            fg_color="#ff6b6b",
            hover_color="#ff8a8a",
            corner_radius=8,
            width=100,
            command=self.success_popup.destroy
        ).pack(pady=16)
    
    def download_and_convert(self):
        if not check_all_deps():
            self.show_error("Missing Dependencies", "Please install dependencies first.")
            return
        
        url = self.url_entry.get().strip()
        filename = self.name_entry.get().strip()
        
        if not url:
            self.show_error("Error", "Please enter a YouTube URL")
            return
        
        if not filename:
            self.show_error("Error", "Please enter a filename")
            return
        
        selected_format = self.format_var.get()
        for ext in [".mp3", ".m4a", ".wav", ".mp4"]:
            filename = filename.replace(ext, "")
        
        output_path = filedialog.askdirectory(title="Select output folder")
        if not output_path:
            return
        
        self.download_btn.configure(state="disabled", fg_color="#3d3d5c")
        self.status_label.configure(text="Downloading and converting...", text_color="#fbbf24")
        
        def run_download():
            try:
                output_template = os.path.join(output_path, f"{filename}.{selected_format}")
                quality = self.quality_var.get()
                
                cmd = [YTDLP_PATH]
                
                if selected_format in ["mp3", "m4a", "wav"]:
                    cmd.extend(["-x", "--audio-format", selected_format])
                    
                    if selected_format in ["mp3", "m4a"]:
                        if "320" in quality:
                            cmd.extend(["--audio-quality", "0"])
                        elif "256" in quality:
                            cmd.extend(["--audio-quality", "1"])
                        elif "192" in quality:
                            cmd.extend(["--audio-quality", "2"])
                        else:
                            cmd.extend(["--audio-quality", "4"])
                
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
                    
                    self.after(0, lambda: self.status_label.configure(
                        text=f"✓ Saved to: {actual_file}",
                        text_color="#4ade80"
                    ))
                    self.after(0, lambda: self.show_success(actual_file))
                else:
                    error_msg = result.stderr or result.stdout or "Unknown error"
                    if len(error_msg) > 150:
                        error_msg = error_msg[:150] + "..."
                    self.after(0, lambda: self.status_label.configure(text="Download failed", text_color="#ff6b6b"))
                    self.after(0, lambda: self.show_error("Error", error_msg))
            except Exception as e:
                self.after(0, lambda: self.status_label.configure(text="Error occurred", text_color="#ff6b6b"))
                self.after(0, lambda: self.show_error("Error", str(e)))
            finally:
                self.after(0, lambda: self.download_btn.configure(state="normal"))
                self.after(0, self.update_button_state)
        
        threading.Thread(target=run_download, daemon=True).start()

if __name__ == "__main__":
    app = App()
    app.mainloop()
