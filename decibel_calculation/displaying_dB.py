# save as db_display.py
import threading
import queue
import time
import serial
import tkinter as tk
from tkinter import font

SERIAL_PORT = "COM3"     # change if needed
BAUDRATE = 115200
READ_TIMEOUT = 1         # seconds
REFRESH_MS = 1000        # update GUI every 1000 ms

def serial_reader_thread(port, baud, out_queue, stop_event):
    try:
        ser = serial.Serial(port, baud, timeout=READ_TIMEOUT)
    except Exception as e:
        out_queue.put(("__ERROR__", str(e)))
        return

    while not stop_event.is_set():
        try:
            raw = ser.readline()           # bytes until newline
            if not raw:
                continue
            line = raw.decode(errors="ignore").strip()
            if not line:
                continue
            # try parse float, otherwise ignore
            try:
                val = float(line)
                out_queue.put(("VALUE", val))
            except ValueError:
                # optionally accept comma decimals: "23,4"
                line2 = line.replace(",", ".")
                try:
                    val = float(line2)
                    out_queue.put(("VALUE", val))
                except ValueError:
                    # ignore non-numeric lines
                    out_queue.put(("MSG", line))
        except Exception:
            # keep running on serial read errors
            time.sleep(0.1)
    try:
        ser.close()
    except Exception:
        pass

def main():
    q = queue.Queue(maxsize=1)   # store latest messages (we'll only keep last)
    stop_event = threading.Event()
    t = threading.Thread(target=serial_reader_thread, args=(SERIAL_PORT, BAUDRATE, q, stop_event), daemon=True)
    t.start()

    root = tk.Tk()
    root.title("dB Monitor")

    # Heading
    title_font = font.Font(root=root, size=20, weight="bold")
    title = tk.Label(root, text="Sound Level Meter", font=title_font)
    title.pack(pady=(15, 5))

    # Big font numeric label
    big = font.Font(root=root, size=48, weight="bold")
    label = tk.Label(root, text="--.- dB", font=big, width=10)
    label.pack(padx=20, pady=10)


    info = tk.Label(root, text=f"Port: {SERIAL_PORT} @ {BAUDRATE}  —  Last update: --:--:--")
    info.pack(padx=10, pady=(0,12))

    status = tk.Label(root, text="", fg="orange")
    status.pack()

    latest_val = None
    last_time = None

    def update_gui():
        nonlocal latest_val, last_time
        # drain queue, keep last meaningful value
        while True:
            try:
                typ, payload = q.get_nowait()
            except queue.Empty:
                break
            if typ == "VALUE":
                latest_val = payload
                last_time = time.strftime("%H:%M:%S")
                status.config(text="")
            elif typ == "MSG":
                # optional: show last incoming non-numeric message
                status.config(text=f"msg: {payload}")
            elif typ == "__ERROR__":
                status.config(text=f"serial error: {payload}", fg="red")

        if latest_val is None:
            label.config(text="--.- dB")
            info.config(text=f"Port: {SERIAL_PORT} @ {BAUDRATE}  —  Last update: --:--:--")
        else:
            label.config(text=f"{latest_val:.1f} dB")
            info.config(text=f"Port: {SERIAL_PORT} @ {BAUDRATE}  —  Last update: {last_time}")

        root.after(REFRESH_MS, update_gui)

    def on_close():
        stop_event.set()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.after(100, update_gui)
    root.mainloop()

if __name__ == "__main__":
    main()
