#!/usr/bin/env python3
# coding: utf-8

"""
MARTYR – AI Mastering Desktop App

– Custom title bar (minimize & close), draggable, centered
– Rounded, borderless red buttons
– Matte-black dropdowns with dark arrow button, centered larger text
– Centered bold section titles
– Background mastering thread (no freeze)
– Manual + dynamic presets, waveform preview
– LUFS/format/quality selectors
– Export WAV/FLAC/MP3 via matchering + imageio-ffmpeg
– Persistent footer with links
"""

import os, tempfile, shutil, webbrowser, requests, subprocess, threading
from datetime import datetime

import matchering as mg
import pandas as pd
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import imageio_ffmpeg

import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Global state
track_file = None
reference_file = None
wave_canvas = None

# Presets (genres only, updated URLs)
manual_presets = {
    "SELECT MANUALLY": None,
    "ROCK":     "https://martired.com/wp-content/uploads/2025/04/ROCK.flac",
    "ALT.ROCK":     "https://martired.com/wp-content/uploads/2025/04/ALTERNATIVE-ROCK.flac",
    "METALCORE":     "https://martired.com/wp-content/uploads/2025/04/METALCORE.flac",
    "HYPERPOP":     "https://martired.com/wp-content/uploads/2025/04/HYPERPOP.flac",
    "HIPHOP":     "https://martired.com/wp-content/uploads/2025/04/HIPHOPRAP.flac",
    "CLASSICAL":     "https://martired.com/wp-content/uploads/2025/04/CLASSICAL.flac",
    "POP":     "https://martired.com/wp-content/uploads/2025/04/POP.flac",
    "AFROBEAT":     "https://martired.com/wp-content/uploads/2025/04/AFROBEAT.flac",
    "LATIN":     "https://martired.com/wp-content/uploads/2025/04/LATINO.flac",
}

def load_dynamic():
    try:
        df = pd.read_csv(
            "https://docs.google.com/spreadsheets/d/1Zvdf--BtuVIMsg7lves2Ndp48EGjh4s8mB5l1UsVuiw/gviz/tq?tqx=out:csv"
        )
        if df.shape[1] >= 2:
            return {str(n).upper(): str(l) for n,l in zip(df.iloc[:,0], df.iloc[:,1]) if l}
    except:
        pass
    return {}

preset_map = {**manual_presets, **load_dynamic()}
preset_names = list(preset_map.keys())

# Logging
def log(msg):
    txt_log.config(state="normal")
    txt_log.insert("end", msg + "\n")
    txt_log.see("end")
    txt_log.config(state="disabled")

# Waveform preview
def show_waveform(path):
    global wave_canvas
    if wave_canvas:
        wave_canvas.get_tk_widget().destroy()
    try:
        data, sr = sf.read(path)
    except:
        log("WARN: cannot preview waveform")
        return
    fig = plt.figure(facecolor="black", figsize=(8,0.5), dpi=100)
    ax = fig.add_axes([0,0,1,1])
    ax.plot(np.arange(len(data))/sr, data.mean(axis=1) if data.ndim > 1 else data, color="white")
    ax.axis("off")
    wave_canvas = FigureCanvasTkAgg(fig, master=frame_wave)
    wave_canvas.draw()
    wave_canvas.get_tk_widget().pack(fill="x", padx=20, pady=5)

# Convert & save
def convert_and_save(wav, fmt, qual):
    base = os.path.splitext(os.path.basename(track_file))[0]
    default = f"{base}_masterizado.{fmt}"
    dest = filedialog.asksaveasfilename(
        initialfile=default,
        defaultextension=f".{fmt}",
        filetypes=[("WAV","*.wav"),("FLAC","*.flac"),("MP3","*.mp3")],
        title="Save mastered file"
    )
    if not dest:
        return
    try:
        if fmt == "wav":
            shutil.move(wav, dest)
        elif fmt == "flac":
            d, sr = sf.read(wav)
            sf.write(dest, d, sr, format="FLAC", subtype="PCM_24" if qual=="high" else "PCM_16")
            os.remove(wav)
        else:
            exe = imageio_ffmpeg.get_ffmpeg_exe()
            br = "320k" if qual=="high" else "192k"
            subprocess.check_call([exe, "-y", "-i", wav, "-codec:a", "libmp3lame", "-b:a", br, dest])
            os.remove(wav)
        log(f"Saved: {dest}")
    except Exception as e:
        messagebox.showerror("Export Error", str(e))

