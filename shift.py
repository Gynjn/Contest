import time

def avoidance(bool_value, ser):
    start_time = time.time()  # Get the current time in seconds
    end_time = start_time + 6.3  # Set the end time as 5 seconds from the start
    if(bool_value == 1):
        while time.time() < end_time:
            message = 'a' + str(-6) + 's' + str(50)
            ser.write(message.encode())
            time.sleep(0.025)
        return 1
    else:
        while time.time() < end_time+0.7:
            message = 'a' + str(6) + 's' + str(50)
            ser.write(message.encode())
            time.sleep(0.025)
        return 2
