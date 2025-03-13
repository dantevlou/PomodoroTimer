import time

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
    countdown(25)