# Adds one file or link to the Infos page.
# Put this next to infos.html, open in Thonny (Local Python 3) and press Run.
import datetime, json, re, shutil, webbrowser
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "updates-data.js"
FOLDER = HERE / "updates"
MARK = "window.UPDATES=["


def stop(msg):
    raise SystemExit("STOP: " + msg)


def pick():
    try:
        import tkinter as tk
        from tkinter import filedialog
        r = tk.Tk()
        r.withdraw()
        r.attributes("-topmost", True)
        p = filedialog.askopenfilename(title="Pick the PDF or image", parent=r)
        r.destroy()
        return p or ""
    except Exception:
        return input("Paste the file path: ")


def add(title, file):
    """returns the file or link that the new line points to"""
    title, file = title.strip(), file.strip().strip('"')
    if not title or not file:
        stop("a title and a file or link are needed")
    if not DATA.is_file():
        stop("updates-data.js not found next to this script")
    raw = DATA.read_bytes().decode("utf-8")
    k = raw.find(MARK)
    k = raw.find("\n", k) if k >= 0 else -1
    if k < 0:
        stop("could not find window.UPDATES=[ in updates-data.js")
    if re.match(r"https?:", file, re.I):
        url = file
    else:
        src = Path(file)
        if not src.is_file():
            stop("file not found: %s" % src)
        FOLDER.mkdir(exist_ok=True)
        stem = re.sub(r"[^A-Za-z0-9._-]+", "-", src.stem).strip("-.") or "file"
        ext = src.suffix.lower()
        name, n = stem + ext, 2
        while (FOLDER / name).exists():
            name, n = "%s-%d%s" % (stem, n, ext), n + 1
        shutil.copy2(src, FOLDER / name)
        url = "updates/" + name
    entry = {"d": datetime.date.today().isoformat(), "t": title, "u": url}
    line = json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + ","
    nl = "\r\n" if "\r\n" in raw else "\n"
    DATA.write_bytes((raw[:k + 1] + line + nl + raw[k + 1:]).encode("utf-8"))
    return url


def main():
    title = input("Title: ")
    link = input("Paste a link, or press Enter to pick a file: ").strip()
    url = add(title, link or pick())
    extra = "" if url.lower().startswith("http") else " and " + url
    print("OK: added. Upload to GitHub: updates-data.js" + extra)
    webbrowser.open((HERE / "infos.html").as_uri())


if __name__ == "__main__":
    main()
