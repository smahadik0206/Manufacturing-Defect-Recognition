import tkinter as tk

def button_click():
    global function_running
    if not function_running:
        function_running = True
        
        # Perform your function here
        
        function_running = False

function_running = False

root = tk.Tk()
button = tk.Button(root, text="Click Me", command=button_click)
button.pack()

root.mainloop()
