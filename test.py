import os
import requests
import json
import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle
from pathlib import Path

stdscr = curses.initscr()

curses.noecho()
curses.cbreak()
stdscr.keypad(True)

home = str(Path.home())
rel_path = ".briar/auth_token"
abs_file_path = os.path.join(home, rel_path)

apiURL = "http://127.0.0.1:7000"
auth =  {"Authorization" : "Bearer " + open(abs_file_path, "r").read()}

def contacts():
    url_format = apiURL + "/v1/contacts"
    response = requests.get(url_format, headers = auth)
    json_data = response.json()
    contactlist = []
    
    for contact in json_data:
        contactlist.append( { "id" : str(contact["contactId"]), "name" : contact["author"]["name"] } )
        
    return contactlist


def menuitems(win, item, selected, y, x):
    win.attron(curses.color_pair(3))
    if selected != True:
        win.attron(curses.A_REVERSE)
    win.addstr(y, x, item)
    if selected != True:
        win.attroff(curses.A_REVERSE)
    win.attroff(curses.color_pair(3))


def menuBox(menuWin):
    # Long strings will wrap to the next line automatically
    # to stay within the window
    start_y = 1
    start_x = 1
    menuWin.border(0)

    menuindex = 0
    menuWin.addstr(start_y,start_x,"MAIN MENU", curses.color_pair(2))
    menuitems(menuWin, "Contacts", True, start_y+2, start_x)
    menuitems(menuWin, "Groups", False, start_y+3, start_x)
    menuitems(menuWin, "Forums", False, start_y+4, start_x)
    menuitems(menuWin, "Blogs", False, start_y+5, start_x)
    menuitems(menuWin, "Exit", False, start_y+7, start_x)



    # Print the window to the screen
    menuWin.refresh()


    while True:
        k = menuWin.getch()

        if k == ord('s'):#258:
            if menuindex == 0:
                menuindex = 1
                menuitems(menuWin, "Contacts", False, start_y+2, start_x)
                menuitems(menuWin, "Groups", True, start_y+3, start_x)
            elif menuindex == 1:
                menuindex = 2
                menuitems(menuWin, "Groups", False, start_y+3, start_x)
                menuitems(menuWin, "Forums", True, start_y+4, start_x)
            elif menuindex == 2:
                menuindex = 3
                menuitems(menuWin, "Forums", False, start_y+4, start_x)
                menuitems(menuWin, "Blogs", True, start_y+5, start_x)
            elif menuindex == 3:
                menuindex = 4
                menuitems(menuWin, "Blogs", False, start_y+5, start_x)
                menuitems(menuWin, "Exit", True, start_y+7, start_x)
            elif menuindex == 4:
                menuindex = 0
                menuitems(menuWin, "Contacts", True, start_y+2, start_x)
                menuitems(menuWin, "Exit", False, start_y+7, start_x)
        elif k == ord('w'):#259:
            if menuindex == 0:
                menuindex = 4
                menuitems(menuWin, "Contacts", False, start_y+2, start_x)
                menuitems(menuWin, "Exit", True, start_y+7, start_x)
            elif menuindex == 1:
                menuindex = 0
                menuitems(menuWin, "Groups", False, start_y+3, start_x)
                menuitems(menuWin, "Contacts", True, start_y+2, start_x)
            elif menuindex == 2:
                menuindex = 1
                menuitems(menuWin, "Forums", False, start_y+4, start_x)
                menuitems(menuWin, "Groups", True, start_y+3, start_x)
            elif menuindex == 3:
                menuindex = 2
                menuitems(menuWin, "Blogs", False, start_y+5, start_x)
                menuitems(menuWin, "Forums", True, start_y+4, start_x)
            elif menuindex == 4:
                menuindex = 3
                menuitems(menuWin, "Exit", False, start_y+7, start_x)
                menuitems(menuWin, "Blogs", True, start_y+5, start_x)
        elif k == 10:
            if menuindex == 0:
                contactBox(curses.newwin(15, 20, 0, 21))
            elif menuindex == 1:
                menuindex = 0
                menuitems(menuWin, "Groups", False, start_y+3, start_x)
                menuitems(menuWin, "Contacts", True, start_y+2, start_x)
            elif menuindex == 2:
                menuindex = 1
                menuitems(menuWin, "Forums", False, start_y+4, start_x)
                menuitems(menuWin, "Groups", True, start_y+3, start_x)
            elif menuindex == 3:
                menuindex = 2
                menuitems(menuWin, "Blogs", False, start_y+5, start_x)
                menuitems(menuWin, "Forums", True, start_y+4, start_x)
            elif menuindex == 4:
                return
            
        menuWin.refresh()
            

    curses.endwin()


