from guizero import App, TextBox, PushButton, Box, MenuBar, ListBox, Text
from os import remove
from microfs import ls, rm, put, get, get_serial
from uflash import find_microbit, flash
from random import choice
#import sys # just for a clean exit when using pyinstaller
from sys import exit

temp_file = '.tmp'
file_name = ''
icons_file = "icons"

### functions ###
def check_connection():
    path = find_microbit()
    if path == None:
        status_text.value = "< microbit not mounted >"
    else:
        status_text.value = "< microbit mounted >"
    try:
        microbit = get_serial()
        status_text.value = status_text.value +" < serial connected >"
        return microbit
    except IOError as error:
        list_box.clear()
        view.value = error
        
def list_files():
    edit_finish()
    microbit = check_connection()
    file_list = ls(microbit)
    if file_list == []:
        list_box.clear()
        list_box.append("No files on Microbit")
        return
    else:
        list_box.clear()
        for file in file_list:
            list_box.append(file)

def view_file():
    global file_name
    edit_finish()
    microbit = check_connection()
    file_name = list_box.value
    try:
        if file_name != None:
            get(file_name, target=temp_file, serial=microbit)
        else:
            view.value = "Please select a file. Click List for file list"
            return
    except IOError as error:
        view.value = str(error) + " {}".format(temp_file)
    with open(temp_file) as file:
        view.value = file.read()
    #remove(temp_file)

def download_file():
    global file_name
    edit_finish()
    microbit = check_connection()
    file_name = list_box.value
    try:
        if file_name != None:
            get(file_name, target=temp_file, serial=microbit)
        else:
            view.value = "Please select a file. Click List for file list"
            return
    except IOError as error:
        view.value = str(error) + " {}".format(file_name)
    with open(temp_file) as file:
        tmp_data = file.read()
    remove(temp_file)    
    
    file_returned = app.select_file(filetypes=[["All files", "*.*"], ["Text documents", "*.txt"]], save=True)
    if file_returned != (): 
        with open(file_returned, 'w') as file:
            file.write(tmp_data)
        view.value = "Downloaded to {}".format(file_returned)
        tmp_data = ""
    else:
        return

def upload_file():
    edit_finish()
    microbit = check_connection()
    file_returned = app.select_file(filetypes=[["All files", "*.*"], ["Text documents", "*.txt"]])
    if file_returned != ():
        try:
            put(file_returned, serial=microbit)
            view.value = "Uploaded {} to Microbit".format(file_returned)
            list_files()
        except IOError as error:
            view.value = str(error) + " {}".format(file_returned)
    else:
        return
        
def delete_file():
    global file_name
    edit_finish()
    microbit = check_connection()
    file_name = list_box.value
    try:
        if file_name != None:
            check = app.yesno("Delete Warning!",
                                "Delete {} from Microbit permanently?\nCannot be undone!"
                              .format(file_name))
            if check == True:
                rm(file_name, serial=microbit)
                view.value = "Deleted {} from Microbit".format(file_name)
                list_files()
            else:
                return
        else:
            view.value = "Please select a file. Click List for file list"
            return
    except IOError as error:
        view.value = str(error) + " {}".format(file_name)
        
def edit_finish():
    #view.value = ""
    edit_button.image = icons_file+"{}".format("/edit.png")
    edit_button.width = 138
    edit_button.height = int(md_buttons.height)
    if view.bg == "white":
        view.tk.config(insertbackground="white")
    else:
        view.tk.config(insertbackground="black")
        
    edit_button.update_command(edit_file)
    try:
        with open(temp_file) as file:
            temp_data = file.read
        temp_data = ""
        #remove(temp_file)
    except:
        return
        
        
def save_file():
    global file_name
    microbit = check_connection()
    #file_name = list_box.value
    try:
        if file_name != None:
            check = app.yesno("Save Warning!",
                                "Overwrite {} on the Microbit?\nCannot be undone!".format(file_name))
            if check == True:
                with open(temp_file, 'w') as file:
                    file.write(view.value)
                try:
                    put(temp_file, target=file_name, serial=microbit)
                    view.value = "Uploaded {} to Microbit".format(file_name)
                    list_files()
                    remove(temp_file)
                    edit_finish()
                except IOError as error:
                    view.value = str(error) + " {}".format(file_name)
            else:
                return
        else:
            return
    except IOError as error:
        view.value = str(error) + " {}".format(file_name)
    
def edit_file():
    global file_name
    microbit = check_connection()
    file_name = list_box.value
    try:
        if file_name != None:
            check = app.yesno("Edit Warning!",
                                "Edit {}?\nNot recommended.\nYou must Save any changes\nor they will be lost.".format(file_name))
            if check == True:
                edit_button.image = icons_file+"{}".format("/save.png")
                edit_button.width = 138
                edit_button.height = int(md_buttons.height)
                get(file_name, target=temp_file, serial=microbit)
                with open(temp_file) as file:
                    view.value = file.read()
                view.focus()
                edit_button.update_command(save_file)
                if view.bg == "white":
                    view.tk.config(insertbackground="black")
                else:
                    view.tk.config(insertbackground="white")
            else:
                edit_finish()
                return
        else:
            view.value = "Please select a file. Click List for file list"
            return
    except IOError as error:
        view.value = str(error) + " {}".format(file_name)
        
