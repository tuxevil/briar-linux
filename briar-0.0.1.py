import os
import requests
import json
import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle
from pathlib import Path


__author__ = "Sebastian Real"
##test de commit 2

stdscr = curses.initscr()

curses.noecho()
curses.cbreak()
stdscr.keypad(True)

home = str(Path.home())
rel_path = ".briar/auth_token"
abs_file_path = os.path.join(home, rel_path)

apiURL = "http://127.0.0.1:7000"
auth =  {"Authorization" : "Bearer " + open(abs_file_path, "r").read()}


def contacts(stdscr):
    url_format = apiURL + "/v1/contacts"
    response = requests.get(url_format, headers = auth)
    json_data = response.json()
    contactlist = []
    
    draw_window(stdscr, "Briar Linux Client", "Press the number (x) of contacts to see messages or 'e' to exit")
    # Centering calculations
    height, width = stdscr.getmaxyx()
    z = 18
    x, y = int((width // 2) - (z // 2) - z % 2), 3
    stdscr.addstr(y-1,x,"Contacts", curses.color_pair(2))
    
    contactList = []
    for contact in json_data:
        contactlist.append(str(contact["contactId"]))
        stdscr.addstr(y, x, "(" + str(contact["contactId"]) + ")")
        stdscr.addstr(y, x+5, contact["author"]["name"])
        contactList.append(contact["author"]["name"])
        y += 1
        
    stdscr.refresh()
    
    # Wait for next input
    k = stdscr.getkey()
    if k in contactlist:    
        messages(stdscr, k, contactList[int(k)-1])
    elif k == 'e':
        menu(stdscr)
    else:
        error(stdscr)
        contacts(stdscr)

def messages(stdscr, contactId, contactName):
    url_format = apiURL + "/v1/messages/" + contactId
    response = requests.get(url_format, headers = auth )
    json_data = response.json()
    
    draw_window(stdscr, "Briar Linux Client", "Press anykey to refresh or 'n' to send new message or press 'e' to exit")
    # Centering calculations
    height, width = stdscr.getmaxyx()
    z = 18
    x, y = int((width // 2) - (z // 2) - z % 2), 3
    stdscr.addstr(y-1,x,"Messages with: " + contactName, curses.color_pair(2))
    
    for msg in json_data:
        message(stdscr, msg, y)
        y += 1
        
    stdscr.refresh()
    k = stdscr.getch()
    
    if k == ord('n'):
        send(stdscr, contactId, contactName)
    elif k == ord('e'):
        menu(stdscr)
    else: messages(stdscr, contactId)

def message(stdscr, message, y):
    #varibles for the other's person messages
    color, x = 6, 3
    #change variables if is our own messages
    if message["local"] == True:
        color, x = 5, 20
    #apply variables and print the text
    stdscr.attron(curses.color_pair(color))
    stdscr.addstr(y, x, message["text"])
    stdscr.attroff(curses.color_pair(color))

def send(stdscr, contactId, contactName):
    draw_window(stdscr, "Briar Linux Client", "Type your message and press Ctrl+G to send")
    # Centering calculations
    height, width = stdscr.getmaxyx()
    z = 18
    x, y = int((width // 2) - (z // 2) - z % 2), 3
    stdscr.addstr(y-1,x,"New message for: " + contactName, curses.color_pair(2))
    
    ncols, nlines = 40, 5
    uly, ulx = 5, 2
    editwin = curses.newwin(nlines, ncols, uly, ulx)
    rectangle(stdscr, uly-1, ulx-1, uly + nlines, ulx + ncols)
    stdscr.refresh()

    box = Textbox(editwin)
    # Let the user edit until Ctrl-G is struck.
    box.edit()
    # Get resulting contents
    message = box.gather()
    
    if message != "":
        url_format = apiURL + "/v1/messages/" + contactId
        response = requests.post(url_format, headers = auth, json = {"text":message} )
        stdscr.addstr(20,10, "Message sent")
    else:
        stdscr.addstr(20,10, "Message empty", curses.color_pair(4) )
    stdscr.refresh()
    stdscr.getch()
    
    messages(stdscr, contactId, contactName)


###########################################################################################
### TODO
###########################################################################################
def addContact():
    url_format = apiURL + "/v1/contacts/add/link"
    response = requests.get(url_format, headers = auth )
    print(response.json()) 
    
    url_format = apiURL + "/v1/contacts/add/pending"
    response = requests.post(url_format, headers = auth )
    print(response.json()) 
    
def delContact():
    _id = input("Id a eliminar: ")
    url_format = apiURL + "/v1/contacts/" + _id
    response = requests.delete(url_format, headers = auth )
    print(response.json()) 



############################################################################################
def error(stdscr):
    stdscr.addstr(20, 20, "Wrong option!", curses.color_pair(4))
    stdscr.refresh()
    stdscr.getch()
    
def draw_window(stdscr, title, statusbarstr):
    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()
    height, width = stdscr.getmaxyx()

    # Start colors in curses
    curses.start_color()
    #color de titulo
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)
    #colores de mensajes
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_CYAN)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLUE)
    

    # Centering calculations
    start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
    start_y = 1 

    stdscr.border(0)
    
    # Render status bar
    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(height-2, 1, statusbarstr)
    stdscr.addstr(height-2, len(statusbarstr)+1, " " * (width - len(statusbarstr) - 2))
    stdscr.attroff(curses.color_pair(3))

    # Turning on attributes for title
    stdscr.attron(curses.color_pair(1))
    stdscr.attron(curses.A_BOLD)

    # Rendering title
    stdscr.addstr(start_y, start_x_title, title)

    # Turning off attributes for title
    stdscr.attroff(curses.color_pair(1))
    stdscr.attroff(curses.A_BOLD)
    
def menu(stdscr):
    draw_window(stdscr, "Briar Linux Client", "Press 'c' for contacts 'g' for groups 'f' for forums 'b' for blogs or 'e' to exit")
    
    height, width = stdscr.getmaxyx()
    # Centering calculations
    start_x_subtitle = int((width // 2) - (len("Main Menu") // 2) - len("Main Menu") % 2)
    start_y = 2 

    # Print rest of text
    stdscr.addstr(start_y,start_x_subtitle,"Main Menu", curses.color_pair(2))
    stdscr.addstr(start_y + 2,start_x_subtitle,"(C)ontacts")
    stdscr.addstr(start_y + 3,start_x_subtitle,"(G)roups")
    stdscr.addstr(start_y + 4,start_x_subtitle,"(F)orums")
    stdscr.addstr(start_y + 5,start_x_subtitle,"(B)logs")
    stdscr.addstr(start_y + 6,start_x_subtitle,"(E)xit")
    

    # Refresh the screen
    stdscr.refresh()

    # Wait for next input
    k = stdscr.getch()
    
    if k == ord('c'):
        contacts(stdscr)
    elif k == ord('g'):
        groups()
    elif k == ord('f'):
        forums()
    elif k == ord('b'):
        blogs()
    elif k == ord('e'):
        exit()
    else:
        error(stdscr)
        menu(stdscr)

def main():
    curses.wrapper(menu)

if __name__ == "__main__":
    main()

