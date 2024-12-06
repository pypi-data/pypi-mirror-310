from datetime import datetime

def booking_success():
    """Returns the current datetime and booking success message."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Booking successfully done on {current_time}"
