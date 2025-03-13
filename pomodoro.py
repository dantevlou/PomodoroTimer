import time

def pomodoro_cycle(work_time, break_time, cycles):
    """
    Runs a full Pomodoro cycle with work and break intervals.
    """
    for cycle in range(cycles):
        print(f"Work session {cycle + 1} started!")
        countdown(work_time)
        
        if cycle < cycle - 1:
            print("Take a short break!")
            countdown(break_time)
            
    print("Pomodoro session complete!")

def countdown(minutes):
    """
    Displays a countdown timer in MM:SS format.
    """
    seconds = minutes * 60 
    while seconds:
        mins, secs = divmod(seconds, 60)
        print(f"{mins:02}:{secs:02}", end="\r")
        time.sleep(1) 
        seconds -= 1 
    print("\nTime's up!")
    
if __name__ == "__main__":
    work_time = int(input("Enter work session duration (minutes): "))
    break_time = int(input("Enter break duration (minutes): "))
    cycles = int(input("Enter number of cycles: "))
    
    pomodoro_cycle(work_time, break_time, cycles)