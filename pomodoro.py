import tkinter as tk
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
        
        # Timer settings
        self.work_time = 25 * 60
        self.break_time = 5 * 60
        self.remaining_time = self.work_time
        self.is_running = False
        self.is_work_session = True

        # UI Elements
        self.session_label = tk.Label(root, text="Work Session", font=("Helvetica", 20, "bold"), bg="#f0f4fd", fg="#555")
        self.session_label.pack(pady=20)

        self.timer_label = tk.Label(root, text="25:00", font=("Helvetica", 50, "bold"), bg="#f0f4fd", fg="#333")
        self.timer_label.pack(pady=20)
        
        self.start_button = tk.Button(root, text="Start", font=("Helvetica", 14), command=self.start_timer)
        self.start_button.pack(pady=5)
        
        self.stop_button = tk.Button(root, text="Stop", font=("Helvetica", 14), command=self.stop_timer)
        self.stop_button.pack(pady=5)
        
        self.reset_button = tk.Button(root, text="Reset", font=("Helvetica", 14), command=self.reset_timer)
        self.reset_button.pack(pady=5)
        
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

            self.root.after(1000, self.update_timer)
        
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