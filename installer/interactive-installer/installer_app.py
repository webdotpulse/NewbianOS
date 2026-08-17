"""
NewbianOS Interactive Installer Application Launcher
"""

import os
import sys
import webbrowser

INSTALLER_HTML = os.path.abspath(os.path.join(os.path.dirname(__file__), "installer_ui.html"))

def launch_installer():
    print("======================================================================")
    print("⚡ Launching NewbianOS 13 'Nexus' Interactive Installer...")
    print("======================================================================")

    # Check for PyQt6 / PySide6 WebEngine
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtWebEngineWidgets import QWebEngineView
        from PyQt6.QtCore import QUrl

        app = QApplication(sys.argv)
        view = QWebEngineView()
        view.setWindowTitle("NewbianOS Interactive Installer")
        view.load(QUrl.fromLocalFile(INSTALLER_HTML))
        view.resize(1000, 660)
        view.show()
        sys.exit(app.exec())
    except ImportError:
        pass

    # Chromium / Chrome in app mode
    for c in ["google-chrome", "chromium", "google-chrome-stable", "x-www-browser"]:
        if os.system(f"which {c} > /dev/null 2>&1") == 0:
            cmd = f"{c} --app=file://{INSTALLER_HTML} --window-size=1000,660 &"
            os.system(cmd)
            return

    webbrowser.open(f"file://{INSTALLER_HTML}")

if __name__ == "__main__":
    launch_installer()
