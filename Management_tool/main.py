from tkinter import *

window_width = 600
window_height = 400

if __name__ == '__main__':
    main_frame = Tk()
    main_frame.title("Management_tool")
    main_frame.geometry(f'{window_width}x{window_height}')
    main_frame.resizable(False, False) # this make the window to don't be resizeable
    main_frame.iconbitmap(".\my_icon.ico");

    main_frame.mainloop()# display components and run the program
