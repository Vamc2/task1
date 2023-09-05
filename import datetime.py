import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import threading
import time

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Alarm Clock")
        self.root.geometry("300x150")
        
        self.alarm_time = None
        
        self.label = tk.Label(root, text="Set Alarm (HH:MM):")
        self.label.pack(pady=10)
        
        self.entry = tk.Entry(root)
        self.entry.pack(pady=5)
        
        self.set_button = tk.Button(root, text="Set Alarm", command=self.set_alarm)
        self.set_button.pack(pady=5)
        
        self.cancel_button = tk.Button(root, text="Cancel Alarm", command=self.cancel_alarm)
        self.cancel_button.pack(pady=5)
        
    def set_alarm(self):
        alarm_time_str = self.entry.get()
        
        try:
            self.alarm_time = datetime.strptime(alarm_time_str, "%H:%M")
            current_time = datetime.now().time()
            
            if self.alarm_time.time() < current_time:
                # If the alarm time is in the past, set it for the next day
                self.alarm_time = self.alarm_time.replace(day=self.alarm_time.day + 1)
            
            self.show_message("Alarm set for {}".format(self.alarm_time.strftime("%H:%M")))
            
            # Start a new thread to monitor and trigger the alarm
            self.alarm_thread = threading.Thread(target=self.monitor_alarm)
            self.alarm_thread.daemon = True
            self.alarm_thread.start()
        
        except ValueError:
            self.show_message("Invalid time format. Please use HH:MM in 24-hour format.")
    
    def cancel_alarm(self):
        self.alarm_time = None
        self.show_message("Alarm canceled.")
    
    def monitor_alarm(self):
        while self.alarm_time:
            current_time = datetime.now().time()
            
            if current_time >= self.alarm_time.time():
                self.show_message("Time to wake up!")
                break
            
            time.sleep(1)
    
    def show_message(self, message):
        messagebox.showinfo("Alarm", message)

if __name__ == "__main__":
    root = tk.Tk()
    alarm_clock = AlarmClock(root)
    root.mainloop()
