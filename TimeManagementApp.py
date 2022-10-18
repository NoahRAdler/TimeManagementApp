from tkinter import *
from tkinter import messagebox
import glob

# From current level, find all .txt files in the designated folder for app
global files 
files = glob.glob('./TodoAndReminders/*.txt')

# Displays files to chose from with the associated input for choosing
def showTodoFiles():

    fileDisplayTextArea.config(state = NORMAL) # Change state of Text area to allow write

    for i in range(len(files)):

        fileDisplayTextArea.insert(END, str(i + 1) + ": " + files[i] + "\n")
        
    fileDisplayTextArea.config(state = DISABLED) # Make read-only again

# Checks if input from spinner is a valid file
def spinnerInputValidator(input):

    if input.isdigit():
        if int(input) not in range(1, len(files) + 1):
            messagebox.showerror("Invalid Range Error","Bad Input: Invalid range, select a listed file number")
            return FALSE
    else:
        messagebox.showerror("Non-digit Error","Bad Input: Not a digit") 
        return FALSE
    return TRUE

# Displays contents of file selected
def showFileContents():
    input = fileSelecter.get()

    if spinnerInputValidator(input):

        fileContentsTextArea.config(state = NORMAL) # Change state of Text area to allow write

        fileContentsTextArea.delete(1.0, END)
        index = int(input) - 1

        fOpened = open(files[index], "r")

        for line in fOpened:
            fileContentsTextArea.insert(END, line + "\n")

        fOpened.close()
        fileContentsTextArea.config(state = DISABLED) # Make read-only again


# Open new window to edit file
def newEditWindow():
    input = fileSelecter.get()

    if spinnerInputValidator(input):
        editWindow = Toplevel()

        # Sets title and size
        editWindow.title("Schedule Editing Window")
        editWindow.geometry("1400x600")

        #scrollbar setup
        textScroll = Scrollbar(editWindow, orient=VERTICAL)
        textScroll.pack(side = RIGHT, fill = Y)

        editingTextArea = Text(editWindow,
                               width = 150,
                               height = 30,
                               yscrollcommand = textScroll.set)

        editingTextArea.pack(side = RIGHT, fill = Y)

        applyEditButton = Button(editWindow,
                                 text = "Apply Changes") # Make command for apply changes
        applyEditButton.pack(side = LEFT)

        #scrollbar config
        textScroll.config(command=editingTextArea.yview)



# Main Window
mainWindow = Tk()

# mainWindow size
mainWindow.geometry('500x500')

# background color
mainWindow.config(background = "white")

# titling mainWindow
mainWindow.title("Time Manager")

selectFrame = Frame(mainWindow)

# Button: initiate command to find files
showFilesButton = Button(mainWindow,
                         text = "Show Files",
                         command = showTodoFiles)

# TextArea: display files here
fileDisplayTextArea = Text(mainWindow,
                         width = 50, height = 10,
                         state = DISABLED,
                         fg = "black",
                         bg = "lightBlue")

# Button: Read file Selected
ShowFile = Button(selectFrame,
                         text = "Show File",
                         command = showFileContents)

# Button: Edit file selected
editFileButton = Button(selectFrame,
                          text = "Edit File",
                          command = newEditWindow ) # Add command functionality

# SpinBox: Select file
fileSelecter = Spinbox(selectFrame,
                       from_=1, to = len(files) )

# TextArea: display file contents here
fileContentsTextArea = Text(mainWindow,
                         width = 50, height = 10,
                         state = DISABLED,
                         fg = "black",
                         bg = "lightBlue")

# Assign all widgets to mainWindow grid
showFilesButton.grid(column = 1, row = 1)

fileDisplayTextArea.grid(column = 1, row = 2)

selectFrame.grid(column = 1, row = 3) # Holds both widgets below that use .pack

ShowFile.pack( side = LEFT) # stacks/packs starting left, allows them to be side by side 

fileSelecter.pack( side = LEFT)

editFileButton.pack( side = LEFT )

fileContentsTextArea.grid(column = 1, row = 4)





mainWindow.mainloop()