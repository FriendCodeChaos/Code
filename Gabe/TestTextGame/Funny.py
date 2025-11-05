import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import urllib.request
import os
import random
import threading

# --- Download the cat GIF if not exists ---
GIF_URL = "https://thvnext.bing.com/th/id/OIP.qfvUN78iVb9gtr_x-r9L7QAAAA?o=7&cb=12rm=3&rs=1&pid=ImgDetMain&o=7&rm=3"
GIF_PATH = "cat.gif"
if not os.path.exists(GIF_PATH):
    urllib.request.urlretrieve(GIF_URL, GIF_PATH)

# Keep references to prevent garbage collection
all_frames = []

def run_cats():
    global all_frames
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.attributes("-transparentcolor", "white")
    root.config(bg="white")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")

    canvas = tk.Canvas(root, width=screen_width, height=screen_height,
                       bg="white", highlightthickness=0)
    canvas.pack()

    # Load GIF and frames
    img = Image.open(GIF_PATH).convert("RGBA")
    width, height = img.size
    img = img.resize((width // 3, height // 3), Image.Resampling.LANCZOS)

    pil_frames = [frame.copy() for frame in ImageSequence.Iterator(img)]
    frames = [ImageTk.PhotoImage(frame) for frame in pil_frames]
    all_frames = frames  # keep reference

    class Cat:
        def __init__(self, canvas, pil_frames):
            self.canvas = canvas
            self.pil_frames = pil_frames
            self.num_frames = len(pil_frames)
            self.frame_index = random.randint(0, self.num_frames - 1)
            self.rotation = 0  # current rotation angle
            self.width, self.height = pil_frames[0].size

            self.tk_image = ImageTk.PhotoImage(self.pil_frames[self.frame_index])
            self.id = canvas.create_image(
                random.randint(0, screen_width - self.width),
                random.randint(0, screen_height - self.height),
                image=self.tk_image, anchor='nw'
            )

            # Movement speed
            self.dx = random.choice([-12, -10, -8, 8, 10, 12])
            self.dy = random.choice([-12, -10, -8, 8, 10, 12])

            # Slow rotation
            self.rotate_delay = random.randint(4, 8)
            self.rotate_counter = 0

            # Animate GIF frames slowly
            self.frame_delay = random.randint(2, 5)
            self.frame_counter = 0

        def move(self):
            # Bounce
            x, y = self.canvas.coords(self.id)
            if x + self.dx <= 0 or x + self.dx + self.width >= screen_width:
                self.dx *= -1
            if y + self.dy <= 0 or y + self.dy + self.height >= screen_height:
                self.dy *= -1
            self.canvas.move(self.id, self.dx, self.dy)

            # Animate GIF
            self.frame_counter += 1
            if self.frame_counter >= self.frame_delay:
                self.frame_index = (self.frame_index + 1) % self.num_frames
                self.frame_counter = 0

            # Rotate slowly
            self.rotate_counter += 1
            if self.rotate_counter >= self.rotate_delay:
                self.rotation = (self.rotation + 5) % 360
                rotated = self.pil_frames[self.frame_index].rotate(self.rotation, expand=True)
                self.tk_image = ImageTk.PhotoImage(rotated)
                self.canvas.itemconfig(self.id, image=self.tk_image)
                self.rotate_counter = 0

    cats = [Cat(canvas, pil_frames) for _ in range(25)]

    def animate():
        for cat in cats:
            cat.move()
        root.after(16, animate)  # ~60 FPS

    animate()
    root.mainloop()

def start_cats():
    threading.Thread(target=run_cats, daemon=True).start()