def double_click():
    view_file()

def exit_app():
    edit_finish()
    exit(0)
    
def dark_theme():
    list_box.bg = "black"
    list_box.text_color = "white"
    view.bg = "black"
    view.text_color = "white"
    view.tk.config(insertbackground="black")
    
def light_theme():
    list_box.bg = "white"
    list_box.text_color = "black"
    view.bg = "white"
    view.text_color = "black"
    view.tk.config(insertbackground="white")
    
def flash_mp():
    path = find_microbit()
    if path == None:
        view.value = "Please check Microbit is plugged in and mounted. Unplug and replug may help."
        return
    else:
        check = app.yesno("Flash Warning", "Flash MicroPython to Microbit and create file system?\nAll data on Microbit will be lost.")
        if check == True:
            flash()
        else:
            return
    
### here we define the app ### 
app = App(title = "MicroFS Manager", width = "980", height = "500")
## pick a random background colour and set the font
colours = ["red", "green", "light blue", "yellow"] # blue is too dark so using light blue
app.bg = choice(colours)
app.text_color = "white"
app.font = "verdana"
app.text_size = 12

## menu ##
menubar = MenuBar(app,
                # These are the menu options
                toplevel=["File", "Create", "Options", "Help", "About"],
                # The options are recorded in a nested lists, one list for each menu option
                # Each option is a list containing a name and a function
                options=[
                    [ ["List Files", list_files],
                      ["View File", view_file],
                      ["Download File", download_file],
                      ["Upload File", upload_file],
                      ["Delete File", delete_file],
                      ["Exit", exit_app] ],
                    [ ["Flash MicroPython to Microbit", flash_mp] ],
                    [ ["Dark theme", dark_theme],
                      ["Light theme", light_theme] ],
                    [ ["List - Lists the files on the Microbit file system", None],
                      ["View - View the contents of the selected file", None],
                      ["Download - Download the selected file from the microbit to the computer. The file remains on Microbit", None],
                      ["Upload - Upload a file from the computer to the Microbit", None],
                      ["Delete - Delete the selected file from the Microbit", None],
                      ["Edit - Allows basic editing of the file on the Microbit. To cancel, click View", None],
                      ["Save - Saves an edited file to the Microbit", None],
                      ["Exit - Leave MicroFS Manager", None] ],
                    [ ["MicroFS Manager V1.0 - By Tim Wornell 2022", None],
                      ["Dodgey Icons Copyright 2022 Tim Wornell", None] ]
                    ])

## space box
blank_box = Text(app, height="fill", width="fill", text=" ",align="top", size=5)
## button box
md_buttons = Box(app, align="top", width="fill", height=int(app.height/4))

## buttons in button box
list_button = PushButton(md_buttons, command=list_files, image=icons_file+"{}".format("/list.png"),
                         align="left", width=138, height=int(md_buttons.height))
view_button = PushButton(md_buttons, command=view_file, image=icons_file+"{}".format("/view.png"),
                         align="left", width=138, height=int(md_buttons.height))
download_button = PushButton(md_buttons, command=download_file, image=icons_file+"{}".format("/download2.png"),
                             align="left", width=138, height=int(md_buttons.height))
upload_button = PushButton(md_buttons, command=upload_file, image=icons_file+"{}".format("/upload.png"),
                           align="left", width=138, height=int(md_buttons.height))
delete_button = PushButton(md_buttons, command=delete_file, image=icons_file+"{}".format("/delete.png"),
                           align="left", width=138, height=int(md_buttons.height))
edit_button = PushButton(md_buttons, command=edit_file, image=icons_file+"{}".format("/edit.png"),
                         align="left", width=138, height=int(md_buttons.height))
exit_button = PushButton(md_buttons, command=exit_app, image=icons_file+"{}".format("/exit.png"),
                         align="left", width=138, height=int(md_buttons.height))

## list of the buttons
buttons = [list_button, view_button, download_button, upload_button, delete_button, edit_button, exit_button]

## remove the button borders and movement when clicked.
for button in buttons:
    button.tk.config(highlightthickness=0, bd=0, relief="sunken")


## box to hold the info text boxes
info_box = Box(app, align="top", width="fill")
if app.bg == "blue":
    info_box.text_color = "white"
else:
    info_box.text_color = "black"
## info text boxes
file_box = Text(info_box, height="fill", width=int(app.width/30), text="Files on Microbit",align="left")
message_box = Text(info_box, align="left", height="fill", width="fill", text="Output")

#status box and text
status_box = Box(app, align="bottom", width="fill", height="fill")
filling_box = Box(status_box, align="right", width="fill", height="fill")
status_text = Text(status_box, text="", width=40, height="fill", align="left", color="black")

## list files box and view/edit box
list_box = ListBox(app, height="fill", width=int(app.width/3), align="left")
view = TextBox(app, multiline=True, height="fill", width="fill", align="right",
                scrollbar=True)
view.wrap = False

## set dark theme as default, start double click and list the files on start up
dark_theme()
list_box.when_double_clicked = double_click
list_files()
## start the app
app.display()
