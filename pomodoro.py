import tkinter as tk

root = tk.Tk()
root.title("Pomodoro Timer")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = int(screen_width * 0.2)
window_height = int(screen_height * 0.4)

position_x = 0
position_y = 0

root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

timer_label = tk.Label(root, text="25:00", font=("Helvetica", 40))
timer_label.pack(pady=20)

root.mainloop()