import signal
from functools import wraps
import platform
import os
import pandas as pd

class TimeoutError(Exception):
    """Custom exception to be raised when a timeout occurs."""
    pass

def timeout(seconds=10, error_message="Function call timed out"):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        @wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)  # Cancel the alarm
            return result
        return wrapper
    return decorator

def play_sound_or_say(message=None):
    if platform.system() == 'Darwin':  # Darwin is the system name for macOS
        if message:
            os.system(f'say "{message}"')
        else:
            os.system('say "Ding"')
    else:
        # For Windows and Linux, we'll just print a beep sound
        # Windows has a built-in beep sound in the command prompt, and Linux terminals generally support the BEL character for a beep.
        print('\a')  # This is the BEL character, which causes the terminal to beep

def dates_to_scrape():
    now = pd.Timestamp.now()
    dates = pd.date_range(start="2020-01-01", end=now, freq="D")
    return dates