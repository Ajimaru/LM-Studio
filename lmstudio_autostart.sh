#!/usr/bin/env bash
set -e

# === Logdatei im aktuellen Verzeichnis ===
LOGFILE="$(pwd)/lmstudio_autostart.log"
exec > >(sed 's/\x1b\[[0-9;]*m//g' > "$LOGFILE") 2>&1

# === Einstellungen ===
APPDIR="/home/robby/Apps"
SCRIPT_DIR="$APPDIR/LM-Studio"
LMSTUDIO_APPIMAGE=$(ls -t "$APPDIR"/LM-Studio-*.AppImage | head -n 1)
LMS_CLI="/home/robby/.lmstudio/bin/lms"
GPU="1.0"
MAX_WAIT=30
INTERVAL=1

# === Modellname aus Argument oder leer ===
MODEL="${1:-}"

export LMSTUDIO_DISABLE_AUTO_LAUNCH=true

if [ ! -f "$LMSTUDIO_APPIMAGE" ]; then
    echo "❌ Keine LM Studio AppImage gefunden in $APPDIR"
    exit 1
fi

echo "$(date '+%Y-%m-%d %H:%M:%S') 🚀 Starte LM Studio GUI: $LMSTUDIO_APPIMAGE"
"$LMSTUDIO_APPIMAGE" &

echo "$(date '+%Y-%m-%d %H:%M:%S') 🔍 Warte auf LM Studio-Fenster..."
SECONDS_WAITED=0
WINDOW_ID=""

while [ "$SECONDS_WAITED" -lt "$MAX_WAIT" ]; do
    WINDOW_ID=$(xdotool search --onlyvisible --name "LM Studio" | head -n 1)
    if [ -n "$WINDOW_ID" ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') ✅ Fenster gefunden: $WINDOW_ID – minimiere..."
        xdotool windowminimize "$WINDOW_ID"
        break
    fi
    sleep "$INTERVAL"
    SECONDS_WAITED=$((SECONDS_WAITED + INTERVAL))
done

if [ -z "$WINDOW_ID" ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') ⚠️ Fenster nicht gefunden – Minimierung übersprungen."
fi

echo "$(date '+%Y-%m-%d %H:%M:%S') ⏳ Warte 10 Sekunden, bis LM Studio bereit ist..."
sleep 10

# === Modell laden, wenn übergeben ===
if [ -n "$MODEL" ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') 📦 Lade Modell: $MODEL ..."
    if "$LMS_CLI" load "$MODEL" --gpu="$GPU"; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') ✅ Modell geladen!"
        notify-send -i dialog-information -t 5000 "LM Studio" "✅ Modell '$MODEL' erfolgreich geladen!"
    else
        echo "$(date '+%Y-%m-%d %H:%M:%S') ❌ Modell '$MODEL' konnte nicht geladen werden – überspringe."
        MODEL="fehler-modell"
    fi
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') ℹ️ Kein Modell übergeben – überspringe Laden."
    MODEL="kein-modell"
fi

# === Starte Tray-Monitor mit Modellname (auch Platzhalter) ===
echo "$(date '+%Y-%m-%d %H:%M:%S') 🐍 Starte Tray-Monitor: $SCRIPT_DIR/lmstudio_tray.py mit Modell '$MODEL'"
python3 "$SCRIPT_DIR/lmstudio_tray.py" "$MODEL" &

