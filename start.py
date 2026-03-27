import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
import os


class StartApp(tk.Tk):
    def __init__(self):    
        super().__init__()


        self.title("Taxi Booking System")
        self.state('zoomed') 
        self.attributes('-fullscreen', False) 
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        self.geometry(f"{screen_width}x{screen_height}")
        self.configure(bg="#2C1195")
        self.canvas = Canvas(self, width=screen_width, height=screen_height, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.start_color = "#85C1E9"
        self.end_color = "#2E86C1"
        self.create_gradient()

        left_frame = tk.Frame(self.canvas, bg="snow", width=800)
        left_frame.place(relx=0, rely=0, relheight=1, relwidth=0.4)
        try:
            logo_image = Image.open("logo.png")
            logo_photo = ImageTk.PhotoImage(logo_image)
            logo_label = tk.Label(left_frame, image=logo_photo, bg="snow")
            logo_label.image = logo_photo
            logo_label.pack(pady=(40, 10))
        except:
            tk.Label(
                left_frame,
                text="🚕",
                font=("Helvetica", 80),
                bg="snow",
                fg="#000000"
            ).pack(pady=(40, 10))

        self.title_label = tk.Label(
            left_frame,
            text="My Cab",
            font=("Helvetica", 24, "bold"),
            fg="black",
            bg="snow"
        )
        self.title_label.pack(pady=(10, 20))
        self.animate_title_text()

        right_frame = tk.Frame(self.canvas, bg="snow")
        right_frame.place(relx=0.4, rely=0, relheight=1, relwidth=0.6)

        try:
            taxi_image = Image.open("taxi.png")
            taxi_photo = ImageTk.PhotoImage(taxi_image)
            taxi_label = tk.Label(right_frame, image=taxi_photo, bg="#FFD801")
            taxi_label.image = taxi_photo
            taxi_label.place(relx=0.5, rely=0.4, anchor="center")
        except:
            tk.Label(
                right_frame,
                text="🚖\nTAXI",
                font=("Helvetica", 50, "bold"),
                bg="#FFD801",
                fg="#000000",
                justify="center"
            ).place(relx=0.5, rely=0.4, anchor="center")

        self.start_button = tk.Button(
            right_frame,
            text="Start",
            width=15,
            height=2,
            font=("Arial", 16),
            fg="white",
            bg="black",
            relief="flat",
            command=self.start_action
        )
        self.start_button.place(relx=0.5, rely=0.85, anchor="center")
        self.add_button_hover_effect(self.start_button)

    def create_gradient(self):
        self.canvas.delete("gradient")
        r1, g1, b1 = self.hex_to_rgb(self.start_color)
        r2, g2, b2 = self.hex_to_rgb(self.end_color)
        
        canvas_height = self.canvas.winfo_height() if self.canvas.winfo_height() > 1 else 600
        
        steps = canvas_height
        for i in range(steps):
            r = int(r1 + (r2 - r1) * (i / steps))
            g = int(g1 + (g2 - g1) * (i / steps))
            b = int(b1 + (b2 - b1) * (i / steps))
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_line(0, i, self.winfo_width(), i, fill=color, tags="gradient")
        self.start_color, self.end_color = self.end_color, self.start_color
        self.after(50, self.create_gradient)

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def animate_title_text(self):
        current_font = self.title_label.cget("font")
        if isinstance(current_font, str):
            current_size = int(current_font.split()[1])
        else:
            current_size = current_font[1]
        
        new_size = 24 if current_size > 24 else 26
        self.title_label.config(font=("Helvetica", new_size, "bold"))
        self.after(500, self.animate_title_text)

    def add_button_hover_effect(self, button):
        def on_enter(e):
            button.config(bg="slategrey", fg="#FFD801")

        def on_leave(e):
            button.config(bg="black", fg="white")

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def start_action(self):
        self.destroy()
        from login import LoginPage
        new_root = tk.Tk()
        LoginPage(new_root)
        new_root.mainloop()


if __name__ == "__main__":
    try:
        from database_setup import create_database
        create_database()
    except Exception as e:
        print(f"Note: {e}")
    

    app = StartApp()
    app.mainloop()