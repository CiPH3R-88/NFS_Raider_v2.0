import customtkinter
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import struct
import os
import sys
import ctypes
from tkinter import font as tkfont

# ================= APP DIR =================

def app_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(__file__)

# ================= FONT LOADING =================

def load_custom_font(font_filename):
    font_path = os.path.join(app_dir(), font_filename)
    if os.path.exists(font_path):
        ctypes.windll.gdi32.AddFontResourceExW(font_path, 0x10, 0)

load_custom_font("RobotoMono.ttf")

# ================= UI SETTINGS =================

FONT_LABEL = ("Roboto Mono", 17, "bold")
FONT_INPUT = ("Roboto Mono", 16, "bold")
FONT_FIELD = ("Roboto Mono", 16)
FONT_COLOR = "#1bbc68"

FIELD_TEXT_COLOR = "#7A7A7A"
FIELD_HIGHLIGHT_COLOR = "#1bbc68"
FIELD_BORDER_COLOR = "#484848"

# ================= BIN HASH =================

def bin_hash_32(s: str) -> int:
    h = 0xFFFFFFFF
    for ch in s.encode("latin-1", errors="ignore"):
        h = (h * 33 + ch) & 0xFFFFFFFF
    return h

# ================= VLT HASH =================

def u32(x): return x & 0xFFFFFFFF

def mix32_1(a, b, c):
    a = u32((c >> 13) ^ (a - b - c))
    b = u32((a << 8) ^ (b - c - a))
    c = u32((b >> 13) ^ (c - a - b))
    a = u32((c >> 12) ^ (a - b - c))
    b = u32((a << 16) ^ (b - c - a))
    c = u32((b >> 5) ^ (c - a - b))
    a = u32((c >> 3) ^ (a - b - c))
    b = u32((a << 10) ^ (b - c - a))
    c = u32((b >> 15) ^ (c - a - b))
    return a, b, c

def mix32_2(a, b, c):
    a = u32((c >> 13) ^ (a - b - c))
    b = u32((a << 8) ^ (b - c - a))
    c = u32((b >> 13) ^ (c - a - b))
    a = u32((c >> 12) ^ (a - b - c))
    b = u32((a << 16) ^ (b - c - a))
    c = u32((b >> 5) ^ (c - a - b))
    a = u32((c >> 3) ^ (a - b - c))
    b = u32((a << 10) ^ (b - c - a))
    return u32((b >> 15) ^ (c - a - b))

def vlt_hash_32(s: str) -> int:
    if not s:
        return 0

    arr = s.encode("ascii", errors="ignore")

    a = 0x9E3779B9
    b = 0x9E3779B9
    c = 0xABCDEF00

    v1 = 0
    v2 = len(arr)

    while v2 >= 12:
        a = u32(a + struct.unpack_from("<I", arr, v1)[0])
        b = u32(b + struct.unpack_from("<I", arr, v1 + 4)[0])
        c = u32(c + struct.unpack_from("<I", arr, v1 + 8)[0])

        a, b, c = mix32_1(a, b, c)

        v1 += 12
        v2 -= 12

    c = u32(c + len(arr))

    if v2 == 11:
        c = u32(c + (arr[v1 + 10] << 24))
        v2 = 10
    if v2 == 10:
        c = u32(c + (arr[v1 + 9] << 16))
        v2 = 9
    if v2 == 9:
        c = u32(c + (arr[v1 + 8] << 8))
        v2 = 8
    if v2 == 8:
        b = u32(b + (arr[v1 + 7] << 24))
        v2 = 7
    if v2 == 7:
        b = u32(b + (arr[v1 + 6] << 16))
        v2 = 6
    if v2 == 6:
        b = u32(b + (arr[v1 + 5] << 8))
        v2 = 5
    if v2 == 5:
        b = u32(b + arr[v1 + 4])
        v2 = 4
    if v2 == 4:
        a = u32(a + (arr[v1 + 3] << 24))
        v2 = 3
    if v2 == 3:
        a = u32(a + (arr[v1 + 2] << 16))
        v2 = 2
    if v2 == 2:
        a = u32(a + (arr[v1 + 1] << 8))
        v2 = 1
    if v2 == 1:
        a = u32(a + arr[v1])

    return mix32_2(a, b, c)


