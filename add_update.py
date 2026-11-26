# Adds one line to updates-data.js and copies your file into the updates folder.
# Put this next to updates.html, open in Thonny (Local Python 3) and press Run.
import datetime, json, re, shutil, webbrowser
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "updates-data.js"
FOLDER = HERE / "updates"
CATS = ["Notice", "Class Routine", "Academic Routine", "Other"]
IMG = (".jpg", ".jpeg", ".png", ".webp", ".gif")
MARK = "window.UPDATES=["


def stop(msg):
    raise SystemExit("STOP: " + msg)


def uniq(stem, ext):
    stem = re.sub(r"[^A-Za-z0-9._-]+", "-", stem).strip("-.") or "file"
    name, n = stem + ext, 2
    while (FOLDER / name).exists():
        name = "%s-%d%s" % (stem, n, ext)
        n += 1
    return name


def need(p):
    p = Path(str(p).strip().strip('"'))
    if not p.is_file():
        stop("file not found: %s" % p)
    return p


def copy(src):
    src = need(src)
    FOLDER.mkdir(exist_ok=True)
    name = uniq(src.stem, src.suffix.lower())
    shutil.copy2(src, FOLDER / name)
    return "updates/" + name


def thumb(src, reuse=""):
    """small copy for the grid (needs Pillow), otherwise reuse or plain copy"""
    src = need(src)
    FOLDER.mkdir(exist_ok=True)
    try:
        from PIL import Image
    except ImportError:
        if src.stat().st_size > 300000:
            print("Tip: big pictures load slowly. Install Pillow once for small thumbnails:")
            print("     Thonny > Tools > Manage packages > search Pillow > Install")
        return reuse or copy(src)
    try:
        im = Image.open(src).convert("RGB")
        im.thumbnail((640, 640))
        name = uniq(src.stem + "-t", ".jpg")
        im.save(FOLDER / name, "JPEG", quality=80, optimize=True)
    except Exception as e:
        stop("could not read the image: %s" % e)
    return "updates/" + name


def add(cat, title, date="", file="", img=""):
    """returns (the new line, list of site files to upload)"""
    if not DATA.exists():
        stop("updates-data.js not found next to this script")
    cat, title = cat.strip(), title.strip()
    if not cat or not title:
        stop("category and title are needed")
    date = date.strip() or datetime.date.today().isoformat()
    try:
        datetime.date.fromisoformat(date)
    except ValueError:
        stop("date must look like 2026-11-27")
    raw = DATA.read_bytes().decode("utf-8")
    k = raw.find(MARK)
    k = raw.find("\n", k) if k >= 0 else -1
    if k < 0:
        stop("could not find window.UPDATES=[ in updates-data.js")
    file, img = file.strip().strip('"'), img.strip().strip('"')
    files, u, i = [], "", ""
    if file:
        if re.match(r"https?:", file, re.I):
            u = file
        else:
            u = copy(file)
            files.append(u)
    if img:
        i = thumb(img)
    elif u and not re.match(r"https?:", file, re.I) and file.lower().endswith(IMG):
        i = thumb(file, u)
    if i:
        files.append(i)
    e = [("d", date), ("c", cat), ("t", title), ("u", u), ("i", i)]
    line = "{" + ",".join('"%s":%s' % (a, json.dumps(b, ensure_ascii=False)) for a, b in e if b) + "},"
    nl = "\r\n" if "\r\n" in raw else "\n"
    raw = raw[:k + 1] + line + nl + raw[k + 1:]
    DATA.write_bytes(raw.encode("utf-8"))
    return line, files


def pick(title):
    try:
        import tkinter as tk
        from tkinter import filedialog
        r = tk.Tk()
        r.withdraw()
        r.attributes("-topmost", True)
        p = filedialog.askopenfilename(title=title, parent=r)
        r.destroy()
        return p or ""
    except Exception:
        return input(title + " (paste a path, Enter to skip): ")


def main():
    print("Add an update")
    for n, c in enumerate(CATS, 1):
        print(" %d  %s" % (n, c))
    s = input("Category number, or type a new one: ").strip()
    cat = CATS[int(s) - 1] if s.isdigit() and 1 <= int(s) <= len(CATS) else s
    title = input("Title: ")
    date = input("Date (Enter = today, or like 2026-11-27): ")
    link = input("Link (paste a URL, or just Enter to pick a file): ").strip()
    file = link or pick("Pick the PDF or image to attach (Cancel = none)")
    auto = file and not link and file.lower().endswith(IMG)
    img = "" if auto else pick("Pick a thumbnail image (Cancel = none)")
    line, files = add(cat, title, date, file, img)
    print("OK: added", line)
    print("Upload to GitHub: updates-data.js" + "".join(", " + f for f in files))
    webbrowser.open((HERE / "updates.html").as_uri())


if __name__ == "__main__":
    main()
