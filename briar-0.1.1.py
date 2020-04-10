import os
import requests
import json
import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle
from pathlib import Path
import sys, traceback

home = str(Path.home())
rel_path = ".briar/auth_token"
abs_file_path = os.path.join(home, rel_path)

apiURL = "http://127.0.0.1:7000"
auth =  {"Authorization" : "Bearer " + open(abs_file_path, "r").read()}

def contacts():
    url_format = apiURL + "/v1/contacts"
    response = requests.get(url_format, headers = auth)
    json_data = response.json()
    contactList = []
    for contact in json_data:
        contactList.append(contact["author"]["name"])
    return contactList

def messages(contactId, contactName):
    url_format = apiURL + "/v1/messages/" + str(contactId)
    response = requests.get(url_format, headers = auth )
    json_data = response.json()
    return json_data
    
    

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
    
    
class CursedMenu(object):
    '''A class which abstracts the horrors of building a curses-based menu system'''
    def __init__(self):
        '''Initialization'''
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        self.screen.keypad(1)

        # Highlighted and Normal line definitions
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.highlighted = curses.color_pair(1)
        self.normal = curses.A_NORMAL


    def show(self, options, title="Title", subtitle="Subtitle"):
        '''Draws a menu with the given parameters'''
        self.set_options(options)
        self.title = title.upper()
        self.subtitle = subtitle.upper()
        self.selected = 0
        self.draw_menu()


    def set_options(self, options):
        '''Validates that the last option is "Exit"'''
        if options[-1] is not 'Exit':
            options.append('Exit')
        self.options = options

    def set_submenu(self, submenu):
        '''Validates that the last option is "Exit"'''
        if submenu[-1] is not 'Exit':
            submenu.append('Exit')
        self.submenu = submenu

    def draw_dict(self):
        cfg_dict = {}
        cfg_dict['InstanceName'] = "InstanceName"
        cfg_dict['Environment'] = "Enviroment"
        cfg_dict['InstanceType'] = "InstanceType"
        cfg_dict['SystemOwner'] = "SystemOwner"
        cfg_dict['LifeCycle'] = "LifeCycle"
        cfg_dict['DeptName'] = "DeptName"
        cfg_dict['Org'] = "Org"
        self.screen.addstr(8, 35, " "*43, curses.A_BOLD)
        self.screen.addstr(10, 35," "*43, curses.A_BOLD)
        self.screen.addstr(12, 35," "*43, curses.A_BOLD)
        self.screen.addstr(14, 35," "*43, curses.A_BOLD)
        self.screen.addstr(16, 35," "*43, curses.A_BOLD)
        self.screen.addstr(18, 35," "*43, curses.A_BOLD)
        self.screen.addstr(20, 35," "*43, curses.A_BOLD)
        self.screen.addstr(8, 35, cfg_dict['InstanceName'], curses.A_STANDOUT)
        self.screen.addstr(10, 35,cfg_dict['Environment'], curses.A_STANDOUT)
        self.screen.addstr(12, 35,cfg_dict['InstanceType'], curses.A_STANDOUT)
        self.screen.addstr(14, 35,cfg_dict['SystemOwner'], curses.A_STANDOUT)
        self.screen.addstr(16, 35,cfg_dict['LifeCycle'], curses.A_STANDOUT)
        self.screen.addstr(18, 35,cfg_dict['DeptName'], curses.A_STANDOUT)
        self.screen.addstr(20, 35,cfg_dict['Org'], curses.A_STANDOUT)
        self.screen.refresh()

    def draw_menu(self):
        '''Actually draws the menu and handles branching'''
        request = ""
        try:
            while request is not "Exit":
                self.draw()
                request = self.get_user_input()
                self.handle_request(request)
            self.__exit__()

        # Also calls __exit__, but adds traceback after
        except Exception as exception:
            self.__exit__()
            traceback.print_exc()


    def draw(self):
        '''Draw the menu and lines'''
        self.screen.border(0)
        self.screen.subwin(7, 15, 3, 1).box()
        self.screen.addstr(1,30, self.title, curses.A_STANDOUT|curses.A_BOLD) # Title for this menu
        self.screen.hline(2, 1, curses.ACS_HLINE, 78)
        self.screen.addstr(3,2, self.subtitle, curses.A_BOLD) #Subtitle for this menu

        # Display all the menu items, showing the 'pos' item highlighted
        y = 4
        for index in range(len(self.options)):
            menu_name = len(self.options[index])
            textstyle = self.normal
            if index == self.selected:
                textstyle = self.highlighted
            self.screen.addstr(y, 2, "%d.%s" % (index+1, self.options[index]), textstyle)
            y += 1
        #self.draw_dict()
        self.screen.refresh()

    def get_user_input(self):
        '''Gets the user's input and acts appropriately'''
        user_in = self.screen.getch() # Gets user input

        '''Enter and Exit Keys are special cases'''
        if user_in == 10:
            return self.options[self.selected]
        if user_in == 27:
            return self.options[-1]
        if user_in == (curses.KEY_END, ord('!')):
            return self.options[-1]

        # This is a number; check to see if we can set it
        if user_in >= ord('1') and user_in <= ord(str(min(9,len(self.options)+1))):
            self.selected = user_in - ord('0') - 1 # convert keypress back to a number, then subtract 1 to get index
            return

        # Increment or Decrement
        if user_in == curses.KEY_UP: # left arrow
            self.selected -=1
        if user_in == curses.KEY_DOWN: # right arrow
            self.selected +=1
        self.selected = self.selected % len(self.options)
        return



    def handle_request(self, request):
        '''This is where you do things with the request'''
        if request is "Contacts":
           self.draw_submenu(request, contacts(), 8, 20, 3, 16)
        elif request is "Groups":
           self.org_func()
        elif request is "Forums":
           self.org_func()
        elif request is "Blogs":
           self.org_func()
        if request is None: return

    def draw_submenu(self, subtitle, submenu, lines, cols, h, w):
        '''Actually draws the submenu and handles branching'''
        c = None
        self.option = 0
        self.set_submenu(submenu)
        height = len(self.submenu)
        while c != 10:
            self.s = curses.newwin(height+lines, cols, h, w)
            self.s.keypad(1)
            self.s.box()
            self.s.addstr(0,1, subtitle.upper(), curses.A_BOLD) #Subtitle for this menu
            
            for index in range(len(self.submenu)):
                textstyle = self.normal
                if index == self.option:
                    textstyle = self.highlighted
                self.s.addstr(index+1,1, "%d-%s" % (index+1, self.submenu[index]), textstyle)
            self.s.refresh()
            c = self.s.getch() # Gets user input
            
        # This is a number; check to see if we can set it
            if c >= ord('1') and c <= ord(str(len(self.submenu)+1)):
                self.option = c - ord('0') - 1 # convert keypress back to a number, then subtract 1 to get index
       # Increment or Decrement
            elif c == curses.KEY_DOWN: # down arrow
                if self.option < len(self.submenu):
                    self.option += 1
                else: self.option = 0
            elif c == curses.KEY_UP: # up arrow
                if self.option > 0:
                    self.option -= 1
                else: self.option = len(self.submenu)
        '''if c == 10:
            #d = self.submenu[self.option]
            d = str(self.option+1)
            self.s.addstr(6,1, d)
            self.s.refresh()
        self.s.getch()'''
        return self.draw_submenu(self.submenu[self.option],messages(self.option+1, self.submenu[self.option]),8,20,3,16)

    def __exit__(self):
        curses.endwin()
        os.system('clear')


'''demo'''
cm = CursedMenu()
cm.show(['Contacts','Groups','Forums','Blogs'], title='Briar Linux Client 0.0.1v', subtitle='Main Menu')
