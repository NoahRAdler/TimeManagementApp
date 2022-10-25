from tkinter import *
from tkinter import messagebox
import glob

# From current level, find all .txt files in the designated folder for app,
# Global use variables indicated as All capitalized and using _ as seperators
FILES = glob.glob('./TodoAndReminders/*.txt')
WRITE_WINDOWS_OPEN = 0
CURRENT_FILE = ""

if len(FILES) < 1:
    messagebox.showerror("No Text Files Error","No text files in TodoAndReminders folder, " 
                    +  "add at least one then restart the app.")
else:

    # Displays files to chose from with the associated input for choosing
    def showTodoFiles():

        fileDisplayTextArea.config(state = NORMAL) # Change state of Text area to allow write

        fileDisplayTextArea.delete(1.0, END)

        for i in range(len(FILES)):

            # This is probably around O(n^2) but n should be low, refactor if a much larger data set is used  
            fileDisplayTextArea.insert(END, str(i + 1) + ": " + displayStrippedPath(FILES[i]) + "\n")

            fileDisplayTextArea.insert(END, "")
        
        fileDisplayTextArea.config(state = DISABLED) # Make read-only again

    # Checks if input from spinner is a valid file
    def spinnerInputValidator(input):

        if input.isdigit():
            if int(input) not in range(1, len(FILES) + 1):
                messagebox.showerror("Invalid Range Error","Bad Input: Invalid range, select a listed file number")
                return False
        else:
            messagebox.showerror("Non-digit Error","Bad Input: Not a digit") 
            return False
        return True

    # Used to display a file name in a more readable manner, returns string
    def displayStrippedPath(pathed):

        formatted = pathed[pathed.index("\\") + 1:]

        return formatted

    # Displays contents of file selected to default read area
    def showFileContents():
        input = fileSelecter.get()

        if spinnerInputValidator(input):

            fileContentsTextArea.config(state = NORMAL) # Change state of Text area to allow write

            fileContentsTextArea.delete(1.0, END)
            index = int(input) - 1

            fOpened = open(FILES[index], "r")

            for line in fOpened:
                fileContentsTextArea.insert(END, line)

            fOpened.close()
            fileContentsTextArea.config(state = DISABLED) # Make read-only again

    # Displays contents of file to a selected read/write area
    # Arg: text area 
    def showFileContentsRW(textArea): 
        input = fileSelecter.get()
    
        if spinnerInputValidator(input):
            textArea.delete(1.0, END)
            index = int(input) - 1

            fOpened = open(FILES[index], "r")

            for line in fOpened:
                textArea.insert(END, line)

            fOpened.close()

    # Write to file
    def writeToFile(textArea):
        confirmWrite = messagebox.askquestion(
            "Confirm Change", "Are you sure you want to apply these changes to file: "
                                              + displayStrippedPath(CURRENT_FILE) + " ?")

        if confirmWrite == 'yes':
            
            fWrite = open(CURRENT_FILE, "w")

            fWrite.write(textArea.get(1.0, END))

            fWrite.close
            return True
        else:
            return False

    # Open new window to edit file
    def newEditWindow():
        input = fileSelecter.get()
        global WRITE_WINDOWS_OPEN

        if spinnerInputValidator(input) and WRITE_WINDOWS_OPEN == 0:

            # When editWindow close event
            def onClosing():
                if messagebox.askokcancel("Exit", "Do you want to exit? Changes will not be saved."):
                    global WRITE_WINDOWS_OPEN
                    WRITE_WINDOWS_OPEN -= 1
                    editWindow.destroy()

            # Used to apply the file write and close the window 
            def applyingChanges():
            
                if writeToFile(editingTextArea):
                    global WRITE_WINDOWS_OPEN   # Controls the number of editing windows open |default: 1 max
                    global APPLY_ACTIVE         # Deactivates exit alert if Apply button used in favor of apply alert

                    APPLY_ACTIVE = 0            # 0 using the bool() method results false, 1 results true
                    WRITE_WINDOWS_OPEN -= 1
                    
                    showFileContents() # run showFileContents to update the displayed contents
                    editWindow.destroy()

            global CURRENT_FILE
            CURRENT_FILE = FILES[int(input) - 1]
            editWindow = Toplevel()
            WRITE_WINDOWS_OPEN += 1
            APPLY_ACTIVE = 1

            # Sets title and size
            editWindow.title("Schedule Editing Window")
            editWindow.geometry("1400x600")

            # scrollbar setup
            textScroll = Scrollbar(editWindow, orient=VERTICAL)
            textScroll.pack(side = RIGHT, fill = Y)

            editingTextArea = Text(editWindow,
                                   width = 150,
                                   height = 30,
                                   yscrollcommand = textScroll.set)

            editingTextArea.pack(side = RIGHT, fill = Y)

            applyEditButton = Button(editWindow,
                                     text = "Apply Changes",
                                     command = applyingChanges) # Make command for apply changes
            applyEditButton.pack(side = LEFT)

            # scrollbar config
            textScroll.config(command=editingTextArea.yview)
            showFileContentsRW(editingTextArea)

            # Controls exit state of the window
            if(bool(APPLY_ACTIVE)):
                editWindow.protocol("WM_DELETE_WINDOW", onClosing)


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
                              command = newEditWindow )

    # SpinBox: Select file

    fileSelecter = Spinbox(selectFrame,
                           from_=1, to = len(FILES) )

    # TextArea: display file contents here
    fileContentsTextArea = Text(mainWindow,
                             width = 50, height = 10,
                             state = DISABLED,
                             fg = "black",
                             bg = "lightBlue")

    # Configure grid for expandable text area
    Grid.rowconfigure(mainWindow, 2, weight=1)
    Grid.rowconfigure(mainWindow, 4, weight=1)
    Grid.columnconfigure(mainWindow, 1, weight=1)

    # Assign all widgets to mainWindow grid
    showFilesButton.grid(column = 1, row = 1)

    fileDisplayTextArea.grid(column = 1, row = 2, sticky="nsew")

    selectFrame.grid(column = 1, row = 3) # Holds both widgets below that use .pack

    ShowFile.pack( side = LEFT) # stacks/packs starting left, allows them to be side by side 

    fileSelecter.pack( side = LEFT)

    editFileButton.pack( side = LEFT )

    fileContentsTextArea.grid(column = 1, row = 4, sticky="nsew")





    mainWindow.mainloop()