from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import glob

# From current level, find all .txt files in the designated folder for app,
# Global use variables indicated as All capitalized and using _ as seperators
FILES = glob.glob('./TodoAndReminders/*.txt')
WRITE_WINDOWS_OPEN = 0
CURRENT_FILE = ""

if len(FILES) < 1:
    messagebox.showerror("No Text Files Error","No text files in TodoAndReminders folder, or no folder at all. " 
                    +  "Make sure to have a TodoAndReminders folder with "
                    +   "at least one .txt file then restart the app.")
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
    # Arg: text area Object 
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



    #__________________________________________EDIT_WINDOW______________________________________________
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

            # Applys given template from comboBox, uses count if within parameters else defaults to 1
            def insertTemplate():

                # strip may be fine to remove but by no means remove the replace method, 
                # otherwise (numOfOutputs)input has \n and breaks it
                numOfOutputs = templateCountInput.get(1.0, END).strip().replace("\n","")
                template = templateComboBox.get()
                
                # Insert takes place at cursor location
                if numOfOutputs.isdigit() and int(numOfOutputs) in range(1, 101):
                    lineSpacing = len(template) - len(template.lstrip())
                    template = template.strip()

                    if bool(displayCountVarHold.get()):
                        for x in range(1, int(numOfOutputs)+1):
                            editingTextArea.insert(editingTextArea.index('insert'), " " * lineSpacing + str(x) + 
                                                   template + "\n")
                    else:
                        for x in range(1, int(numOfOutputs)+1):
                            editingTextArea.insert(editingTextArea.index('insert'), template + "\n")
                else:
                    editingTextArea.insert(editingTextArea.index('insert'), template + "\n")

            # allows the comboBox to properly use tab
            def comboBoxTabFix(event):
                
                indexTemp = templateComboBox.index('insert')
                templateComboBox.insert(indexTemp, " " * 3)
                templateComboBox.icursor(str(indexTemp) + "3")


            global CURRENT_FILE
            CURRENT_FILE = FILES[int(input) - 1]
            editWindow = Toplevel()
            WRITE_WINDOWS_OPEN += 1
            APPLY_ACTIVE = 1

            # Sets title and size
            editWindow.title("Schedule Editing Window")
            editWindow.geometry("1400x600")

            # Set corner Icon
            editWindow.iconbitmap(r'MoonQM.ico')

            editOptionFrame = Frame(editWindow)

            # scrollbar setup
            textScroll = Scrollbar(editWindow, orient=VERTICAL)
            

            editingTextArea = Text(editWindow,
                                   width = 150,
                                   height = 30,
                                   yscrollcommand = textScroll.set,
                                   undo = True)


            applyEditButton = Button(editOptionFrame,
                                     text = "Apply Changes",
                                     command = applyingChanges) 

            # applies template from combo box allowing imput or an option provided in the drop down 
            insertTemplateButton = Button(editOptionFrame,
                                         text="Insert Template",
                                         command=insertTemplate)

            
            countLabel = Label(editOptionFrame,
                               text="Number of Inserts, Up to 100" )

            # Controls how many inserts there should be up to 100
            templateCountInput = Text(editOptionFrame,
                                      width = 3,
                                      height = 1)

            # Values for Combo box
            textTemplates = [
                "",
                "[ ] CheckboxItems",
                ". NumberedItems: ",
                "   [ ] ChkBoxWithTab"
                ]

            # CheckButton Value holder
            displayCountVarHold = IntVar()

            # Gives examples for templates also allowing unique input
            templateComboBox = ttk.Combobox(editOptionFrame, value=textTemplates)

            # Controls if a count is displayed in the template
            displayCountCheck = Checkbutton(editOptionFrame,
                                            text="Display template count",
                                            variable = displayCountVarHold,
                                            offvalue = 0,
                                            onvalue = 1)

            # Place/pack into main window
            textScroll.pack(side = RIGHT, fill = Y)
            editingTextArea.pack(side = RIGHT, fill = Y)
            editOptionFrame.pack(side = LEFT)

            # Place/pack into options frame
            applyEditButton.pack(pady=25)
            insertTemplateButton.pack(pady=10)
            templateComboBox.pack()
            countLabel.pack(pady=10)
            templateCountInput.pack()
            displayCountCheck.pack(pady=10)

            # scrollbar config
            textScroll.config(command=editingTextArea.yview)

            # When Opening editWindow, this displays the file contents.
            showFileContentsRW(editingTextArea)

            # Bind hotkeys for editing
            editWindow.bind('<Control-KeyPress-Z>', editingTextArea.edit_undo)
            editWindow.bind('<Control-KeyPress-Y>', editingTextArea.edit_redo)

            # Allows use of Tab-Key in comboBox for easier template editing
            templateComboBox.unbind_all('<<NextWindow>>')
            templateComboBox.bind('<Tab>', comboBoxTabFix) 

            # Controls exit state of the window
            if(bool(APPLY_ACTIVE)):
                editWindow.protocol("WM_DELETE_WINDOW", onClosing)




    # _________________________________________Main_Window______________________________________________
    mainWindow = Tk()

    # mainWindow size
    mainWindow.geometry('500x500')

    # background color
    mainWindow.config(background = "white")

    # titling mainWindow
    mainWindow.title("Time Manager")

    # Set corner Icon
    mainWindow.iconbitmap(r'MoonQM.ico')

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

    fileSelecter.pack( side = LEFT, padx=5)

    editFileButton.pack( side = LEFT )

    fileContentsTextArea.grid(column = 1, row = 4, sticky="nsew")





    mainWindow.mainloop()