import tkinter as tk
from tkinter import ttk
from playsound import playsound

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.configure(bg="#f0f4fd")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 500
        window_height = 550
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
        
        input_frame = tk.Frame(root, bg="#fff")
        input_frame.pack(pady=10)

        # Work Input
        tk.Label(input_frame, text="Work (min):", font=("Helvetica", 12), bg="#f0f4fd", fg="#777").grid(row=0, column=0, padx=5)
        self.work_entry = tk.Entry(input_frame, width=5)
        self.work_entry.insert(0, "25")
        self.work_entry.grid(row=0, column=1, padx=5)

        # Break Input
        tk.Label(input_frame, text="Break (min):", font=("Helvetica", 12), bg="#f0f4fd", fg="#777").grid(row=0, column=2, padx=5)
        self.break_entry = tk.Entry(input_frame, width=5)
        self.break_entry.insert(0, "5")
        self.break_entry.grid(row=0, column=3, padx=5)

        # Set Duration Button
        self.set_button = ttk.Button(input_frame, text="Set Duration", command=self.set_durations, style="App.TButton")
        self.set_button.grid(row=1, column=0, columnspan=4, pady=10)
        
        # Reset Duration Button
        self.reset_duration_button = ttk.Button(input_frame, text="Reset Duration", command=self.reset_durations, style="App.TButton")
        self.reset_duration_button.grid(row=2, column=0, columnspan=4, pady=5)

        
        # Default Timer Settings
        self.work_time = 25 * 60
        self.break_time = 5 * 60
        self.remaining_time = self.work_time
        self.is_running = False
        self.is_work_session = True
        
        # Session Count
        self.session_count = 0
        self.counter_label = tk.Label(root, text="Sessions Completed: 0", font=("Helvetica", 12), bg="#f0f4fd", fg="#777")
        self.counter_label.pack(pady=5)

        # Session Label
        self.session_label = tk.Label(root, text="Work Session", font=("Helvetica", 20, "bold"), bg="#f0f4fd", fg="#555")
        self.session_label.pack(pady=10)

        # Timer Label
        self.timer_label = tk.Label(root, text="25:00", font=("Helvetica", 50, "bold"), bg="#f0f4fd", fg="#333")
        self.timer_label.pack(pady=10)
        
        # Progress Bar
        self.progress = ttk.Progressbar(root, length=300, mode='determinate', style="App.Horizontal.TProgressbar")
        self.progress.pack(pady=10)
        
        # Auto-Start Next Session
        self.auto_start = tk.BooleanVar()
        self.auto_start_check = tk.Checkbutton(root, text="Auto-Start Next Session", variable=self.auto_start, bg="#f0f4fd")
        self.auto_start_check.pack(pady=5)
        
        # Pause Indicator Label
        self.pause_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#f0f4fd", fg="#ff6347")
        self.pause_label.pack(pady=5)

        # Styles
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("App.TButton",
            foreground="#fff",
            background="#4e73df",
            borderwidth=0,
            focusthickness=3,
            focuscolor='none',
            padding=10,
            font=("Helvetica", 12)
        )
        style.configure("App.Horizontal.TProgressbar",
            troughcolor='#d6d6d6',   
            background='#4e73df',       
            thickness=20,
            borderwidth=0
        )

        style.map("App.TButton",
            background=[('active', '#2e59d9'), ('pressed', '#1c3faa')],
            foreground=[('pressed', '#fff'), ('active', '#fff')]
        )
        
        # Buttons
        button_frame = tk.Frame(root, bg="#f0f4fd")
        button_frame.pack(pady=20)

        self.start_button = ttk.Button(button_frame, text="Start", command=self.start_timer, style="App.TButton")
        self.start_button.grid(row=0, column=0, padx=10)

        self.pause_button = ttk.Button(button_frame, text="Pause", command=self.pause_timer, style="App.TButton")
        self.pause_button.grid(row=0, column=1, padx=10)

        self.reset_button = ttk.Button(button_frame, text="Reset", command=self.reset_timer, style="App.TButton")
        self.reset_button.grid(row=0, column=2, padx=10)

    def set_durations(self):
        """Set custom work/break durations based on user input."""
        try:
            work_minutes = int(self.work_entry.get())
            break_minutes = int(self.break_entry.get())
            if work_minutes <= 0 or break_minutes <= 0:
                raise ValueError
            self.work_time = work_minutes * 60
            self.break_time = break_minutes * 60
            self.remaining_time = self.work_time
            self.is_work_session = True
            self.timer_label.config(text=f"{work_minutes:02}:00", fg="#333")
        except ValueError:
            self.timer_label.config(text="Invalid Input", fg="red")
            
    def reset_durations(self):
        self.work_entry.delete(0, tk.END)
        self.work_entry.insert(0, "25")

        self.break_entry.delete(0, tk.END)
        self.break_entry.insert(0, "5")

        self.work_time = 25 * 60
        self.break_time = 5 * 60
        self.remaining_time = self.work_time
        self.is_work_session = True
        self.timer_label.config(text="25:00", fg="#333", bg="#f0f4fd", font=("Helvetica", 50, "bold"))

    def update_timer(self):
        if self.remaining_time > 0 and self.is_running:
            mins, secs = divmod(self.remaining_time, 60)
            self.timer_label.config(text=f"{mins:02}:{secs:02}")
            
            total_time = self.work_time if self.is_work_session else self.break_time
            progress_value = ((total_time - self.remaining_time) / total_time) * 100
            self.progress['value'] = progress_value
            
            self.remaining_time -= 1
            self.root.after(1000, self.update_timer)
            
        elif self.remaining_time == 0:
            # Play Sound
            playsound('sounds/alarm.mp3')
            
            # Switch Session
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
            
            if self.auto_start.get():
                self.is_running = True
                self.update_timer()
            else:
                self.is_running = False
                self.start_button.state(['!disabled'])
                self.start_button.config(text="Resume")

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.update_timer()
            self.start_button.state(['disabled']) 
            self.pause_label.config(text="")

    def pause_timer(self):
        self.is_running = False
        self.start_button.config(text="Resume")
        self.start_button.state(['!disabled'])
        self.pause_label.config(text="Paused")

    def reset_timer(self):
        self.is_running = False
        self.remaining_time = self.work_time
        self.is_work_session = True
        work_minutes = self.work_time // 60
        self.progress['value'] = 0
        self.start_button.config(text="Start")
        self.timer_label.config(text=f"{work_minutes:02}:00", fg="#333")
        self.start_button.state(['!disabled'])
        self.pause_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
