#!/usr/bin/env python3
import os
import subprocess
import tkinter as tk
from PIL import Image, ImageTk
import tempfile
import cairosvg

DESKTOP_DIRS = [
    '/usr/share/applications',
    os.path.expanduser('~/.local/share/applications'),
    '/var/lib/flatpak/exports/share/applications',
    '/var/lib/snapd/desktop/applications'
]

ICON_EXTS = ['png', 'svg', 'xpm', 'jpg', 'jpeg', 'bmp', 'gif']

# ---------- Icon theme handling ----------
def get_current_icon_theme():
    """Get current XFCE icon theme name."""
    try:
        theme = subprocess.check_output([
            "xfconf-query", "-c", "xsettings", "-p", "/Net/IconThemeName"
        ]).decode().strip()
        print(f"[DEBUG] Current icon theme: {theme}")
        return theme
    except subprocess.CalledProcessError:
        print("[DEBUG] Could not get icon theme, falling back to 'hicolor'")
        return "hicolor"

def get_icon_search_paths(theme):
    """Get icon search paths for the given theme."""
    paths = []
    xdg_data_dirs = os.environ.get("XDG_DATA_DIRS", "/usr/local/share:/usr/share").split(":")
    xdg_data_home = os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))

    for base in [xdg_data_home] + xdg_data_dirs:
        theme_dir = os.path.join(base, "icons", theme)
        if os.path.exists(theme_dir):
            paths.append(theme_dir)

    for base in [xdg_data_home] + xdg_data_dirs:
        hicolor_dir = os.path.join(base, "icons", "hicolor")
        if os.path.exists(hicolor_dir):
            paths.append(hicolor_dir)

    if os.path.exists("/usr/share/pixmaps"):
        paths.append("/usr/share/pixmaps")

    print(f"[DEBUG] Icon search paths: {paths}")
    return paths

def search_icon(icon_name, paths):
    """Search for an icon by name in all paths."""
    for base in paths:
        for root, _, files in os.walk(base):
            for ext in ICON_EXTS:
                candidate = f"{icon_name}.{ext}"
                if candidate in files:
                    return os.path.join(root, candidate)
    return None

# ---------- Window & desktop file handling ----------
def get_running_windows():
    windows = []
    try:
        output = subprocess.check_output(['wmctrl', '-lx']).decode()
    except subprocess.CalledProcessError:
        return windows

    for line in output.splitlines():
        parts = line.split(None, 4)
        if len(parts) < 5:
            continue
        win_id, wm_class_full, _, _, win_name = parts
        exe_name = wm_class_full.split('.')[-1].lower()
        windows.append((win_id, exe_name, win_name))
    return windows

def extract_last_word_after_dash(win_name):
    """If a dash exists, take the last word after it."""
    original = (win_name or "").strip()
    name = " ".join(original.split())
    print(f"[DEBUG] Raw window name: '{original}' -> normalized: '{name}'")

    for sep in ('—', '–', '-'):
        if sep in name:
            segment = name.rsplit(sep, 1)[-1].strip()
            words = segment.split()
            last_word = words[-1] if words else segment
            print(f"[DEBUG] Found dash '{sep}'. Segment: '{segment}', Last word: '{last_word}'")
            return last_word
    print("[DEBUG] No dash found. Using full name.")
    return name

def find_desktop_file(name_guess):
    target = name_guess.lower().replace(' ', '')
    for directory in DESKTOP_DIRS:
        if not os.path.exists(directory):
            continue
        for file in os.listdir(directory):
            if not file.endswith('.desktop'):
                continue
            if target in file.lower().replace(' ', ''):
                return os.path.join(directory, file)
    return None

def read_icon_from_desktop(desktop_file):
    if not desktop_file:
        return None
    try:
        with open(desktop_file, 'r', errors='ignore') as f:
            for line in f:
                if line.startswith('Icon='):
                    icon_name = line.strip().split('=',1)[1]
                    print(f"[DEBUG] Desktop file '{desktop_file}' Icon= '{icon_name}'")
                    return icon_name
    except Exception as e:
        print(f"[DEBUG] Error reading desktop file '{desktop_file}': {e}")
    return None

