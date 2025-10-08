"""
Brownian Motion Simulator - Modern UI
Simulasi Gerak Brown dengan GUI Modern & Interaktif
Python Version with Tkinter GUI

=== INSTALLATION GUIDE ===

LINUX (Ubuntu/Debian):
    sudo apt-get update
    sudo apt-get install python3-tk

LINUX (Fedora/RedHat):
    sudo dnf install python3-tkinter

LINUX (Arch):
    sudo pacman -S tk

macOS:
    # Tkinter biasanya sudah included dengan Python dari python.org
    # Jika belum, install via Homebrew:
    brew install python-tk

Windows:
    # Tkinter biasanya sudah included dengan Python installer dari python.org
    # Jika belum ada, reinstall Python dan centang "tcl/tk and IDLE"

=== HOW TO RUN ===
    python brownian_motion.py

atau

    python3 brownian_motion.py

========================
"""

import tkinter as tk
from tkinter import ttk
import random
import math
import time

class Particle:
    def __init__(self, canvas_width, canvas_height):
        self.x = random.uniform(30, canvas_width - 30)
        self.y = random.uniform(30, canvas_height - 30)
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.radius = random.uniform(4, 7)
        self.color = random.choice([
            '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A',
            '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2',
            '#FF9FF3', '#54A0FF', '#48DBFB', '#1DD1A1'
        ])
        self.trail = []
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

    def update(self, speed):
        # Brownian motion: random walk
        self.vx += random.uniform(-0.5, 0.5)
        self.vy += random.uniform(-0.5, 0.5)

        # Limit speed
        max_speed = speed * 0.5
        current_speed = math.sqrt(self.vx**2 + self.vy**2)
        if current_speed > max_speed:
            self.vx = (self.vx / current_speed) * max_speed
            self.vy = (self.vy / current_speed) * max_speed

        # Update position
        self.x += self.vx
        self.y += self.vy

        # Bounce off walls with damping
        if self.x < self.radius or self.x > self.canvas_width - self.radius:
            self.vx *= -0.8
            self.x = max(self.radius, min(self.x, self.canvas_width - self.radius))

        if self.y < self.radius or self.y > self.canvas_height - self.radius:
            self.vy *= -0.8
            self.y = max(self.radius, min(self.y, self.canvas_height - self.radius))

        # Update trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > 30:
            self.trail.pop(0)

class ModernButton(tk.Canvas):
    def __init__(self, parent, text, command, bg_color, hover_color, **kwargs):
        super().__init__(parent, **kwargs)
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text = text

        self.config(
            bg=bg_color,
            highlightthickness=0,
            cursor="hand2"
        )

        self.bind("<Button-1>", lambda e: self.command())
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

        self.draw_button()

    def draw_button(self):
        self.delete("all")
        width = self.winfo_reqwidth() or 120
        height = self.winfo_reqheight() or 45

        # Rounded rectangle background
        radius = 10
        self.create_rounded_rect(0, 0, width, height, radius, fill=self.bg_color)

        # Text
        self.create_text(
            width/2, height/2,
            text=self.text,
            fill="white",
            font=("Segoe UI", 11, "bold")
        )

    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def on_enter(self, e):
        self.config(bg=self.hover_color)
        for item in self.find_all():
            if self.type(item) == "polygon":
                self.itemconfig(item, fill=self.hover_color)

    def on_leave(self, e):
        self.config(bg=self.bg_color)
        for item in self.find_all():
            if self.type(item) == "polygon":
                self.itemconfig(item, fill=self.bg_color)

class BrownianMotionSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("🔬 Simulasi Gerak Brown")
        self.root.geometry("1400x900")

        # Modern gradient background
        self.root.configure(bg="#1a1a2e")

        # Variables
        self.particles = []
        self.is_running = False
        self.show_trails = True
        self.num_particles = 20
        self.speed = 3
        self.total_steps = 0
        self.start_time = None
        self.particle_count = 0

        # Show splash screen first
        self.show_splash_screen()

    def show_splash_screen(self):
        """Display welcome splash screen with introduction"""
        splash = tk.Toplevel(self.root)
        splash.title("Selamat Datang")
        splash.geometry("700x600")
        splash.configure(bg="#0f1419")
        splash.resizable(False, False)

        # Center the splash screen
        splash.update_idletasks()
        x = (splash.winfo_screenwidth() // 2) - (700 // 2)
        y = (splash.winfo_screenheight() // 2) - (600 // 2)
        splash.geometry(f"700x600+{x}+{y}")

        # Remove window decorations for modern look
        splash.overrideredirect(True)

        # Main container
        container = tk.Frame(splash, bg="#0f1419")
        container.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

        # Animated icon
        icon_label = tk.Label(
            container,
            text="🔬",
            font=("Arial", 80),
            bg="#0f1419",
            fg="#667eea"
        )
        icon_label.pack(pady=(20, 10))

        # Title
        title = tk.Label(
            container,
            text="SIMULASI GERAK BROWN",
            font=("Segoe UI", 28, "bold"),
            fg="#ffffff",
            bg="#0f1419"
        )
        title.pack(pady=(0, 20))

        # Introduction text
        intro_text = """
Selamat datang di Simulasi Gerak Brown!

Gerak Brown adalah fenomena gerakan acak partikel mikroskopis 
yang tersuspensi dalam fluida (cairan atau gas). Gerakan ini 
terjadi akibat tumbukan terus-menerus dengan molekul-molekul 
fluida yang bergerak secara acak.

📚 Sejarah:
Fenomena ini pertama kali diamati oleh botanis Skotlandia 
Robert Brown pada tahun 1827 saat mengamati butiran serbuk 
sari dalam air di bawah mikroskop.

🔬 Signifikansi Ilmiah:
• Bukti eksperimental keberadaan atom dan molekul
• Dasar teori kinetik gas dan mekanika statistik
• Aplikasi dalam fisika, kimia, biologi, dan ekonomi
• Model untuk memahami difusi dan transport molekuler

💡 Dalam simulasi ini:
Setiap partikel berwarna merepresentasikan molekul atau 
partikel koloid yang bergerak secara acak akibat tumbukan 
dengan molekul fluida di sekitarnya.
        """

        intro_label = tk.Label(
            container,
            text=intro_text,
            font=("Segoe UI", 10),
            fg="#9ca3af",
            bg="#0f1419",
            justify=tk.LEFT,
            wraplength=600
        )
        intro_label.pack(pady=(0, 20))

        # Progress bar
        progress_frame = tk.Frame(container, bg="#0f1419")
        progress_frame.pack(fill=tk.X, pady=(10, 20))

        progress_canvas = tk.Canvas(
            progress_frame,
            height=6,
            bg="#1a1a2e",
            highlightthickness=0
        )
        progress_canvas.pack(fill=tk.X)

        # Start button
        start_btn = ModernButton(
            container,
            text="🚀 Mulai Simulasi",
            command=lambda: self.close_splash(splash),
            bg_color="#667eea",
            hover_color="#5568d3",
            width=250,
            height=50
        )
        start_btn.pack(pady=(0, 10))

        # Credits
        credit = tk.Label(
            container,
            text="Dikembangkan untuk pembelajaran Fisika & Kimia",
            font=("Segoe UI", 8),
            fg="#4b5563",
            bg="#0f1419"
        )
        credit.pack()

        # Animate progress bar
        self.animate_progress(progress_canvas, 0)

        # Auto close after 8 seconds if not clicked
        splash.after(8000, lambda: self.close_splash(splash))

    def animate_progress(self, canvas, progress):
        """Animate the loading progress bar"""
        if progress <= 100:
            width = canvas.winfo_width() or 620
            bar_width = (width * progress) / 100

            canvas.delete("all")
            canvas.create_rectangle(
                0, 0, bar_width, 6,
                fill="#667eea",
                outline=""
            )

            self.root.after(30, lambda: self.animate_progress(canvas, progress + 1))

    def close_splash(self, splash):
        """Close splash screen and show main app"""
        splash.destroy()
        self.setup_ui()
        self.init_particles()

    def setup_ui(self):
        # Main container with padding
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Header section
        header_frame = tk.Frame(main_frame, bg="#1a1a2e")
        header_frame.pack(fill=tk.X, pady=(0, 20))

        # Title with emoji
        title = tk.Label(
            header_frame,
            text="🔬 Simulasi Gerak Brown",
            font=("Segoe UI", 36, "bold"),
            fg="#ffffff",
            bg="#1a1a2e"
        )
        title.pack()

        subtitle = tk.Label(
            header_frame,
            text="Gerakan acak partikel seperti molekul dalam fluida",
            font=("Segoe UI", 13),
            fg="#9ca3af",
            bg="#1a1a2e"
        )
        subtitle.pack(pady=(5, 0))

        # Content area
        content_frame = tk.Frame(main_frame, bg="#1a1a2e")
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left side - Canvas
        left_frame = tk.Frame(content_frame, bg="#1a1a2e")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))

        # Canvas with modern styling
        canvas_container = tk.Frame(
            left_frame,
            bg="#2d3748",
            highlightthickness=0
        )
        canvas_container.pack(fill=tk.BOTH, expand=True)

        # Add shadow effect
        shadow_canvas = tk.Canvas(
            canvas_container,
            bg="#1a1a2e",
            highlightthickness=0,
            height=5
        )
        shadow_canvas.pack(fill=tk.X, side=tk.BOTTOM)

        self.canvas = tk.Canvas(
            canvas_container,
            bg="#0f1419",
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

        # Right side - Controls
        right_frame = tk.Frame(content_frame, bg="#1a1a2e", width=350)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        right_frame.pack_propagate(False)

        # Control panels
        self.create_control_panel(right_frame)

        # Bottom info
        info_frame = tk.Frame(main_frame, bg="#1a1a2e")
        info_frame.pack(fill=tk.X, pady=(20, 0))

        info_text = tk.Label(
            info_frame,
            text="💡 Gerak Brown pertama kali diamati oleh Robert Brown (1827) saat mengamati serbuk sari dalam air",
            font=("Segoe UI", 10),
            fg="#6b7280",
            bg="#1a1a2e",
            wraplength=1000,
            justify=tk.LEFT
        )
        info_text.pack()

    def create_control_panel(self, parent):
        # Stats cards
        stats_frame = tk.Frame(parent, bg="#1a1a2e")
        stats_frame.pack(fill=tk.X, pady=(0, 20))

        # Create stat cards
        self.create_stat_card(stats_frame, "Total Steps", "0", "steps", "#667eea")
        self.create_stat_card(stats_frame, "Partikel", "0", "particles", "#4ecdc4")
        self.create_stat_card(stats_frame, "Runtime", "0s", "runtime", "#f093fb")

        # Control section
        control_container = tk.Frame(parent, bg="#2d3748")
        control_container.pack(fill=tk.BOTH, expand=True)

        # Padding inside control container
        control_inner = tk.Frame(control_container, bg="#2d3748")
        control_inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Particle count slider
        self.create_slider_control(
            control_inner,
            "🔵 Jumlah Partikel",
            5, 50, self.num_particles,
            self.update_particle_count,
            "particle"
        )

        # Speed slider
        self.create_slider_control(
            control_inner,
            "⚡ Kecepatan",
            1, 10, self.speed,
            self.update_speed,
            "speed"
        )

        # Buttons
        button_container = tk.Frame(control_inner, bg="#2d3748")
        button_container.pack(fill=tk.X, pady=(20, 0))

        # Play/Pause button
        self.play_btn = ModernButton(
            button_container,
            text="▶ Mulai",
            command=self.toggle_simulation,
            bg_color="#667eea",
            hover_color="#5568d3",
            width=300,
            height=50
        )
        self.play_btn.pack(pady=(0, 10))

        # Button row
        btn_row = tk.Frame(button_container, bg="#2d3748")
        btn_row.pack(fill=tk.X, pady=(0, 10))

        self.reset_btn = ModernButton(
            btn_row,
            text="🔄 Reset",
            command=self.reset_simulation,
            bg_color="#f093fb",
            hover_color="#d97ddf",
            width=145,
            height=45
        )
        self.reset_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.trail_btn = ModernButton(
            btn_row,
            text="✓ Jejak",
            command=self.toggle_trails,
            bg_color="#4ecdc4",
            hover_color="#3db8ad",
            width=145,
            height=45
        )
        self.trail_btn.pack(side=tk.RIGHT)

    def create_stat_card(self, parent, title, value, var_name, color):
        card = tk.Frame(parent, bg="#2d3748")
        card.pack(fill=tk.X, pady=(0, 10))

        # Value
        value_label = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 24, "bold"),
            fg=color,
            bg="#2d3748"
        )
        value_label.pack(pady=(15, 0))
        setattr(self, f"{var_name}_label", value_label)

        # Title
        title_label = tk.Label(
            card,
            text=title,
            font=("Segoe UI", 10),
            fg="#9ca3af",
            bg="#2d3748"
        )
        title_label.pack(pady=(0, 15))

    def create_slider_control(self, parent, label, from_, to, initial, command, prefix):
        container = tk.Frame(parent, bg="#2d3748")
        container.pack(fill=tk.X, pady=(0, 20))

        # Label row
        label_row = tk.Frame(container, bg="#2d3748")
        label_row.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            label_row,
            text=label,
            font=("Segoe UI", 11, "bold"),
            fg="#ffffff",
            bg="#2d3748"
        ).pack(side=tk.LEFT)

        value_label = tk.Label(
            label_row,
            text=str(initial) if prefix == "particle" else f"{initial}x",
            font=("Segoe UI", 11, "bold"),
            fg="#667eea",
            bg="#2d3748"
        )
        value_label.pack(side=tk.RIGHT)
        setattr(self, f"{prefix}_value_label", value_label)

        # Custom styled slider
        slider = tk.Scale(
            container,
            from_=from_,
            to=to,
            orient=tk.HORIZONTAL,
            bg="#2d3748",
            fg="#ffffff",
            troughcolor="#1a1a2e",
            highlightthickness=0,
            sliderrelief=tk.FLAT,
            command=command,
            showvalue=0,
            length=260
        )
        slider.set(initial)
        slider.pack(fill=tk.X)
        setattr(self, f"{prefix}_slider", slider)

    def update_particle_count(self, value):
        self.num_particles = int(float(value))
        self.particle_value_label.config(text=str(self.num_particles))
        if not self.is_running:
            self.init_particles()

    def update_speed(self, value):
        self.speed = int(float(value))
        self.speed_value_label.config(text=f"{self.speed}x")

    def toggle_simulation(self):
        self.is_running = not self.is_running

        if self.is_running:
            self.play_btn.text = "⏸ Jeda"
            self.play_btn.draw_button()
            self.start_time = time.time()
            self.animate()
        else:
            self.play_btn.text = "▶ Mulai"
            self.play_btn.draw_button()

    def reset_simulation(self):
        self.is_running = False
        self.play_btn.text = "▶ Mulai"
        self.play_btn.draw_button()
        self.total_steps = 0
        self.start_time = None

        self.canvas.delete("all")
        self.init_particles()

        self.steps_label.config(text="0")
        self.runtime_label.config(text="0s")

    def toggle_trails(self):
        self.show_trails = not self.show_trails

        if self.show_trails:
            self.trail_btn.text = "✓ Jejak"
        else:
            self.trail_btn.text = "✗ Jejak"
        self.trail_btn.draw_button()

        if not self.show_trails:
            for particle in self.particles:
                particle.trail = []

    def init_particles(self):
        self.canvas.update()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width < 2 or height < 2:
            self.root.after(100, self.init_particles)
            return

        self.particles = []
        for _ in range(self.num_particles):
            self.particles.append(Particle(width, height))

        self.particles_label.config(text=str(len(self.particles)))

    def animate(self):
        if not self.is_running:
            return

        # Clear canvas with fade effect
        self.canvas.delete("all")

        # Draw grid (subtle)
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        grid_size = 50
        for i in range(0, width, grid_size):
            self.canvas.create_line(i, 0, i, height, fill="#1a1a2e", width=1)
        for i in range(0, height, grid_size):
            self.canvas.create_line(0, i, width, i, fill="#1a1a2e", width=1)

        # Update and draw particles
        for particle in self.particles:
            particle.update(self.speed)

            # Draw trail with gradient effect
            if self.show_trails and len(particle.trail) > 1:
                for i in range(len(particle.trail) - 1):
                    x1, y1 = particle.trail[i]
                    x2, y2 = particle.trail[i + 1]
                    alpha_factor = i / len(particle.trail)

                    self.canvas.create_line(
                        x1, y1, x2, y2,
                        fill=particle.color,
                        width=2,
                        stipple="gray50" if alpha_factor < 0.5 else ""
                    )

            # Draw particle with glow effect
            glow_radius = particle.radius + 4
            self.canvas.create_oval(
                particle.x - glow_radius,
                particle.y - glow_radius,
                particle.x + glow_radius,
                particle.y + glow_radius,
                fill=particle.color,
                outline="",
                stipple="gray25"
            )

            # Main particle
            self.canvas.create_oval(
                particle.x - particle.radius,
                particle.y - particle.radius,
                particle.x + particle.radius,
                particle.y + particle.radius,
                fill=particle.color,
                outline="white",
                width=1
            )

        # Update statistics
        self.total_steps += 1
        self.steps_label.config(text=str(self.total_steps))

        if self.start_time:
            runtime = int(time.time() - self.start_time)
            minutes = runtime // 60
            seconds = runtime % 60
            if minutes > 0:
                self.runtime_label.config(text=f"{minutes}m {seconds}s")
            else:
                self.runtime_label.config(text=f"{seconds}s")

        # Continue animation (60 FPS)
        self.root.after(16, self.animate)

def main():
    root = tk.Tk()

    # Try to set app icon (optional)
    try:
        root.iconbitmap('icon.ico')
    except:
        pass

    app = BrownianMotionSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
