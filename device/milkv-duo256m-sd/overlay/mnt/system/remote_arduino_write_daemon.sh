#!/bin/sh

WATCH_DIR="/lib/firmware"
TARGET_ELF="${WATCH_DIR}/arduino.elf"
INCOMING_ELF="${WATCH_DIR}/arduino.elf.incoming"

# 無限ループで監視
echo "[remote_arduino_write_daemon] Start monitoring $WATCH_DIR for arduino.elf.incoming..."

while true; do
    if [ -e "$INCOMING_ELF" ]; then
        echo "[remote_arduino_write_daemon] Detected new arduino.elf.incoming. Replacing arduino.elf..."
        echo stop  > /sys/class/remoteproc/remoteproc0/state
        sleep 1
        rm -f "$TARGET_ELF"
        mv "$INCOMING_ELF" "$TARGET_ELF"
        sleep 0.1
        if test -e /usr/bin/burnd; then
            burnd &
            if test -e "$TARGET_ELF"; then
                sleep 2
                echo stop  > /sys/class/remoteproc/remoteproc0/state
                echo start > /sys/class/remoteproc/remoteproc0/state
            fi
        fi
        echo "[remote_arduino_write_daemon] arduino.elf updated and remoteproc restarted."
    fi
    sleep 1
done 
