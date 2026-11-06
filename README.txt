PaddleOCR Label Desktop
=======================

This version opens in its own desktop window. It does not start the Python
HTTP server and does not require you to open Firefox/Chrome manually.

Files:
- paddleocr_label_desktop.py : desktop launcher
- paddleocr_label.html       : annotation interface
- logo.jpg                   : header logo   # logo add 
- requirements.txt           : Python dependencies
- run.sh                      : Linux launcher

Ubuntu installation:
    sudo apt update
    sudo apt install python3-pip
    python3 -m pip install -r requirements.txt

Run:
    python3 paddleocr_label_desktop.py

Or:
    chmod +x run.sh
    ./run.sh

Use Open Folder to select your image dataset. If label.txt is inside the
selected folder, the interface will load it automatically. Export/Backup
buttons open a desktop Save dialog.

Annotation edits and verification states are automatically saved in the
application's local browser storage and restored when the same image folder
is opened again. Auto-save does not modify label.txt; use Export Label.txt
to write an updated label file. Text entered in the Text Content editor is
automatically converted to uppercase.

Note: The interface is rendered by Qt WebEngine inside a desktop application
window. No web server or external browser is used. The annotation interface
and its existing controls are retained.
