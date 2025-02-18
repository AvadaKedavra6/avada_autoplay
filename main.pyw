import tkinter as tk
from tkinter import filedialog, messagebox
import keyboard
import time
import threading
import re

class DagAutoPlay:
    def __init__(self, root):
        self.root = root
        self.root.title("Dagon Autoplay - Roblox")
        self.notes = []
        self.running = False
        self.bpm = 120
        self.delay = 60 / self.bpm
        self.hotkey = "f6"

        self.special_keys = {
            '!': ('shift', '1'),
            '%': ('shift', '5'),
            ':': ('shift', ';'),
            '*': ('shift', '8'),
            '(': ('shift', '9'),
            ')': ('shift', '0'),
            '[': ('[',),
            ']': (']',),
            '-': ('-',),
            '–': ('-',),
            ' ': ('space',),
        }

        # UI
        self.label = tk.Label(root, text="Dagon Autoplay", font=("Arial", 16))
        self.label.pack(pady=10)

        self.load_button = tk.Button(root, text="Load a sheets", command=self.load_notes, font=("Arial", 12))
        self.load_button.pack(pady=10)

        self.start_button = tk.Button(root, text=f"Start (Hotkey: {self.hotkey.upper()})", command=self.toggle_autoplay, font=("Arial", 12), state=tk.DISABLED)
        self.start_button.pack(pady=10)

        self.status_label = tk.Label(root, text="Status : Waiting a file", font=("Arial", 12))
        self.status_label.pack(pady=10)

        self.status_hotkey = tk.Label(root, text=f"Press {self.hotkey.upper()} for start/stop the autoplay !", font=("Arial", 10), fg="gray")
        self.status_hotkey.pack(pady=5)

        threading.Thread(target=self.listen_hotkey, daemon=True).start()

    def load_notes(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    lines = file.read().splitlines()

                bpm_line = lines[0]
                match = re.match(r"BPM=(\d+)", bpm_line)
                if match:
                    self.bpm = int(match.group(1))
                    self.delay = 60 / self.bpm
                    self.notes = lines[1:]
                    self.status_label.config(text=f"Status : {len(self.notes)} lines loaded and {self.bpm} BPM")
                    self.start_button.config(state=tk.NORMAL)
                else:
                    raise ValueError("The file must be start with 'BPM=<valeur>'.")

            except Exception as e:
                messagebox.showerror("Error", f"Error with the file : {e}")

    def toggle_autoplay(self):
        if self.running:
            self.stop_autoplay()
        else:
            self.start_autoplay()

    def start_autoplay(self):
        if not self.notes:
            messagebox.showwarning("Warning", "No file loaded !")
            return

        self.running = True
        self.status_label.config(text="Status : Autoplay is started...")

        threading.Thread(target=self.play_notes, daemon=True).start()

    def play_notes(self):
        def process_chord(chord):
            for char in chord:
                if char in self.special_keys:

                    modifiers = self.special_keys[char][:-1]
                    main_key = self.special_keys[char][-1]

                    for mod in modifiers:
                        keyboard.press(mod)

                    keyboard.press(main_key)

                    for mod in modifiers:
                        keyboard.release(mod)

                    keyboard.release(main_key)
                else:
                    if char.isupper():
                        keyboard.press('shift')
                    keyboard.press(char.lower())
                    if char.isupper():
                        keyboard.release('shift')
            time.sleep(self.delay)
            for char in chord:
                if char in self.special_keys:
                    main_key = self.special_keys[char][-1]
                    keyboard.release(main_key)
                else:
                    keyboard.release(char.lower())

        for line in self.notes:
            if not self.running:
                break

            patterns = re.findall(r"\[.*?\]|–+|[^\s\[\]-]+", line)

            for pattern in patterns:
                if not self.running:
                    break

                if pattern.startswith("[") and pattern.endswith("]"):
                    keys = pattern[1:-1]
                    process_chord(keys)

                elif pattern == "–":
                    time.sleep(self.delay)

                elif len(pattern) == 1:
                    if pattern in self.special_keys:
                        modifiers = self.special_keys[pattern][:-1]
                        main_key = self.special_keys[pattern][-1]

                        for mod in modifiers:
                            keyboard.press(mod)

                        keyboard.press(main_key)

                        for mod in modifiers:
                            keyboard.release(mod)

                        keyboard.release(main_key)
                    else:
                        if pattern.isupper():
                            keyboard.press('shift')
                            keyboard.press_and_release(pattern.lower())
                            keyboard.release('shift')
                        else:
                            keyboard.press_and_release(pattern)
                    time.sleep(self.delay)

                else:
                    try:
                        if pattern in self.special_keys:

                            modifiers = self.special_keys[pattern][:-1]
                            main_key = self.special_keys[pattern][-1]

                            for mod in modifiers:
                                keyboard.press(mod)

                            keyboard.press(main_key)

                            for mod in modifiers:
                                keyboard.release(mod)

                            keyboard.release(main_key)
                        else:
                            keyboard.press_and_release(pattern.lower())
                    except ValueError:
                        print(f"Invalid key: {pattern}")
                    time.sleep(self.delay)

        if self.running:
            self.running = False
            self.status_label.config(text="Status : Finished")
            self.ask_restart()

    def stop_autoplay(self):
        self.running = False
        self.status_label.config(text="Status : Stopped")

    def ask_restart(self):
        answer = messagebox.askyesno("Autoplay finished", "Do you want to restart this file ?")
        if answer:
            self.start_autoplay()
        else:
            self.status_label.config(text="Status : Waiting a file")

    def listen_hotkey(self):
        while True:
            keyboard.wait(self.hotkey)
            self.toggle_autoplay()


if __name__ == "__main__":
    root = tk.Tk()
    app = DagAutoPlay(root)
    root.mainloop()