# ---------- Icon resolution ----------
def build_icon_candidates(desktop_file, exe_name, last_word):
    """
    Build a prioritized list of icon candidates:
      1) Icon= from .desktop
      2) WM_CLASS exe
      3) Last word after dash
      4) Individual words from last_word if no icon found
    """
    candidates = []
    icon_from_desktop = read_icon_from_desktop(desktop_file)
    if icon_from_desktop:
        candidates.append(icon_from_desktop)
    if exe_name:
        candidates.append(exe_name)
    if last_word:
        candidates.append(last_word)

    # Lowercase and no-space variants
    extra = []
    for s in candidates:
        if not s:
            continue
        s2 = s.lower()
        s3 = s2.replace(' ', '')
        if '.' in s2:
            extra.append(s2.split('.')[-1])
        extra.extend([s2, s3])

    # Deduplicate while preserving order
    seen = set()
    all_cands = []
    for c in candidates + extra:
        if c and c not in seen:
            seen.add(c)
            all_cands.append(c)

    # If no icon found for these, add individual words from last_word
    if last_word:
        words = last_word.split()
        for w in words:
            w_lower = w.lower()
            if w_lower not in seen:
                seen.add(w_lower)
                all_cands.append(w_lower)

    print(f"[DEBUG] Icon candidates (final): {all_cands}")
    return all_cands

def get_icon_path(desktop_file, exe_name, last_word, search_paths):
    for cand in build_icon_candidates(desktop_file, exe_name, last_word):
        found = search_icon(cand, search_paths)
        print(f"[DEBUG] Trying '{cand}' -> {'FOUND: ' + found if found else 'not found'}")
        if found:
            return found
    return None

# ---------- Icon loading ----------
def load_icon(icon_path):
    if not icon_path or not os.path.exists(icon_path):
        return Image.new('RGB', (64,64), color='gray')
    ext = os.path.splitext(icon_path)[1].lower()
    if ext == '.svg':
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            cairosvg.svg2png(url=icon_path, write_to=tmp.name)
            img = Image.open(tmp.name)
        os.unlink(tmp.name)
        return img.resize((64,64))
    else:
        try:
            return Image.open(icon_path).resize((64,64))
        except:
            return Image.new('RGB', (64,64), color='gray')

# ---------- Window focusing ----------
def focus_window(win_id):
    subprocess.call(['wmctrl', '-ia', win_id])

# ---------- Main ----------
def main():
    theme = get_current_icon_theme()
    search_paths = get_icon_search_paths(theme)
    windows = get_running_windows()
    print(f"[DEBUG] Found {len(windows)} running windows.")

    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.configure(bg='black')
    root.title("Running Apps")

    # Container for absolute positioning
    area = tk.Frame(root, bg='black')
    area.pack(fill='both', expand=True)

    icons = []

    screen_width = root.winfo_screenwidth()
    padding = 12
    x = padding
    y = padding
    row_height = 0

    print(f"[DEBUG] Screen width: {screen_width}")

    for win_id, exe, win_name in windows:
        last_word = extract_last_word_after_dash(win_name)
        desktop_file = find_desktop_file(last_word)
        icon_path = get_icon_path(desktop_file, exe, last_word, search_paths)

        img = load_icon(icon_path)
        tk_img = ImageTk.PhotoImage(img)
        icons.append(tk_img)

        btn = tk.Button(
            area,
            image=tk_img,
            text=win_name,
            compound='top',
            bg='black',
            fg='white',
            bd=0,
            highlightthickness=0,
            wraplength=96,
            justify='center',
            command=lambda w=win_id: (focus_window(w), root.destroy())  # focus then close GUI
        )
        # Let Tk compute the real required size so we can wrap correctly
        btn.update_idletasks()
        w = btn.winfo_reqwidth()
        h = btn.winfo_reqheight()

        # If next button would overflow, wrap to new row
        if x + w + padding > screen_width:
            print(f"[DEBUG] Wrap row: next button width {w} would exceed {screen_width - x}")
            x = padding
            y += row_height + padding
            row_height = 0

        # Place button and advance cursor
        btn.place(x=x, y=y)
        print(f"[DEBUG] Placed '{win_name}' at x={x}, y={y}, w={w}, h={h}")

        x += w + padding
        if h > row_height:
            row_height = h

    root.mainloop()




if __name__ == "__main__":
    main()
