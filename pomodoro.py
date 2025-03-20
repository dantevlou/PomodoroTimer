import tkinter as tk
from tkinter import ttk
from playsound import playsound

class PomodoroApp:
    """A GUI Pomodoro Timer application with customizable work/break durations and auto-start feature."""
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.configure(bg="#f0f4fd")
        self.setup_window()
        self.initialize_variables()
        self.create_styles()
        self.create_widgets()

    def setup_window(self):
        """Center window on screen."""
        width, height = 500, 550
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        pos_x = (screen_w // 2) - (width // 2)
        pos_y = (screen_h // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

    def initialize_variables(self):
        """Initialize timer, session, and control states."""
        self.work_time = 25 * 60  # Default work duration (seconds)
        self.break_time = 5 * 60  # Default break duration (seconds)
        self.remaining_time = self.work_time
        self.is_running = False
        self.is_work_session = True
        self.session_count = 0
        self.auto_start = tk.BooleanVar()  # Auto-start toggle

    def create_styles(self):
        """Define button and progress bar styles."""
        style = ttk.Style()
        style.theme_use('clam')

        # Main buttons style
        style.configure("App.TButton",
                        foreground="#fff", background="#4e73df",
                        borderwidth=0, padding=10,
                        font=("Helvetica", 12))
        style.map("App.TButton",
                  background=[('active', '#2e59d9'), ('pressed', '#1c3faa')],
                  foreground=[('pressed', '#fff'), ('active', '#fff')])

        # Highlight Set Duration button when entry modified
        style.configure("Highlight.TButton",
                        foreground="#1e1e2f", background="#f6ad55",
                        borderwidth=0, padding=10,
                        font=("Helvetica", 12))
        style.map("Highlight.TButton",
                  background=[('active', '#ed8936'), ('pressed', '#dd6b20')],
                  foreground=[('pressed', '#1e1e2f'), ('active', '#1e1e2f')])

        # Resume button style
        style.configure("Resume.TButton",
                        foreground="#1e1e2f", background="#f6ad55",
                        borderwidth=0, padding=12,
                        font=("Century Gothic", 14))
        style.map("Resume.TButton",
                  background=[('active', '#ed8936'), ('pressed', '#dd6b20')],
                  foreground=[('pressed', '#1e1e2f'), ('active', '#1e1e2f')])

        # Progress bar style
        style.configure("App.Horizontal.TProgressbar",
                        troughcolor='#d6d6d6',
                        background='#4e73df',
                        thickness=20,
                        borderwidth=0)

    def create_widgets(self):
        """Create and organize UI elements."""
        self.create_input_frame()
        self.create_session_info()
        self.create_timer_display()
        self.create_session_switch_controls()
        self.create_controls()

    def create_input_frame(self):
        """Input fields for custom work and break durations."""
        frame = tk.Frame(self.root, bg="#fff")
        frame.pack(pady=10)

        # Work Duration Input
        tk.Label(frame, text="Work (min):", font=("Helvetica", 12), bg="#f0f4fd", fg="#777").grid(row=0, column=0, padx=5)
        self.work_entry = tk.Entry(frame, width=5)
        self.work_entry.insert(0, "25")
        self.work_entry.grid(row=0, column=1, padx=5)

        # Break Duration Input
        tk.Label(frame, text="Break (min):", font=("Helvetica", 12), bg="#f0f4fd", fg="#777").grid(row=0, column=2, padx=5)
        self.break_entry = tk.Entry(frame, width=5)
        self.break_entry.insert(0, "5")
        self.break_entry.grid(row=0, column=3, padx=5)

        # Set and Reset Buttons
        self.set_button = ttk.Button(frame, text="Set Duration", command=self.set_durations, style="App.TButton")
        self.set_button.grid(row=1, column=0, columnspan=4, pady=10)

        ttk.Button(frame, text="Reset Duration", command=self.reset_durations, style="App.TButton").grid(row=2, column=0, columnspan=4, pady=5)

        # Highlight effect when modifying input
        self.work_entry.bind("<KeyRelease>", self.highlight_set_button)
        self.break_entry.bind("<KeyRelease>", self.highlight_set_button)

    def create_session_info(self):
        """Session count and session type display."""
        self.counter_label = tk.Label(self.root, text="Sessions Completed: 0", font=("Helvetica", 12),
                                     bg="#f0f4fd", fg="#777")
        self.counter_label.pack(pady=5)

        self.session_label = tk.Label(self.root, text="Work Session", font=("Helvetica", 20, "bold"),
                                     bg="#f0f4fd", fg="#555")
        self.session_label.pack(pady=10)

    def create_timer_display(self):
        """Main timer display and progress bar."""
        self.timer_label = tk.Label(self.root, text="25:00", font=("Helvetica", 50, "bold"),
                                bg="#f0f4fd", fg="#333")
        self.timer_label.pack(pady=10)

        self.progress = ttk.Progressbar(self.root, length=300, mode='determinate', style="App.Horizontal.TProgressbar")
        self.progress.pack(pady=10)

        # Pause Indicator Label
        self.pause_label = tk.Label(self.root, text="", font=("Helvetica", 14), bg="#f0f4fd", fg="#ff6347")
        self.pause_label.pack(pady=5)

    def create_controls(self):
        """Start, Pause, Reset control buttons + Session Switch buttons."""
        frame = tk.Frame(self.root, bg="#f0f4fd")
        frame.pack(pady=20)

        self.start_button = ttk.Button(frame, text="Start", command=self.start_timer, style="App.TButton")
        self.start_button.grid(row=0, column=0, padx=10)

        ttk.Button(frame, text="Pause", command=self.pause_timer, style="App.TButton").grid(row=0, column=1, padx=10)

        ttk.Button(frame, text="Reset", command=self.reset_timer, style="App.TButton").grid(row=0, column=2, padx=10)
        
    def switch_to_work(self):
        """Manually switch to Work session."""
        self.is_running = False
        self.is_work_session = True
        mins = int(self.work_entry.get())
        self.remaining_time = mins * 60
        self.progress['value'] = 0
        self.session_label.config(text="Work Session", fg="#555")
        self.timer_label.config(text=f"{mins:02}:00", fg="#333")
        self.start_button.config(text="Start", style="App.TButton")
        self.start_button.state(['!disabled'])
        self.pause_label.config(text="Switched to Work")

    def switch_to_break(self):
        """Manually switch to Break session."""
        self.is_running = False
        self.is_work_session = False
        mins = int(self.break_entry.get())
        self.remaining_time = mins * 60
        self.progress['value'] = 0
        self.session_label.config(text="Break Session", fg="#1E90FF")
        self.timer_label.config(text=f"{mins:02}:00", fg="#333")
        self.start_button.config(text="Start", style="App.TButton")
        self.start_button.state(['!disabled'])
        self.pause_label.config(text="Switched to Break")
        
    def create_session_switch_controls(self):
        """Switch buttons & Auto-Start checkbox aligned horizontally."""
        frame = tk.Frame(self.root, bg="#f0f4fd")
        frame.pack(pady=10)

        # Switch to Work Button
        ttk.Button(frame, text="Switch to Work", command=self.switch_to_work, style="App.TButton").grid(row=0, column=0, padx=10)

        # Auto-Start Checkbox
        auto_start_check = tk.Checkbutton(frame, text="Auto-Start Next Session", variable=self.auto_start, bg="#f0f4fd")
        auto_start_check.grid(row=0, column=1, padx=10)

        # Switch to Break Button
        ttk.Button(frame, text="Switch to Break", command=self.switch_to_break, style="App.TButton").grid(row=0, column=2, padx=10)


    def highlight_set_button(self, event):
        """Visually highlight Set button when user edits input."""
        self.set_button.configure(style="Highlight.TButton")

    def set_durations(self):
        """Set custom durations based on user input."""
        try:
            work_min = int(self.work_entry.get())
            break_min = int(self.break_entry.get())
            if work_min <= 0 or break_min <= 0:
                raise ValueError
            self.work_time = work_min * 60
            self.break_time = break_min * 60
            self.remaining_time = self.work_time
            self.is_work_session = True
            self.timer_label.config(text=f"{work_min:02}:00", fg="#333")
            self.set_button.configure(style="App.TButton")  # Reset highlight style after setting
        except ValueError:
            # Handle invalid input
            self.timer_label.config(text="Invalid Input", fg="red")

    def reset_durations(self):
        """Reset durations back to default (25/5 minutes)."""
        self.work_entry.delete(0, tk.END)
        self.work_entry.insert(0, "25")
        self.break_entry.delete(0, tk.END)
        self.break_entry.insert(0, "5")

        self.work_time = 25 * 60
        self.break_time = 5 * 60
        self.remaining_time = self.work_time
        self.is_work_session = True
        self.timer_label.config(text="25:00", fg="#333")

    def start_timer(self):
        """Start the timer if not already running."""
        if not self.is_running:
            self.is_running = True
            self.start_button.state(['disabled'])
            self.start_button.config(text="Start", style="App.TButton")
            self.pause_label.config(text="")  # Remove paused indicator
            self.update_timer()

    def pause_timer(self):
        """Pause the countdown."""
        self.is_running = False
        self.start_button.config(text="Resume", style="Resume.TButton")
        self.start_button.state(['!disabled'])
        self.pause_label.config(text="Paused")

    def reset_timer(self):
        """Reset timer to current session's input duration (Work or Break)."""
        self.is_running = False

        if self.is_work_session:
            # Reset to Work session duration
            mins = int(self.work_entry.get())
            self.remaining_time = mins * 60
            self.session_label.config(text="Work Session", fg="#555")
        else:
            # Reset to Break session duration
            mins = int(self.break_entry.get())
            self.remaining_time = mins * 60
            self.session_label.config(text="Break Session", fg="#1E90FF")

        # Reset progress bar & labels
        self.progress['value'] = 0
        self.timer_label.config(text=f"{mins:02}:00", fg="#333")
        self.start_button.config(text="Start", style="App.TButton")
        self.start_button.state(['!disabled'])
        self.pause_label.config(text="")

    def update_timer(self):
        """Main countdown loop."""
        if self.remaining_time > 0 and self.is_running:
            mins, secs = divmod(self.remaining_time, 60)
            self.timer_label.config(text=f"{mins:02}:{secs:02}")
            total_time = self.work_time if self.is_work_session else self.break_time
            self.progress['value'] = ((total_time - self.remaining_time) / total_time) * 100
            self.remaining_time -= 1
            self.root.after(1000, self.update_timer)
        elif self.remaining_time == 0:
            # Timer finished: play sound & switch session
            playsound('sounds/alarm.mp3')
            self.switch_session()

    def switch_session(self):
        """Switch between work and break sessions."""
        if self.is_work_session:
            self.remaining_time = self.break_time
            self.is_work_session = False
            self.session_label.config(text="Break Session", fg="#1E90FF")
        else:
            self.remaining_time = self.work_time
            self.is_work_session = True
            self.session_count += 1
            self.counter_label.config(text=f"Sessions Completed: {self.session_count}")
            self.session_label.config(text="Work Session", fg="#555")

        # Prevent getting stuck if durations are too short
        if self.remaining_time <= 0:
            self.timer_label.config(text="Session Too Short!", fg="red")
            self.is_running = False
            self.start_button.state(['!disabled'])
            self.start_button.config(text="Start", style="App.TButton")
            return

        # Auto-start next session
        if self.auto_start.get():
            self.is_running = True
            self.update_timer()
        else:
            self.is_running = False
            self.start_button.state(['!disabled'])
            self.start_button.config(text="Resume", style="Resume.TButton")

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
