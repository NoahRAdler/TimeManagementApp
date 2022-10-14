from tkinter import *
import glob

# From current level, find all .txt files in the designated folder for app
files = glob.glob('./TodoAndReminders/*.txt')

# Displays files to chose from with the associated input for choosing
def showTodoFiles():

    fileDisplayTextArea.config(state = NORMAL) # Change state of Text area to allow write

    for i in range(len(files)):

        fileDisplayTextArea.insert(END, str(i + 1) + ": " + files[i] + "\n")
        
    fileDisplayTextArea.config(state = DISABLED) # Make read-only again

# Displays contents of file selected
def showFileContents():
    input = fileSelecter.get()

    fileContentsTextArea.config(state = NORMAL) # Change state of Text area to allow write

    if input.isdigit():
        if int(input) not in range(1, len(files) + 1):
            fileContentsTextArea.insert(END, "Bad Input: Invalid range \n")
            return FALSE
    else:
        fileContentsTextArea.insert(END, "Bad Input: Not a digit \n")
        return FALSE

    fileContentsTextArea.delete(1.0, END)
    index = int(input) - 1

    fOpened = open(files[index], "r")

    for line in fOpened:
        fileContentsTextArea.insert(END, line + "\n")

    fOpened.close()
    fileContentsTextArea.config(state = DISABLED) # Make read-only again

        
 

# Main window
window = Tk()

# window size
window.geometry('500x500')

# background color
window.config(background = "white")

# titling main window
window.title("Time Manager")

selectFrame = Frame(window)

# Button: initiate command to find files
showFilesButton = Button(window,
                         text = "Show Files",
                         command = showTodoFiles)

# TextArea: display files here
fileDisplayTextArea = Text(window,
                         width = 50, height = 10,
                         state = DISABLED,
                         fg = "black",
                         bg = "lightBlue")

# Button: Confirm file Selected
confirmSelection = Button(selectFrame,
                         text = "Select File: ",
                         command = showFileContents)

# SpinBox: Select file
fileSelecter = Spinbox(selectFrame,
                       from_=1, to = len(files) )

# TextArea: display file contents here
fileContentsTextArea = Text(window,
                         width = 50, height = 10,
                         state = DISABLED,
                         fg = "black",
                         bg = "lightBlue")

# Assign all widgets to window grid
showFilesButton.grid(column = 1, row = 1)

fileDisplayTextArea.grid(column = 1, row = 2)

selectFrame.grid(column = 1, row = 3) # Holds both widgets below that use .pack

confirmSelection.pack( side = LEFT) # stacks/packs starting left, allows them to be side by side 

fileSelecter.pack( side = LEFT)

fileContentsTextArea.grid(column = 1, row = 4)





window.mainloop()