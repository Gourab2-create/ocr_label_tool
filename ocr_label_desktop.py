#!/usr/bin/env python3
"""
PaddleOCR Label Desktop
Runs the existing annotation interface inside a standalone desktop window.
No Flask, HTTP server, or external browser is started.
"""

import os
import sys
from pathlib import Path

# Snap Code may pass an incomplete private schema directory to child processes.
schema_dir = os.environ.get("GSETTINGS_SCHEMA_DIR")
system_schema_dir = Path("/usr/share/glib-2.0/schemas")
snap_code_dir = Path.home() / "snap" / "code"
if (
    schema_dir
    and snap_code_dir in Path(schema_dir).parents
    and system_schema_dir.is_dir()
):
    os.environ["GSETTINGS_SCHEMA_DIR"] = str(system_schema_dir)

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView


APP_DIR = Path(__file__).resolve().parent
HTML_FILE = APP_DIR / "paddleocr_label.html"


class PaddleOCRLabelDesktop(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OCR Label Desktop")
        self.resize(1500, 900)
        self.setMinimumSize(1000, 650)

        self.browser = QWebEngineView(self)
        self.setCentralWidget(self.browser)

        settings = self.browser.settings()
        settings.setAttribute(settings.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(settings.LocalContentCanAccessRemoteUrls, False)
        settings.setAttribute(settings.JavascriptEnabled, True)

        profile = self.browser.page().profile()
        profile.downloadRequested.connect(self.handle_download)

        if not HTML_FILE.exists():
            QMessageBox.critical(
                self,
                "Missing HTML file",
                f"Could not find:\\n{HTML_FILE}\\n\\nKeep paddleocr_label.html beside this Python file."
            )
            raise FileNotFoundError(HTML_FILE)

        self.browser.load(QUrl.fromLocalFile(str(HTML_FILE)))

    def handle_download(self, download):
        suggested = download.downloadFileName() or "download"
        path, _ = QFileDialog.getSaveFileName(
            self, "Save exported file", str(Path.home() / suggested),
            "All files (*)"
        )
        if not path:
            download.cancel()
            return
        download.setPath(path)
        download.accept()
        self.statusBar().showMessage(f"Saving: {path}", 5000)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("PaddleOCR Label Desktop")
    window = PaddleOCRLabelDesktop()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
