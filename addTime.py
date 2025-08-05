def add_time(start, duration, day=None):
    parts = start.split()
    period = parts[1].upper()
    time_str = parts[0]
    
    time_parts = time_str.split(':')
    start_hour = int(time_parts[0])
    start_minute = int(time_parts[1])
    
    if period == 'PM' and start_hour != 12:
        start_hour += 12
    if period == 'AM' and start_hour == 12:
        start_hour = 0
        
    dur_parts = duration.split(':')
    dur_hour = int(dur_parts[0])
    dur_minute = int(dur_parts[1])
    
    total_minutes = start_minute + dur_minute
    carry_hour = total_minutes // 60
    remaining_minutes = total_minutes % 60
    
    total_hours = start_hour + dur_hour + carry_hour
    days = total_hours // 24
    remaining_hours = total_hours % 24
    
    if remaining_hours == 0:
        hour_12 = 12
        new_period = 'AM'
    elif remaining_hours == 12:
        hour_12 = 12
        new_period = 'PM'
    elif remaining_hours < 12:
        hour_12 = remaining_hours
        new_period = 'AM'
    else:
        hour_12 = remaining_hours - 12
        new_period = 'PM'
    
    formatted_minutes = str(remaining_minutes).zfill(2)
    
    new_day_str = ""
    if day:
        day = day.lower()
        days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        try:
            index = days_of_week.index(day)
            new_index = (index + days) % 7
            new_day = days_of_week[new_index]
            new_day_str = ", " + new_day.capitalize()
        except ValueError:
            pass
    
    result = f"{hour_12}:{formatted_minutes} {new_period}{new_day_str}"
    
    if days == 1:
        result += " (next day)"
    elif days > 1:
        result += f" ({days} days later)"
    
    return result