import sys
import os
from tkinter import *
from tkinter import ttk  # Import ttk for themed buttons
import recorder
import time
from PIL import Image, ImageTk

def start():
    global running, start_time, paused

    if running is not None and not paused:
        print('Recording already in progress')
    else:
        if paused:
            # Adjust start_time to account for the time paused
            start_time += time.time() - pause_start_time
            running.resume_recording()
        else:
            start_time = time.time()  # Record the start time
            running = rec.open('AudioFile/audio.wav', 'wb')
            running.start_recording()
        paused = False
        update_timer()  # Start updating the timer

def stop():
    global running, start_time

    if running is not None:
        running.stop_recording()
        running.close()
        running = None
        window.after_cancel(timer_id)  # Stop updating the timer
        elapsed_time = time.time() - start_time
        print(f'Recording stopped. Elapsed time: {elapsed_time:.2f} seconds')
    else:
        print('No recording in progress')

def pause():
    global running, paused, pause_start_time

    if running is not None and not paused:
        running.pause_recording()
        paused = True
        pause_start_time = time.time()  # Record the time when paused
        print('Recording paused')
    elif running is not None and paused:
        print('Recording already paused')
    else:
        print('No recording in progress')

def update_timer():
    global timer_id, paused

    if running is not None and not paused:
        elapsed_time = time.time() - start_time
        timer_label.config(text=f'Time: {elapsed_time:.2f} seconds')
    timer_id = window.after(100, update_timer)  # Update the timer every 100 milliseconds

def run():
    os.system('python "Source Code/summarization.py"')

rec = recorder.Recorder(channels=1)
running = None
start_time = 0
pause_start_time = 0  # Record the time when paused
timer_id = None
paused = False

window = Tk()
window.title("Meetings Summary")

# Set the background color of the window to black
window.configure(bg='black')

# Center the window on the screen
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = 400
window_height = 425
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

window.geometry(f'{window_width}x{window_height}+{x_position}+{y_position}')

# Styling
font_style = ("Helvetica", 12)

background_image = Image.open('images/bg.jpg')
background_image = background_image.resize((window_width, window_height), Image.LANCZOS)
background_image = ImageTk.PhotoImage(background_image, master=window)

label = Label(window, image=background_image, bg='black')
label.place(x=0, y=0)

# Create themed buttons with a sleek black border
style = ttk.Style()
style.configure('TButton', background='#363636', foreground='black', borderwidth=0, borderradius=10, relief='flat')
style.map('TButton', background=[('active', '#282828')])

button_rec = ttk.Button(window, text='Start Recording', command=start, style='TButton')
button_rec.pack(pady=10)
button_rec.place(x=140,y = 100)
style.configure('TButton', font=font_style)  # Set font for the button
button_pause = ttk.Button(window, text='Pause Recording', command=pause, style='TButton')
button_pause.pack(pady=10)
button_pause.place(x=140,y = 150)
button_stop = ttk.Button(window, text='Stop Recording', command=stop, style='TButton')
button_stop.pack(pady=10)
button_stop.place(x=140,y = 200)
btn = ttk.Button(window, text="Summarize", command=run, style='TButton')
btn.pack(pady=10)
btn.place(x=140,y = 250)
# Configure label style with no background and increased thickness
timer_label = Label(window, text='Time: 0.00 seconds', font=font_style, bd=0, relief='flat', bg='black', fg='white')
timer_label.pack(pady=10)
timer_label.place(x=140,y=300)
timer_label.configure(font=('Helvetica', 12, 'bold'))  # Increase font thickness

window.mainloop()