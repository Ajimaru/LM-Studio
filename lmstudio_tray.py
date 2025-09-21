#!/usr/bin/env python3
import gi
import subprocess
import sys
import os
import signal

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

# === Modellname aus Argument oder Default ===
MODEL = sys.argv[1] if len(sys.argv) > 1 else "kein-modell-übergeben"

# === GTK-Iconnamen aus dem Icon Browser ===
ICON_OK = "emblem-default"         # ✅ Modell aktiv
ICON_FAIL = "emblem-unreadable"    # ❌ Modell nicht geladen
ICON_WARN = "dialog-warning"       # ⚠️ Fehlerstatus

# === Pfad zur lms-CLI ===
LMS_CLI = "/home/robby/.lmstudio/bin/lms"

# === Beende andere Instanzen dieses Skripts ===
def kill_existing_instances():
    result = subprocess.run(["pgrep", "-f", "lmstudio_tray.py"], stdout=subprocess.PIPE, text=True)
    pids = [int(pid) for pid in result.stdout.strip().split("\n") if pid.isdigit()]
    current_pid = os.getpid()
    for pid in pids:
        if pid != current_pid:
            try:
                os.kill(pid, signal.SIGTERM)
                print(f"🧹 Beende alte Instanz: PID {pid}")
            except Exception as e:
                print(f"⚠️ Fehler beim Beenden von PID {pid}: {e}")

kill_existing_instances()

class TrayIcon:
    def __init__(self):
        self.status_icon = Gtk.StatusIcon()
        self.status_icon.set_visible(True)
        self.status_icon.set_tooltip_text("LM Studio Monitor")
        self.status_icon.connect("activate", self.on_click)
        self.status_icon.connect("popup-menu", self.on_right_click)

        self.check_model()
        GLib.timeout_add_seconds(10, self.check_model)

    def on_click(self, icon):
        subprocess.run(["notify-send", "LM Studio", f"Modellstatus: {MODEL} wird überwacht"])

    def on_right_click(self, icon, button, time):
        menu = Gtk.Menu()

        open_item = Gtk.MenuItem(label="LM Studio öffnen")
        open_item.connect("activate", self.open_lm_studio)
        menu.append(open_item)

        menu.append(Gtk.SeparatorMenuItem())

        quit_item = Gtk.MenuItem(label="Tray beenden")
        quit_item.connect("activate", self.quit_app)
        menu.append(quit_item)

        menu.show_all()
        menu.popup(None, None, None, None, button, time)

    def open_lm_studio(self, widget):
        try:
            subprocess.run(["xdg-open", "lmstudio://"], check=False)
        except Exception as e:
            subprocess.run(["notify-send", "Fehler", f"LM Studio konnte nicht geöffnet werden: {e}"])

    def quit_app(self, widget):
        Gtk.main_quit()

    def check_model(self):
        try:
            result = subprocess.run([LMS_CLI, "ps"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
            if result.returncode == 0:
                if MODEL in result.stdout:
                    self.status_icon.set_from_icon_name(ICON_OK)
                    self.status_icon.set_tooltip_text(f"✅ Modell aktiv: {MODEL}")
                else:
                    lines = result.stdout.strip().split('\n')
                    if len(lines) > 1:
                        loaded_models = [line.split()[1] if len(line.split()) > 1 else 'Unbekannt' for line in lines[1:]]
                        tooltip = f"⚠️ Anderes/kein Modell geladen (erwartet: {MODEL})\nGeladen: {', '.join(loaded_models[:3])}"
                    else:
                        tooltip = f"⚠️ Anderes/kein Modell geladen (erwartet: {MODEL})"
                    self.status_icon.set_from_icon_name(ICON_WARN)
                    self.status_icon.set_tooltip_text(tooltip)
            else:
                self.status_icon.set_from_icon_name(ICON_FAIL)
                self.status_icon.set_tooltip_text("❌ LM Studio läuft nicht")
        except subprocess.TimeoutExpired:
            self.status_icon.set_from_icon_name(ICON_WARN)
            self.status_icon.set_tooltip_text("⚠️ Timeout bei Statusprüfung")
        except Exception as e:
            self.status_icon.set_from_icon_name(ICON_FAIL)
            self.status_icon.set_tooltip_text(f"❌ Fehler beim Prüfen: {str(e)}")
        return True

TrayIcon()
Gtk.main()

