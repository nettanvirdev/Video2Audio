#!/usr/bin/env python3

import urllib.request
import urllib.error
import re
import sys
import time
import os
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from threading import Thread

# Function to install necessary dependencies
def install_dependencies():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "ffmpeg-python"])
    except Exception as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

def video_to_audio(filePath, progress_bar, progress_label):
    try:
        import ffmpeg
        file, file_extension = os.path.splitext(filePath)
        progress_label.config(text="Converting video to WAV format...")
        wav_output = f"{file}.wav"
        ffmpeg.input(filePath).output(wav_output).run(overwrite_output=True)
        
        progress_bar['value'] = 50
        progress_label.config(text="Converting WAV to MP3 format...")
        mp3_output = f"{file}.mp3"
        ffmpeg.input(wav_output).output(mp3_output).run(overwrite_output=True)
        
        os.remove(wav_output)
        progress_bar['value'] = 100
        progress_label.config(text="Conversion completed successfully!")
        messagebox.showinfo("Success", f"Successfully converted {filePath} to audio!")
    except Exception as e:
        progress_label.config(text=f"Error: {e}")
        messagebox.showerror("Error", f"Error: {e}")
        exit(1)

def start_conversion(filePath, progress_bar, progress_label):
    progress_bar['value'] = 0
    progress_label.config(text="Starting conversion...")
    conversion_thread = Thread(target=video_to_audio, args=(filePath, progress_bar, progress_label))
    conversion_thread.start()

def browse_file(entry, progress_label):
    file_path = filedialog.askopenfilename()
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)
        progress_label.config(text="File selected.")

def main():
    install_dependencies()
    
    root = tk.Tk()
    root.title("Video to Audio Converter")
    
    frame = ttk.Frame(root, padding="10 10 10 10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    file_label = ttk.Label(frame, text="Select Video File:")
    file_label.grid(row=0, column=0, pady=5)
    
    file_entry = ttk.Entry(frame, width=50)
    file_entry.grid(row=0, column=1, pady=5)
    
    browse_button = ttk.Button(frame, text="Browse", command=lambda: browse_file(file_entry, progress_label))
    browse_button.grid(row=0, column=2, pady=5)
    
    convert_button = ttk.Button(frame, text="Convert", command=lambda: start_conversion(file_entry.get(), progress_bar, progress_label))
    convert_button.grid(row=1, column=0, columnspan=3, pady=10)
    
    progress_bar = ttk.Progressbar(frame, orient="horizontal", length=400, mode="determinate")
    progress_bar.grid(row=2, column=0, columnspan=3, pady=5)
    
    progress_label = ttk.Label(frame, text="")
    progress_label.grid(row=3, column=0, columnspan=3)
    
    root.mainloop()

# Run the application
if __name__ == '__main__':
    main()