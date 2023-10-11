# 1. Integrating tkinter into our program
from tkinter import *
from tkinter import ttk
def calculate(*args):
    try:
        value = float(feet.get())
        meters.set(int(0.3048 * value * 10000.0 + 0.5)/ 10000.0)
    except ValueError:
        pass

# 2. Setting up the Main Application Window
root = Tk()
root.title("json_validator")
main_frame = ttk.Frame(root, padding="3 3 12 12")

# 3. Creating a Content Frame
main_frame.grid(column=0, row=0, sticky=(N, W, E, S)) 
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# 4. Creating the entry widget
feet = StringVar() # Create the widget itself 
feet_entry = ttk.Entry(main_frame, width=7, textvariable=feet) # Create the widget itself
feet_entry.grid(column=2, row=1, sticky=(W,E)) # and then place it onscreen

# 5. Creating the remaining widgets
meters = StringVar()
ttk.Label(main_frame, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
ttk.Button(main_frame, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)
ttk.Label(main_frame, text="feet").grid(column=3, row=1, sticky=W)
ttk.Label(main_frame, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(main_frame, text="meters").grid(column=3, row=2, sticky=W)

# 6. Adding some polish
for child in main_frame.winfo_children():
    child.grid_configure(padx=5, pady=5)
feet_entry.focus() # focus on the entry of the program so that the user don't have to click the entry 
root.bind("<Return>", calculate) # binds Enter keyboard to calculate button.

root.mainloop()