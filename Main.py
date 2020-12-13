# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 14:49:07 2019

@author: user
"""

from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
#to display images
from datetime import datetime
from canteendatabase import *
import time
from time import strftime
import calendar
from random import randint


# BOON JUEY
class nscanteenapp(tk.Tk):
    #initialise the program as it executes
    #when call upon main_GUI, always runs
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #*args in function definitions in python is used to pass a variable number of arguments to a function
        #**kwargs in function definitions in python is used to pass a keyworded, variable-length argument list.
        
        tk.Tk.title(self,"NTU-Makan")
        
        container = Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0,  weight=1)
        container.grid_columnconfigure(0,  weight=1)
        
        self.frames = {}
        
        for F in (StartPage, StoreList1, UserInputTime, StoreList2, UserInputPrice, Storeohs):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        
        self.show_frame(StartPage)
    
    
    def show_frame(self, cont):
        #function to raise a certain frame to the top
         frame = self.frames[cont]
         frame.tkraise()         
    
    budget_exists = 'yes'
    budget_range = [0, 1000]
    #global value for budget
    
    def set_default_budget(self):
    #sets default value for budget
        global budget_exists
        budget_exists = 'yes'
        global budget_range
        budget_range = [0, 1000]
    
    halal = False
    #global value for halal or not
    def set_halal_true(self):
    #sets global value for halal to true
        global halal
        halal = True
    def set_halal_false(self):
    #sets global value for halal to false
        global halal
        halal = False

    def after_set_price(self):
    #what to show, according to if budget exists, or if halal option is selected
        if budget_exists == 'yes' and halal == False:
            self.show_frame(StoreList1)
        
        elif budget_exists == 'yes' and halal == True:
            self.show_frame(StoreList2)

       
        elif budget_exists == 'no':
            window = tk.Toplevel(self)
            Label(window, \
                  width = 25, \
                  height = 6, \
                  bg = 'red', \
                  fg = 'white', \
                  text="Please key in an\n approporiate value\nfor the prices").grid(row=0, column=0)   
            window.resizable(0,0)
            
    def user_input_price_button(self, lowerlimit, higherlimit):
        #command to run the 2 functions
        self.check_budget_exists(lowerlimit, higherlimit)
        self.after_set_price()
    
    def check_budget_exists(self, lowerlimit, higherlimit):
        #ensure that user input budget is legitimate
        x = 0
        
        try:
        #make sure the range is: lower value to higher value
            lowerlimit = float(lowerlimit.get())
            higherlimit = float(higherlimit.get())
        except:
            pass
                                
        try:
            if 0 <= lowerlimit and lowerlimit <= higherlimit:
                x += 1
            else:
                pass
        except:
            pass
        
            
        if x == 1:
            global budget_range
            global budget_exists
            budget_exists = 'yes'
            budget_range = [lowerlimit, higherlimit]

    
        else:
            budget_exists = 'no'
    
    sort_time = 0
    day_of_week = 0
    #global value for the time to check by, and the day of the week
    
    datetime_exists = 'no'
    def check_datetime_exists(self, day, month, year, hours, minutes):
        x = 0
        
        try:
            day = str(day.get())
            month = str(month.get())
            year = str(year.get())
            hours = str(hours.get())
            minutes = str(minutes.get())
        except:
            pass
                                
        try:
            if len(day) == 2 and len(month) == 2 and len(year) == 4 and len(hours) == 2 and len(minutes) ==2:
            #if the length of each input follows the format DD/MM/YYYY  :  HH/MM
                if 0 <= int(hours) <= 23 and 0 <= int(minutes) <= 59:
                #if the hours and minute entries are legitimate 
                    x += 1
                else:
                    pass
            else:
                pass
        except:
            pass
        
        check = day + '/' + month + '/' + year
        try:
            datetime.strptime(check, '%d/%m/%Y')
            #make sure the date is an existing one
            x += 1
        except:
                pass
            
        set_time = ''
        if x == 2:
        #it passed both checks
            global datetime_exists
            datetime_exists = 'yes'

            set_time = check + ' ' + hours + ':' + minutes
            global sort_time
            sort_time = set_time
            global day_of_week
            day_of_week = calendar.weekday(int(year), int(month), int(day))
            days = ["Monday","Tuesday","Wednesday","Thursday","Friday", "Saturday", "Sunday"]
            for x in range(7):
                if day_of_week == x:
                    day_of_week = days[x]
        else:
            datetime_exists = 'no'
    
    def after_set_time(self):
    #what to show the user, depending on if the date entered is legitimate or not
        if datetime_exists == 'yes':
            self.show_frame(UserInputPrice)
        elif datetime_exists == 'no':
        #creates a pop-up window to warn the user
            window = tk.Toplevel(self)
            Label(window, \
                  width = 25, \
                  height = 6, \
                  bg = 'red', \
                  fg = 'white', \
                  text="Please key in an\n approporiate/ existing date\nand time\n in the format:\ndd/mm/yy\nhh/mm").grid(row=0, column=0)
    
    def user_input_time_button(self, day, month, year, hours, minutes):
    #command to run the 2 functions
        self.check_datetime_exists(day, month, year, hours, minutes)
        self.after_set_time()
    
    def set_current_time(self):
    #set global value for time and day, to current system values
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        global sort_time
        sort_time = dt_string
        day_string = now.strftime("%A")
        global day_of_week
        day_of_week = day_string
    
    
    def create_window_wait_time(self, timeperperson):
    #if waiting time is selected for any specific store, this window appears
        window = tk.Toplevel(self)
        
        def waittime(*args):
            try:
                value = int(peopleno.get())
                time_output.set((timeperperson * value))
            except:
                time_output.set('-')

        
        for x in range(2):
            for y in range(2):
                Label(window, \
                      width = 14, \
                      height = 4, \
                      bg = 'light blue', \
                      text="").grid(row=y, column=x)
        
        for y in range(2):
            Label(window, \
                  width = 6, \
                  height = 4, \
                  bg = 'light blue', \
                  text="").grid(row=y, column=2)
        
        for x in range(2):
            Label(window, \
                  width = 14, \
                  height = 2, \
                  bg = 'light blue', \
                  text="").grid(row=2, column=x)
        
        Label(window, \
              width = 6, \
              height = 2, \
              bg = 'light blue', \
              text="").grid(row=2, column=2)
                
        Label(window, \
              width = 14, \
              bg = 'light blue', \
              fg = 'black', \
              text="Number of people\nin front of you:").grid(row=0, column=0, sticky=(N,S,W,E))
        
        Label(window, \
              width = 6, \
              bg = 'light blue', \
              fg = 'black', \
              text="people").grid(row=0, column=2, sticky=(W))
        
        Button(window, \
              width = 8, \
              bg = 'grey', \
              fg = 'black', \
              command = waittime, \
              text="Calculate").grid(row=2, column=0, sticky=(E,W))

        peopleno = StringVar()
        time_output = StringVar()
        
        Entry(window, width=12, textvariable=peopleno).grid(row=0, column=1) 
        #get entry for number of people queuing in front
        
        Label(window, \
              width = 12, \
              bg = 'light blue', \
              fg = 'red', \
              font='Arial 10 bold', \
              textvariable=time_output).grid(row=1, column=1)

        Label(window, \
              width = 14, \
              bg = 'light blue', \
              fg = 'black', \
              text="You will need to\nwait for around:").grid(row=1, column=0, sticky=(N,S,W,E))
        
        Label(window, \
              width = 6, \
              bg = 'light blue', \
              fg = 'black', \
              text="minutes").grid(row=1, column=2, sticky=(W))
        
        window.resizable(0,0)
    

            
    def create_menu(self, menu):
        window = tk.Toplevel(self)
            
        canvas = Canvas(window, width=640, height=720)
        image = ImageTk.PhotoImage(Image.open('menublank.jpg'))
        self.image = image
        canvas.pack()
        canvas.create_image(0, 0, anchor=NW, image=image)
        
        timeperperson = sum(menu["wtime"]) / len(menu["wtime"])
        waitbutton = Button(window, \
                            width = 11, \
                            bg = 'grey', \
                            fg = 'black', \
                            text="Waiting Time", \
                            command=lambda: self.create_window_wait_time(timeperperson), anchor = W)
        waitbutton.configure(width = 11, activebackground = "grey")
        canvas.create_window(450, 65, anchor=NW, window=waitbutton)  
        
        comparetime = int(sort_time[11:13] + sort_time[14:16])
        if day_of_week in menu["day"]:
        #if the store is open on this day
            if menu["btime"][0] <= comparetime <= menu["btime"][1]:
                menutype = "breakfast"
            elif menu["ltime"][0] <= comparetime <= menu["ltime"][1]:
                menutype = "lunch"
            elif menu["dtime"][0] <= comparetime <= menu["dtime"][1]:
                menutype = "dinner"
            else:
                menutype = "closed"
            #check the time, see what menu is open at the current hours
        else:
            menutype = "closed" 
        
        y = 0
        i = 0
        try:
            for x in menu[menutype]:
                if menutype == 'closed':
                    k = menu[menutype][0][0]
                    canvas.create_text(162, 130, anchor=NW, fill="white", text=k)
                    
                elif budget_range[0] <= menu[menutype][i][1] and menu[menutype][i][1] <= budget_range[1]:
                    z = menu[menutype][i][0]
                    r = menu[menutype][i][1]
                    canvas.create_text(162, 130+y, anchor=NW, fill="white", text=z)
                    canvas.create_text(458, 130+y, anchor=NW, fill="white", text=r)
                    y += 17
                    i += 1
                #based on budget range, display the relevant menu items
                #default budget range displayes everything
                else:
                    i += 1
                    #iterate to the next item if the current item is not to be displayed
        except:
            pass
        
        window.resizable(0, 0)
        
    def surprisebutton(self):
        self.set_current_time()
        window = tk.Toplevel(self)
        canlist = [can1, can2, can3, can4, can5, can6]
        openlist = []
        currenthour = int(sort_time[11:13] + sort_time[14:16])
                
        for x in canlist:
        #check what stores are open now, and add them to a new list
            if day_of_week in x["day"]:
                if x["time"][0] <= currenthour <= x["time"][1]:
                    openlist.append(x)
        
        z = 0
        # z is to check if any store open later on
        try:
        #randomly chooses 1 of the stores in the new list
            canteennumber = randint(1, len(openlist))
            canteen = openlist[canteennumber-1]
            z = 1
        except:
            z = 0

        if len(openlist) == 0:
        #if all stores are closed now, display this
            itemname = 'Apologies, nothing is open'
            itemcost = ''
        elif canteen != can6:
        #this is because can6 menu items vary by day, not time
            if canteen["btime"][0] <= currenthour <= canteen["btime"][1]:
                while True:
                    try:
                        item = canteen["breakfast"][randint(0,20)]
                        itemname = item[0]
                        itemcost = str(item[1])
                        break
                    except:
                        pass
            elif canteen["ltime"][0] <= currenthour <= canteen["ltime"][1]:
                while True:
                    try:
                        item = canteen["lunch"][randint(0,20)]
                        itemname = item[0]
                        itemcost = str(item[1])
                        break
                    except:
                        pass
            elif canteen["dtime"][0] <= currenthour <= canteen["dtime"][1]:
                while True:
                    try:
                        item = canteen["dinner"][randint(0,20)]
                        itemname = item[0]
                        itemcost = str(item[1])
                        break
                    except:
                        pass
            else:
                pass
        
        elif canteen == can6:
            if day_of_week == "Monday":
                while True:
                    try:
                        item = canteen["breakfast"][randint(0,20)]
                        itemname = item[0]
                        itemcost = str(item[1])
                        break
                    except:
                        pass
            elif day_of_week == "Wednesday":
                while True:
                    try:
                        item = canteen["dinner"][randint(0,20)]
                        itemname = item[0]
                        itemcost = str(item[1])
                        break
                    except:
                        pass
            else:
                while True:
                    try:
                        item = canteen["lunch"][randint(0,20)]
                        itemname = item[0]
                        itemcost = str(item[1])
                        break
                    except:
                        pass
        if z == 1:
            Label(window, \
                  width = 40, \
                  height = 6, \
                  bg = 'grey', \
                  fg = 'white', \
                  text= 'You can try out:\n' + canteen['name'] + ':\n' + itemname +'    $' + itemcost).grid(row=0, column=0)
        else:
            Label(window, \
                  width = 40, \
                  height = 6, \
                  bg = 'grey', \
                  fg = 'white', \
                  text= 'There are no stores open right now\nSorry, we got nothing to surprise you with').grid(row=0, column=0)
            
        window.resizable(0,0)
        
# CHENG YUN
class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        canvas = Canvas(self, width=640, height=720)
        image = ImageTk.PhotoImage(Image.open('frontpage.jpg'))
        self.image = image
        canvas.pack()
        canvas.create_image(0, 0, anchor=NW, image=image)
        #places image at 0,0. anchor is to represent left upper corner of image

        ctbutton = Button(self, \
                          width = 11, \
                          bg = 'white', \
                          fg = 'black', \
                          text="View stores based on current time", \
                          command=lambda: [controller.set_default_budget(), controller.show_frame(UserInputPrice), controller.set_current_time()], anchor = N)
        ctbutton.configure(width = 29)
        canvas.create_window(100, 420, anchor=NW, window=ctbutton)

        stbutton = Button(self, \
                          width = 11, \
                          bg = 'white', \
                          fg = 'black', \
                          text="View stores based on user input timing", \
                          command=lambda: [controller.set_default_budget(), controller.show_frame(UserInputTime)], anchor = N)
        stbutton.configure(width = 29)
        canvas.create_window(100, 470, anchor=NW, window=stbutton)
        
        bbutton = Button(self, \
                         width = 11, \
                         bg = 'light blue', \
                         fg = 'black', \
                         text="Surprise Me!", \
                         command=lambda: controller.surprisebutton(), anchor = N)
        bbutton.configure(width = 29)
        canvas.create_window(100, 520, anchor=NW, window=bbutton)

        ohbutton = Button(self, \
                         height = 8, \
                         width = 11, \
                         bg = 'white', \
                         fg = 'black', \
                         text="\n\n\nAll stores\nopening hours", \
                         command=lambda: controller.show_frame(Storeohs), anchor = N)
        ohbutton.configure(width = 29)
        canvas.create_window(375, 420, anchor=NW, window=ohbutton)   
        
        clocktime = Label(self, \
                          height = 4, \
                          width = 23, \
                          font=('times', 20, 'bold'), \
                          bg='grey')
        canvas.create_window(320, 239, anchor=N, window=clocktime)
        

        
        def tick():
        #function to check current time repeatedly. If new current time is not same as old one, update label to show the new current time
            s = time.strftime("%d/%m/%Y, %H:%M:%S")
            f = time.strftime("%A")
            a = s[0:10] + '\n' + s[11:20] + '\n' + f
            if a != clocktime["text"]:
                clocktime["text"] = a
            clocktime.after(200, tick)
        tick()

# IRVIN
class StoreList1(tk.Frame):
# View non-halal stores based on current operating hours
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        canvas = Canvas(self, width=640, height=720)
        image = ImageTk.PhotoImage(Image.open('storelist1.jpg'))
        self.image = image
        canvas.pack()
        canvas.create_image(0, 0, anchor=NW, image=image)
        #places image at 0,0. anchor is to represent left upper corner of image


        miniwokimage = ImageTk.PhotoImage(Image.open('miniwok.jpg')) 
        self.miniwokimage= miniwokimage
        miniwok_button = Button(self, \
                             image=miniwokimage, \
                             highlightthickness = 0, \
                             bd = 0, \
                             command=lambda: controller.create_menu(can1))
        canvas.create_window(166, 162, anchor=N, window=miniwok_button)
        
        malahotpotimage = ImageTk.PhotoImage(Image.open('malahotpot.jpg')) 
        self.malahotpotimage= malahotpotimage
        malahotpot_button = Button(self, \
                             image=malahotpotimage, \
                             highlightthickness = 0, \
                             bd = 0, \
                             command=lambda: controller.create_menu(can2))
        canvas.create_window(488, 162, anchor=N, window=malahotpot_button)
        
        macdonaldsimage = ImageTk.PhotoImage(Image.open('macdonalds.jpg')) 
        self.macdonaldsimage= macdonaldsimage
        macdonalds_button = Button(self, \
                             image=macdonaldsimage, \
                             highlightthickness = 0, \
                             bd = 0, \
                             command=lambda: controller.create_menu(can3))
        canvas.create_window(166, 352, anchor=N, window=macdonalds_button)

        subwayimage = ImageTk.PhotoImage(Image.open('subway.jpg')) 
        self.subwayimage= subwayimage
        subway_button = Button(self, \
                             image=subwayimage, \
                             highlightthickness = 0, \
                             bd = 0, \
                             command=lambda: controller.create_menu(can4))
        canvas.create_window(488, 352, anchor=N, window=subway_button)
        
        starbucksimage = ImageTk.PhotoImage(Image.open('starbucks.jpg')) 
        self.starbucksimage= starbucksimage
        starbucks_button = Button(self, \
                             image=starbucksimage, \
                             highlightthickness = 0, \
                             bd = 0, \
                             command=lambda: controller.create_menu(can5))
        canvas.create_window(166, 542, anchor=N, window=starbucks_button)
        
        vegetarianimage = ImageTk.PhotoImage(Image.open('vegetarian.jpg')) 
        self.vegetarianimage= vegetarianimage
        vegetarian_button = Button(self, \
                             image=vegetarianimage, \
                             highlightthickness = 0, \
                             bd = 0, \
                             command=lambda: controller.create_menu(can6))
        canvas.create_window(488, 542, anchor=N, window=vegetarian_button)

        backbutton = Button(self, \
                            width = 11, \
                            bg = 'grey', \
                            fg = 'black', \
                            text="Back to Home", \
                            command=lambda: controller.show_frame(StartPage))
        canvas.create_window(2, 696, anchor=NW, window=backbutton)
        #creating all the buttons

# CHENG YUN        
class UserInputTime(tk.Frame):
    #the page for users to input the time they want
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        canvas = Canvas(self, width=640, height=720)
        image = ImageTk.PhotoImage(Image.open('userinputtime.jpg'))
        self.image = image
        canvas.pack()
        canvas.create_image(0, 0, anchor=NW, image=image)
        #places image at 0,0. anchor is to represent left upper corner of image

        day = StringVar()
        dayentry = Entry(self, \
                         bg = 'grey', \
                         width = 9, \
                         justify = "center", \
                         textvariable=day)
        canvas.create_window(230, 198, anchor=N, window=dayentry)
    
        month = StringVar()
        monthentry = Entry(self, \
                           bg = 'grey', \
                           width = 9, \
                           justify = "center", \
                           textvariable=month)
        canvas.create_window(319, 198, anchor=N, window=monthentry)

        
        year = StringVar()
        yearentry = Entry(self, \
                          bg = 'grey', \
                          width = 9, \
                          justify = "center", \
                          textvariable=year)
        canvas.create_window(405, 198, anchor=N, window=yearentry)


        hours = StringVar()
        hoursentry = Entry(self, \
                           bg = 'grey', \
                           width = 9, \
                           justify = "center", \
                           textvariable=hours)
        canvas.create_window(267, 302, anchor=N, window=hoursentry)

        minutes = StringVar()
        minutesentry = Entry(self, \
                             bg = 'grey', \
                             width = 9, \
                             justify = "center", \
                             textvariable=minutes)
        canvas.create_window(367, 302, anchor=N, window=minutesentry)

        backbutton = Button(self, \
                            width = 11, \
                            bg = 'grey', \
                            fg = 'black', \
                            text="Back to Home", \
                            command=lambda: controller.show_frame(StartPage))
        canvas.create_window(2, 696, anchor=NW, window=backbutton)
        
        gobutton = Button(self, \
                          width = 11, \
                          bg = 'grey', \
                          fg = 'black', \
                          text="GO", \
                          command=lambda: controller.user_input_time_button(day, month, year, hours, minutes))
        canvas.create_window(320, 360, anchor=N, window=gobutton)

# IRVIN            
class StoreList2(tk.Frame):
# View halal stores based on current operating hours    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        canvas = Canvas(self, width=640, height=720)
        image = ImageTk.PhotoImage(Image.open('storelist2.jpg'))
        self.image = image
        canvas.pack()
        canvas.create_image(0, 0, anchor=NW, image=image)
        #places image at 0,0. anchor is to represent left upper corner of image


        macdonaldsimage = ImageTk.PhotoImage(Image.open('macdonalds.jpg')) 
        self.macdonaldsimage= macdonaldsimage
        macdonalds_button = Button(self, \
                             image=macdonaldsimage, \
                             highlightthickness = 0, \
                             bd = 0, \
                             command=lambda: controller.create_menu(can3))
        canvas.create_window(166, 162, anchor=N, window=macdonalds_button)

        subwayimage = ImageTk.PhotoImage(Image.open('subway.jpg')) 
        self.subwayimage= subwayimage
        subway_button = Button(self, \
                             image=subwayimage, \
                             highlightthickness = 0, \
                             bd = 0, \
                             command=lambda: controller.create_menu(can4))
        canvas.create_window(488, 162, anchor=N, window=subway_button)
        
        starbucksimage = ImageTk.PhotoImage(Image.open('starbucks.jpg')) 
        self.starbucksimage= starbucksimage
        starbucks_button = Button(self, \
                             image=starbucksimage, \
                             highlightthickness = 0, \
                             bd = 0, \
                             command=lambda: controller.create_menu(can5))
        canvas.create_window(166, 352, anchor=N, window=starbucks_button)
        
        vegetarianimage = ImageTk.PhotoImage(Image.open('vegetarian.jpg')) 
        self.vegetarianimage= vegetarianimage
        vegetarian_button = Button(self, \
                             image=vegetarianimage, \
                             highlightthickness = 0, \
                             bd = 0, \
                             command=lambda: controller.create_menu(can6))
        canvas.create_window(488, 352, anchor=N, window=vegetarian_button)

        backbutton = Button(self, \
                            width = 11, \
                            bg = 'grey', \
                            fg = 'black', \
                            text="Back to Home", \
                            command=lambda: controller.show_frame(StartPage))
        canvas.create_window(2, 696, anchor=NW, window=backbutton)
        #create the relevant buttons

# BOON JUEY        
class UserInputPrice(tk.Frame):
# Brings up the page for users to choose their budget range, and halal or not 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        canvas = Canvas(self, width=640, height=720)
        image = ImageTk.PhotoImage(Image.open('userinputprice.jpg'))
        self.image = image
        canvas.pack()
        canvas.create_image(0, 0, anchor=NW, image=image)      

        backbutton = Button(self, \
                            width = 11, \
                            bg = 'grey', \
                            fg = 'black', \
                            text="Back to Home", \
                            command=lambda: controller.show_frame(StartPage), anchor = W)
        backbutton.configure(width = 11, activebackground = "grey")
        canvas.create_window(2, 696, anchor=NW, window=backbutton)
        
        lowerlimit = StringVar()
        lowerentry = Entry(self, \
                           width = 31, \
                           bg = 'grey', \
                           justify = "center", \
                           textvariable=lowerlimit)
        lowerentry.insert(END, '0')
        canvas.create_window(57, 223, anchor=NW, window=lowerentry)
        
        higherlimit = StringVar()
        higherentry = Entry(self, \
                            width = 31, \
                            bg = 'grey', \
                            justify = "center", \
                            textvariable=higherlimit)
        higherentry.insert(END, '1000')
        canvas.create_window(404, 223, anchor=NW, window=higherentry)
        
        halalimage = ImageTk.PhotoImage(Image.open('halalplease.jpg')) 
        self.halalimage = halalimage
        halalbutton = Button(self, \
                             image=halalimage, \
                             highlightthickness = 0, \
                             bd = 0, \
                             command=lambda: [controller.set_halal_true(), controller.user_input_price_button(lowerlimit, higherlimit)], anchor = W)
        canvas.create_window(130, 488, anchor=NW, window=halalbutton)

        nothalalimage = ImageTk.PhotoImage(Image.open('anythingisfine.jpg')) 
        self.nothalalimage = nothalalimage
        nothalalbutton = Button(self, \
                                image=nothalalimage, \
                                highlightthickness = 0, \
                                bd = 0, \
                                command=lambda: [controller.set_halal_false(), controller.user_input_price_button(lowerlimit, higherlimit)], anchor = W)
        canvas.create_window(365, 495, anchor=NW, window=nothalalbutton)
        
# BOON JUEY      
class Storeohs(tk.Frame):
    #displays an image of the operating hours for all stores
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        canvas = Canvas(self, width=640, height=720)        
        image = ImageTk.PhotoImage(Image.open('storeoh.jpg'))
        self.image=image
        canvas.pack()
        canvas.create_image(0, 0, anchor=NW, image=image) 

        
        backbutton = Button(self, \
                            width = 11, \
                            bg = 'grey', \
                            fg = 'black', \
                            text="Back to Home", \
                            command=lambda: controller.show_frame(StartPage), anchor = W)
        backbutton.configure(width = 11, activebackground = "grey")
        canvas.create_window(2, 696, anchor=NW, window=backbutton)


app = nscanteenapp()


def exit(event):
    app.destroy()
#command to close program

app.bind("<Escape>", exit)
#close the program upon pressing the "Escape" button on keyboard
app.resizable(0,0)
#avoid letting the menu be resized


app.mainloop()