def contactBox(contactWin):
    contactlist = contacts()
    # Long strings will wrap to the next line automatically
    # to stay within the window
    start_y = 1
    start_x = 1
    contactWin.border(0)

    menuindex = 0
    contactWin.addstr(start_y,start_x,"CONTACTS", curses.color_pair(2))
    start_y += 2
    selected = True
    contactIndex = 0
    for contact in contactlist:
            menuitems(contactWin, contact["name"], selected, start_y, start_x)
            selected = False
            start_y += 1

    # Print the window to the screen
    contactWin.refresh()
''' no esta hecho
    while True:
        k = contactWin.getch()

        if k == ord('s'):#258:
            if contactIndex == 0:
                contactIndex = 1
                menuitems(menuWin, "Contacts", False, start_y+2, start_x)
                menuitems(menuWin, "Groups", True, start_y+3, start_x)
            elif contactIndex == 1:
                contactIndex = 2
                menuitems(menuWin, "Groups", False, start_y+3, start_x)
                menuitems(menuWin, "Forums", True, start_y+4, start_x)
            elif contactIndex == 2:
                contactIndex = 3
                menuitems(menuWin, "Forums", False, start_y+4, start_x)
                menuitems(menuWin, "Blogs", True, start_y+5, start_x)
            elif contactIndex == 3:
                contactIndex = 4
                menuitems(menuWin, "Blogs", False, start_y+5, start_x)
                menuitems(menuWin, "Exit", True, start_y+7, start_x)
            elif contactIndex == 4:
                contactIndex = 0
                menuitems(menuWin, "Contacts", True, start_y+2, start_x)
                menuitems(menuWin, "Exit", False, start_y+7, start_x)
        elif k == ord('w'):#259:
            if menuindex == 0:
                menuindex = 4
                menuitems(menuWin, "Contacts", False, start_y+2, start_x)
                menuitems(menuWin, "Exit", True, start_y+7, start_x)
            elif menuindex == 1:
                menuindex = 0
                menuitems(menuWin, "Groups", False, start_y+3, start_x)
                menuitems(menuWin, "Contacts", True, start_y+2, start_x)
            elif menuindex == 2:
                menuindex = 1
                menuitems(menuWin, "Forums", False, start_y+4, start_x)
                menuitems(menuWin, "Groups", True, start_y+3, start_x)
            elif menuindex == 3:
                menuindex = 2
                menuitems(menuWin, "Blogs", False, start_y+5, start_x)
                menuitems(menuWin, "Forums", True, start_y+4, start_x)
            elif menuindex == 4:
                menuindex = 3
                menuitems(menuWin, "Exit", False, start_y+7, start_x)
                menuitems(menuWin, "Blogs", True, start_y+5, start_x)
        elif k == 10:
            if menuindex == 0:
                contactBox(curses.newwin(15, 20, 0, 21))
            elif menuindex == 1:
                menuindex = 0
                menuitems(menuWin, "Groups", False, start_y+3, start_x)
                menuitems(menuWin, "Contacts", True, start_y+2, start_x)
            elif menuindex == 2:
                menuindex = 1
                menuitems(menuWin, "Forums", False, start_y+4, start_x)
                menuitems(menuWin, "Groups", True, start_y+3, start_x)
            elif menuindex == 3:
                menuindex = 2
                menuitems(contactWin, "Blogs", False, start_y+5, start_x)
                menuitems(contactWin, "Forums", True, start_y+4, start_x)
            elif menuindex == 4:
                return
            
        contactWin.refresh()
    
    
    k = contactWin.getch()

   '''    
            





def main(main_screen):
    # The `screen` is a window that acts as the master window
    # that takes up the whole screen. Other windows created
    # later will get painted on to the `screen` window.
    screen = curses.initscr()
    

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
    # lines, columns, start line, start column
    menuBox(curses.newwin(15, 20, 0, 0))
    
    raise Exception

wrapper(main)
