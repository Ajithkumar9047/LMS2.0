# whatsapp.py
import pywhatkit as kit
import time
from datetime import datetime

current_date = datetime.now().strftime('%d/%m/%Y')

def whatsapp_notification(num_rows_query1, num_rows_query2, num_rows_query3):
    group_name_or_id = "LLFST2ru6IKExGJoZjjopZ"
    message = f"tvs lms-Threshold FEED: {num_rows_query2} Threshold master: {num_rows_query1} Total null: {num_rows_query3} we updated the max count for those null values"

    # Adjust the delay time based on your needs
    delay_seconds = 120  # Delay for 120 seconds (2 minutes)
    time.sleep(delay_seconds)
    now = datetime.now()
    hour = now.hour
    minute = now.minute + 1
    kit.sendwhatmsg_to_group(group_name_or_id, message, hour, minute)
    print('Message sent successfully')
    print(message)