# Load preset reference
def load_preset_ref(name):
    global reference_file
    reference_file = None
    lbl_ref.config(text="")
    url = preset_map.get(name)
    if not url:
        return
    tmp = tempfile.mkdtemp(prefix="preset_")
    ext = os.path.splitext(url)[1]
    out = os.path.join(tmp, name + ext)
    try:
        r = requests.get(url, stream=True, timeout=30); r.raise_for_status()
        with open(out, "wb") as f:
            for ch in r.iter_content(8192):
                f.write(ch)
    except Exception as e:
        messagebox.showerror("Download Error", str(e))
        shutil.rmtree(tmp, ignore_errors=True)
        return
    reference_file = out
    if name != "SELECT MANUALLY":
        lbl_ref.config(text=name)
    else:
        lbl_ref.config(text=os.path.basename(out))

# Upload handlers
def on_upload_ref():
    global reference_file
    p = filedialog.askopenfilename(filetypes=[("Audio files","*.wav *.flac *.mp3 *.aac *.m4a *.ogg *.wma")])
    if p:
        reference_file = p
        lbl_ref.config(text=os.path.basename(p))
        preset_var.set("SELECT MANUALLY")

def on_upload_track():
    global track_file
    p = filedialog.askopenfilename(filetypes=[("Audio files","*.wav *.flac *.mp3 *.aac *.m4a *.ogg *.wma")])
    if p:
        track_file = p
        lbl_track.config(text=os.path.basename(p))
        show_waveform(p)

# Mastering process
def on_start_process():
    if not track_file:
        messagebox.showwarning("Missing Target","Upload a track first"); return
    if not reference_file:
        messagebox.showwarning("Missing Reference","Select or upload reference"); return
    log("Starting mastering...")
    mg.log(info_handler=lambda t: log("INFO: "+t),
           warning_handler=lambda t: log("WARN: "+t),
           debug_handler=lambda t: log("DEBUG: "+t))
    out = os.path.join(tempfile.gettempdir(), f"master_{datetime.now():%Y%m%d_%H%M%S}.wav")
    try:
        mg.process(target=track_file, reference=reference_file, results=[mg.pcm24(out)])
        convert_and_save(out, fmt_var.get(), qual_var.get())
        log("Done")
    except Exception as e:
        log("ERROR: "+str(e))

def start_mastering():
    threading.Thread(target=on_start_process, daemon=True).start()

# Build UI
root = tk.Tk()
root.option_add('*TCombobox*Listbox.background','black')
root.option_add('*TCombobox*Listbox.foreground','white')
root.option_add('*TCombobox*Listbox.selectBackground','#330000')
root.option_add('*TCombobox*Listbox.selectForeground','white')
root.option_add('*TCombobox*Listbox.font',('Arial',12))
root.option_add('TCombobox*Listbox*justify','center')

root.overrideredirect(True)
root.update_idletasks()
w,h = 500,700; x=(root.winfo_screenwidth()-w)//2; y=(root.winfo_screenheight()-h)//2
root.geometry(f"{w}x{h}+{x}+{y}"); root.configure(bg="#181818")

def start_move(e):
    root.drag_x=e.x_root-root.winfo_x(); root.drag_y=e.y_root-root.winfo_y()
def on_move(e):
    root.geometry(f"+{e.x_root-root.drag_x}+{e.y_root-root.drag_y}")

title = tk.Frame(root,bg="#111",height=30); title.pack(fill="x")
title.bind("<Button-1>",start_move); title.bind("<B1-Motion>",on_move)
tk.Label(title,text="MARTYR",fg="red",bg="#111",font=("Akira Expanded",14)).place(relx=0.5,rely=0.5,anchor="center")
tk.Button(title,text="—",command=lambda:(root.overrideredirect(False),root.iconify()),bd=0,bg="#111",fg="white",activebackground="#333").pack(side="right",padx=5)
tk.Button(title,text="✕",command=root.destroy,bd=0,bg="#111",fg="white",activebackground="#900").pack(side="right")
root.bind("<Map>",lambda e:root.overrideredirect(True))

