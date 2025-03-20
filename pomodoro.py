import tkinter as tk
from tkinter import ttk
import time

class PomodoroApp:
    """
    Pomodoro Timer Application (Tkinter GUI)
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.configure(bg="#f0f4fd")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 400
        window_height = 500
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
        
        # Timer Settings
        self.work_time = 25 * 60
        self.break_time = 5 * 60
        self.remaining_time = self.work_time
        self.is_running = False
        self.is_work_session = True
        
        # Session Count
        self.session_count = 0
        self.counter_label = tk.Label(root, text="Sessions Completed: 0", font=("Helvetica", 12), bg="#f0f4fd", fg="#777")
        self.counter_label.pack(pady=5)

        # UI Elements
        self.session_label = tk.Label(root, text="Work Session", font=("Helvetica", 20, "bold"), bg="#f0f4fd", fg="#555")
        self.session_label.pack(pady=20)

        self.timer_label = tk.Label(root, text="25:00", font=("Helvetica", 50, "bold"), bg="#f0f4fd", fg="#333")
        self.timer_label.pack(pady=20)
        
        button_frame = tk.Frame(root, bg="#f0f4fd")
        button_frame.pack(pady=30)

        style = ttk.Style()
        style.configure("TButton", padding=10, relief="flat", background="#8f99fb", font=("Helvetica", 12))

        self.start_button = ttk.Button(button_frame, text="Start", command=self.start_timer)
        self.start_button.grid(row=0, column=0, padx=10)

        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_timer)
        self.stop_button.grid(row=0, column=1, padx=10)

        self.reset_button = ttk.Button(button_frame, text="Reset", command=self.reset_timer)
        self.reset_button.grid(row=0, column=2, padx=10)

        
    def update_timer(self):
        """Updates the countdown timer in the GUI."""
        if self.remaining_time > 0 and self.is_running:
            mins, secs = divmod(self.remaining_time, 60)
            self.timer_label.config(text=f"{mins:02}:{secs:02}")
            self.remaining_time -= 1
            self.root.after(1000, self.update_timer)
            
        elif self.remaining_time == 0:
            if self.is_work_session:
                self.remaining_time = self.break_time
                self.is_work_session = False
                self.session_label.config(text="Break Session", fg="#1E90FF")
            else:
                self.remaining_time = self.work_time
                self.is_work_session = True
                self.session_label.config(text="Work Session", fg="#555")

            self.update_timer()
        
    def start_timer(self):
        """Starts the countdown timer."""
        if not self.is_running:
            self.is_running = True
            self.update_timer()
            
    def stop_timer(self):
        """Stops the countdown timer."""
        self.is_running = False
        
    def reset_timer(self):
        """Resets the timer to the initial work session time."""
        self.is_running = False 
        self.remaining_time = self.work_time
        self.is_work_session = True
        self.timer_label.config(text="25:00", fg="#333")

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()