def byteswap_u32(x: int) -> int:
    return (
        ((x & 0x000000FF) << 24) |
        ((x & 0x0000FF00) << 8)  |
        ((x & 0x00FF0000) >> 8)  |
        ((x & 0xFF000000) >> 24)
    )

def normalize_vlt_candidates(value: int):
    """
    Returns both possible VLT identities for lookup:
    - native
    - byte-swapped
    """
    swapped = byteswap_u32(value)
    return value, swapped
# ================= RUNTIME HASH TABLES =================

VLT_MEM  = {}
VLT_FILE = {}
BIN_MEM  = {}
BIN_FILE = {}

hash_list_path = os.path.join(app_dir(), "hashes_main.txt")
if os.path.exists(hash_list_path):
    with open(hash_list_path, "r", encoding="utf-8") as f:
        for line in f:
            name = line.strip()
            if not name:
                continue

            # VLT (this is the OLD WORKING logic)
            vlt_mem  = vlt_hash_32(name)
            vlt_file = byteswap_u32(vlt_mem)

            VLT_MEM.setdefault(vlt_mem, name)
            VLT_FILE.setdefault(vlt_file, name)

            # BIN
            bin_mem  = bin_hash_32(name)
            bin_file = byteswap_u32(bin_mem)

            BIN_MEM.setdefault(bin_mem, name)
            BIN_FILE.setdefault(bin_file, name)

# ================= UI SETUP =================

customtkinter.deactivate_automatic_dpi_awareness()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Hash-Raider v2.0")
root.geometry("525x235")
root.resizable(False, False)