style=ttk.Style(root); style.theme_use("clam")
style.configure("Red.TButton",background="#8B0000",foreground="white",font=("Arial",12,"bold"),borderwidth=0,relief="flat",borderradius=20)
style.map("Red.TButton",background=[("active","#a00000")])
style.configure("Rounded.TCombobox",fieldbackground="black",background="black",foreground="white",bordercolor="#444444",lightcolor="#444444",darkcolor="#444444",borderwidth=1,relief="flat",padding=6,borderradius=8,font=("Arial",12))
style.map("Rounded.TCombobox",fieldbackground=[("readonly","black")],background=[("readonly","black")],selectbackground=[("readonly","#330000")],selectforeground=[("readonly","white")],arrowcolor=[("!disabled","white")])

cont = tk.Frame(root,bg="#181818"); cont.place(x=0,y=30,relwidth=1,relheight=1,height=-80)

tk.Label(cont,text="Preset:",fg="white",bg="#181818",font=("Arial",12,"bold")).pack(pady=(10,0))
preset_var = tk.StringVar(value=preset_names[0])
cmb = ttk.Combobox(cont,textvariable=preset_var,values=preset_names,state="readonly",style="Rounded.TCombobox")
cmb.pack(fill="x",padx=100,pady=2); cmb.bind("<<ComboboxSelected>>",lambda e:load_preset_ref(preset_var.get()))

ttk.Button(cont,text="Upload Reference Track",style="Red.TButton",command=on_upload_ref).pack(fill="x",padx=20,pady=5)
lbl_ref = tk.Label(cont,text="",fg="white",bg="#181818",font=("Arial",11)); lbl_ref.pack(fill="x",padx=20)

tk.Label(cont,text="LUFS Target:",fg="white",bg="#181818",font=("Arial",12,"bold")).pack(pady=(10,0))
lufs_var = tk.StringVar(value="-18 LUFS (Generic)")
ttk.Combobox(cont,textvariable=lufs_var,values=["-8 LUFS (Film)","-14 LUFS (Spotify)","-16 LUFS (YouTube)","-18 LUFS (Generic)","-23 LUFS (CD)"],state="readonly",style="Rounded.TCombobox").pack(fill="x",padx=100,pady=2)

tk.Label(cont,text="Output Format:",fg="white",bg="#181818",font=("Arial",12,"bold")).pack(pady=(10,0))
fmt_var = tk.StringVar(value="wav")
ttk.Combobox(cont,textvariable=fmt_var,values=["wav","flac","mp3"],state="readonly",style="Rounded.TCombobox").pack(fill="x",padx=100,pady=2)

tk.Label(cont,text="Quality:",fg="white",bg="#181818",font=("Arial",12,"bold")).pack(pady=(10,0))
qual_var = tk.StringVar(value="high")
ttk.Combobox(cont,textvariable=qual_var,values=["medium","high"],state="readonly",style="Rounded.TCombobox").pack(fill="x",padx=100,pady=2)

ttk.Button(cont,text="Upload Track",style="Red.TButton",command=on_upload_track).pack(fill="x",padx=20,pady=5)
ttk.Button(cont,text="Start Mastering",style="Red.TButton",command=start_mastering).pack(fill="x",padx=20,pady=5)

txt_log = tk.Text(cont,height=6,bg="black",fg="white",font=("Courier",10),state="disabled"); txt_log.pack(fill="both",padx=20,pady=(10,0))
frame_wave = tk.Frame(cont,bg="#181818"); frame_wave.pack(fill="x",padx=20,pady=5)
lbl_track = tk.Label(cont,text="",fg="white",bg="#181818",font=("Arial",11)); lbl_track.pack(fill="x",padx=20)

tk.Frame(root,height=2,bg="#444444").pack(fill="x",side="bottom")
footer = tk.Frame(root,bg="#181818"); footer.pack(fill="x",side="bottom",pady=10)
tk.Label(footer,text="Powered by Matchering",fg="yellow",bg="#181818",font=("Arial",12)).pack()
lnk = tk.Label(footer,text="www.martired.com",fg="red",bg="#181818",font=("Arial",10,"underline"),cursor="hand2"); lnk.pack()
lnk.bind("<Button-1>",lambda e:webbrowser.open("https://martired.com"))
tk.Label(footer,text="tested by Lina",fg="red",bg="#181818",font=("Arial",10)).pack()

root.mainloop()
