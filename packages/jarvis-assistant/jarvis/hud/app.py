"""
Jarvis Holographic HUD Application Launcher
Opens a frameless, glassmorphic HUD overlay with Wayland layer-shell support.
"""

import asyncio
import os
import sys
import webbrowser

HUD_HTML_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "hologram_ui.html"))

def launch_hud():
    """Launch the HUD interface using available desktop renderers."""
    # Check for PyQt6 / PySide6 WebEngine
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtWebEngineWidgets import QWebEngineView
        from PyQt6.QtCore import QUrl, Qt

        app = QApplication(sys.argv)
        view = QWebEngineView()
        view.setWindowTitle("Jarvis Multimodal HUD")
        view.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        view.setStyleSheet("background: transparent;")
        view.load(QUrl.fromLocalFile(HUD_HTML_PATH))
        view.resize(1100, 680)
        view.show()
        sys.exit(app.exec())
    except ImportError:
        pass

    # Fallback to Chromium / Chrome in app mode
    chrome_bins = ["google-chrome", "chromium", "google-chrome-stable"]
    for c in chrome_bins:
        if os.system(f"which {c} > /dev/null 2>&1") == 0:
            cmd = f"{c} --app=file://{HUD_HTML_PATH} --window-size=1100,680 --ozone-platform-hint=auto &"
            os.system(cmd)
            return

    # Fallback to default browser
    webbrowser.open(f"file://{HUD_HTML_PATH}")

if __name__ == "__main__":
    launch_hud()