def center_window(win):
    win.update_idletasks()

    width = win.winfo_width()
    height = win.winfo_height()

    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()

    x = (screen_w // 2) - (width // 2)
    y = (screen_h // 2) - (height // 2)

    win.geometry(f"{width}x{height}+{x}+{y}")

icon_path = os.path.join(app_dir(), "nfs.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

frame = ctk.CTkFrame(root, fg_color="transparent")
frame.pack(fill="both", expand=True, padx=(8,8), pady=12)

# ================= STATUS =================

status_l = ctk.CTkLabel(root, text="", font=FONT_FIELD, text_color=FIELD_HIGHLIGHT_COLOR)
status_r = ctk.CTkLabel(root, text="", font=FONT_FIELD)

status_l.place(relx=0.48, y=220, anchor="e")
status_r.place(relx=0.48, y=220, anchor="w")

def show_copied():
    status_l.configure(text="Copied ")
    status_r.configure(text="to clipboard")
    root.after(900, lambda: (status_l.configure(text=""), status_r.configure(text="")))

# ================= TOOLTIP (ONLY IF TRUNCATED) =================

def add_tooltip_if_needed(entry, var):
    f = tkfont.Font(font=FONT_FIELD)
    def on_enter(_):
        text = var.get()
        if not text:
            return
        text_width = f.measure(text)
        entry_width = entry.winfo_width() - 10
        if text_width <= entry_width:
            return
        tooltip = tk.Toplevel(root)
        tooltip.overrideredirect(True)
        tooltip.configure(bg="#222")
        label = tk.Label(tooltip, text=text, fg="white", bg="#222", font=FONT_FIELD)
        label.pack(padx=6, pady=4)
        x = root.winfo_pointerx() + 10
        y = root.winfo_pointery() + 10
        tooltip.geometry(f"+{x}+{y}")
        entry._tooltip = tooltip
    def on_leave(_):
        if hasattr(entry, "_tooltip"):
            entry._tooltip.destroy()
            del entry._tooltip
    entry.bind("<Enter>", on_enter)
    entry.bind("<Leave>", on_leave)

# ================= COPY-ONLY FIELD =================

def output_field(row, col, var, padx=(8, 0)):
    e = ctk.CTkEntry(
        frame,
        textvariable=var,
        font=FONT_FIELD,
        width=210,
        text_color=FIELD_TEXT_COLOR,
        border_color=FIELD_BORDER_COLOR
    )
    e.grid(row=row, column=col, padx=padx, pady=4)
    def on_click(_):
        if not var.get():
            return
        root.clipboard_clear()
        root.clipboard_append(var.get())
        root.update()
        e.configure(text_color=FIELD_HIGHLIGHT_COLOR)
        show_copied()
        root.after(900, lambda: e.configure(text_color=FIELD_TEXT_COLOR))
    e.bind("<Button-1>", on_click)
    e.bind("<Key>", lambda _: "break")
    add_tooltip_if_needed(e, var)
    return e

# ================= VARIABLES =================

hex_var = tk.StringVar()
dec_var = tk.StringVar()

bin_mem_var = tk.StringVar()
bin_file_var = tk.StringVar()
vlt_mem_var = tk.StringVar()
vlt_file_var = tk.StringVar()

updating = False

# ================= LOGIC =================

def resolve(value):
    bin_mem_var.set(BIN_MEM.get(value, ""))
    bin_file_var.set(BIN_FILE.get(value, ""))

    vlt_mem_var.set(VLT_MEM.get(value, ""))
    vlt_file_var.set(VLT_FILE.get(value, ""))

def on_hex_change(*_):
    global updating
    if updating:
        return
    updating = True
    text = hex_var.get().strip().lower()
    try:
        if text.startswith("0x"):
            value = int(text, 16)
        else:
            value = int(text, 16)
        value &= 0xFFFFFFFF
        dec_var.set(str(value))
        resolve(value)
    except:
        dec_var.set("")
        resolve(0)
    updating = False

def on_dec_change(*_):
    global updating
    if updating:
        return
    updating = True
    try:
        value = int(dec_var.get()) & 0xFFFFFFFF
        hex_var.set(f"0x{value:08X}")
        resolve(value)
    except:
        hex_var.set("")
        resolve(0)
    updating = False

hex_var.trace_add("write", on_hex_change)
dec_var.trace_add("write", on_dec_change)

# ================= LAYOUT =================

# HASH
ctk.CTkLabel(frame, text="HASH", font=FONT_LABEL, text_color=FONT_COLOR)\
    .grid(row=0, column=0, sticky="w")

ctk.CTkLabel(frame, text="HEX", font=FONT_FIELD, text_color=FIELD_TEXT_COLOR).grid(row=0, column=1, sticky="w", padx=(14,0))
ctk.CTkLabel(frame, text="DEC", font=FONT_FIELD, text_color=FIELD_TEXT_COLOR).grid(row=0, column=2, sticky="w", padx=(8,0))

ctk.CTkEntry(frame, textvariable=hex_var, font=FONT_INPUT, width=210)\
    .grid(row=1, column=1, padx=(8,0))
ctk.CTkEntry(frame, textvariable=dec_var, font=FONT_INPUT, width=210)\
    .grid(row=1, column=2, padx=(0,0))

# spacer
frame.grid_rowconfigure(2, minsize=30)

# STRING
ctk.CTkLabel(frame, text="STRING", font=FONT_LABEL, text_color=FONT_COLOR)\
    .grid(row=3, column=0, sticky="w")

ctk.CTkLabel(frame, text="BIN", font=FONT_FIELD, text_color=FIELD_TEXT_COLOR).grid(row=3, column=1, sticky="w", padx=(14,0))
ctk.CTkLabel(frame, text="VLT", font=FONT_FIELD, text_color=FIELD_TEXT_COLOR).grid(row=3, column=2, sticky="w", padx=(8,0))

ctk.CTkLabel(frame, text="Memory", font=FONT_FIELD).grid(row=4, column=0, sticky="w")
ctk.CTkLabel(frame, text="File", font=FONT_FIELD).grid(row=5, column=0, sticky="w")

output_field(4, 1, bin_mem_var, padx=(8, 0))
output_field(5, 1, bin_file_var, padx=(8, 0))
output_field(4, 2, vlt_mem_var, padx=(0, 0))
output_field(5, 2, vlt_file_var, padx=(0, 0))

for c in (1, 2):
    frame.grid_columnconfigure(c, weight=1)


root.after(0, lambda: center_window(root))
root.mainloop()

