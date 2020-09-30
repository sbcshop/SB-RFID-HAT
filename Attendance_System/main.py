#! /usr/bin/python3

'''
This file contains GUI code for RFID HAT based attendence system.
'''

import shutil
import logging
import threading
import webbrowser
import tkinter as tk
from tkinter import font
from tkinter import messagebox
from tkinter import *
import tkinter.simpledialog
from os import path, system
from serial.tools import list_ports
import time
from PIL import ImageTk ,Image
import queue
import SerialPort
import ExcelCSV
import sys
##########################  MainApp  ###########################################

class MainApp(tk.Tk):
    '''
    This is a class for Creating Frames and Buttons for left and top frame
    '''

    def __init__(self, *args, **kwargs):
        global logo, img
    
        tk.Tk.__init__(self, *args, **kwargs)

        self.screen_width=tk.Tk.winfo_screenwidth(self)
        self.screen_height=tk.Tk.winfo_screenheight(self)
        self.app_width=800
        self.app_height= 480
        self.xpos = (self.screen_width/2)-(self.app_width/2)
        self.ypos = (self.screen_height/2)-(self.app_height/2)
        self.port = None
        
        self.geometry("%dx%d+%d+%d" %(self.app_width,self.app_height,self.xpos,
                                      self.ypos))
        self.title(" RFID Attendence System")
        if not self.screen_width > self.app_width:
            self.attributes('-fullscreen', True)
            
        self.config(bg="gray85")
        self.leftframe_contents(self)
        self.topframe_contents(self)
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, AdminPage, AddPage, DeletePage, ShowRecordPage, passwordPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame("HomePage")

        self.queue = queue.Queue()
        self.serial_thread = threading.Thread(target=SerialPort.SerialThread, args=(self.queue,))
        self.serial_thread.start()
        self.periodicCall()

    def periodicCall(self):
        """
        Check every 200 ms if there is something new in the queue.
        """
        self.processIncoming(  )
        self.after(200, self.periodicCall)

    def processIncoming(self):
        """Handle all messages currently in the queue, if any."""
        while self.queue.qsize(  ):
            try:
                msg = self.queue.get(0)
                if len(msg) == 12 :
                    #cardId = msg.decode("utf-8")
                    cardId = msg
                    if self.currentPage == 'AddPage':
                        row = self.checkRecord(cardId)
                        if row == '':
                            self.frames['AddPage'].IDText.set(cardId)
                        else:
                            self.popupmsg("Card ID is Already added as "+row[1])
                            self.frames['AddPage'].IDText.set('')
                    elif self.currentPage == 'DeletePage':
                            pass
                    else:  #self.currentPage == 'HomePage' or other page
                        row = self.checkRecord(cardId)
                        if row != '':
                            data = []
                            data.insert(3,row[0])
                            data.insert(0,row[1])

                            timeNow = time.strftime('%H:%M:%S')
                            dateNow = time.strftime('%d/%m/%Y  ')
                            data.insert(1,dateNow+timeNow)
        
                            ExcelCSV.CSVFile.Write('record.csv',data)
                            self.popupmsg("welcome " + row[1])
                        else:
                            self.popupmsg("Card ID is not in record")

                        

            except Queue.Empty:
                pass
    def checkRecord(self,cardId):
        try:
            rows = ExcelCSV.CSVFile.Read('database.csv')
            for row in rows:
                if row[0] == cardId:
                    return row
            return ''
        except:
            return ''
            pass
    
    def topframe_contents(self,selfp):

        self.Topframe = tk.Frame(selfp)
        self.Topframe.pack(side='top', fill = 'x', anchor = 's')
        for i in range(0,2):
            self.Topframe.grid_columnconfigure(i, weight = 1)

        self.dateLabel = tk.Text(self.Topframe, fg = "yellow" ,height = 1,bg="grey",
                                 width = 28, bd  = 0, highlightthickness = 1,font=16)
        self.dateLabel.grid(row = 0, column = 2, sticky=NSEW)

        self.link1 = Label(self.Topframe, text="Shop", fg="blue", cursor="hand2",borderwidth=2, relief="groove")
        self.link1.grid(row = 0, column = 0, sticky=NSEW)
        self.link1.bind("<Button-1>", lambda e: self.callback("https://shop.sb-components.co.uk/"))

        self.link2 = Label(self.Topframe, text="How To Use", fg="blue", cursor="hand2",borderwidth=2, relief="groove")
        self.link2.grid(row = 0, column = 1, sticky=NSEW)
        self.link2.bind("<Button-1>", lambda e: self.callback("https://www.youtube.com/watch?v=0jq11UZN-bg&t=4s"))
        self.update_Clock()

    def update_Clock(self):
        '''Updates the clock per second ''' 
        timeNow = time.strftime('%H:%M:%S')
        dateNow = time.strftime('%A - %d/%m/%Y  ')
        self.dateLabel.delete(1.0, "end")
        self.dateLabel.insert(1.0, dateNow+timeNow)
        self.after(1000, self.update_Clock)
    
    def callback(self,url):
        webbrowser.open_new(url)

    def leftframe_contents(self, selfp):
        '''
        This function creates the left frame widgets
        '''
        
        self.Leftframe = tk.Frame(selfp, bg = "gray80",height = 300)
        self.Leftframe.pack(side='left', fill = 'both',expand = 'false')

        for i in range(0,3):
            self.Leftframe.grid_rowconfigure(i, weight = 1)

        self.img1 = ImageTk.PhotoImage(file="/home/pi/SB-RFID-HAT/Attendance_System/Images/admin_button.png")
        self.img2 = ImageTk.PhotoImage(file="/home/pi/SB-RFID-HAT/Attendance_System/Images/back_button.png")
        self.img3 = ImageTk.PhotoImage(file="/home/pi/SB-RFID-HAT/Attendance_System/Images/exit_button.png")

        
        #self.AdminButton=Button(self.Leftframe, text="Admin", image=self.img1, bd=0,
                                #command = lambda:self.show_frame("AdminPage"))
        #self.AdminButton.grid(row=1, column=0,sticky=NSEW)

        self.AdminButton=Button(self.Leftframe, text="Admin", image=self.img1, bd=0,activebackground="gray85",
                                command = lambda:self.show_frame("passwordPage"))
        self.AdminButton.grid(row=1, column=0,sticky=NSEW)

        self.BackButton=Button(self.Leftframe, text="back", image=self.img2, bd=0,activebackground="gray85",
                               command = self.BackButtonCommandFunction)
        self.BackButton.grid(row=2, column=0,sticky=NSEW)#sticky=NSEW, columnspan =4,ipadx=10,ipady=10)

        self.ExitButton=Button(self.Leftframe, text="Exit", image=self.img3, bd=0, activebackground="gray85",
                               command = self.Exit)
        self.ExitButton.grid(row=3, column=0,sticky=NSEW)#,sticky=NSEW, columnspan =4,ipadx=10,ipady=10)

        self.img=ImageTk.PhotoImage(Image.open ("/home/pi/SB-RFID-HAT/Attendance_System/RFID_GUI/Images/logo.png"))
        self.lab=Label(self.Leftframe,image=self.img)
        self.lab.grid(row=0, column=0,sticky=NSEW)#,sticky=NSEW, columnspan =4)

    def Exit(self):
        self.destroy()
    

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        self.currentPage = page_name
        if page_name  == "AdminPage" :
            self.BackPageFramePoints = 'HomePage'
        elif page_name  == "AddPage" :
            self.BackPageFramePoints = 'AdminPage'
        elif page_name  == "DeletePage" :
            self.BackPageFramePoints = 'AdminPage'
            frame.event_generate("<<ShowFrame>>")            
        elif page_name  == "HomePage" :
            self.BackPageFramePoints = 'HomePage'
        elif page_name == "ShowRecordPage":
            self.BackPageFramePoints = 'AdminPage'
            frame.event_generate("<<ShowFrame>>")
        elif page_name == "passwordPage":
            self.BackPageFramePoints = 'HomePage'
            frame.event_generate("<<ShowFrame>>") 
        else:
            self.BackPageFramePoints = 'HomePage'

        frame.tkraise()

    def BackButtonCommandFunction(self):
        self.show_frame(self.BackPageFramePoints)
        
    def popupmsg(self,msg):
        popup = tk.Tk()

        self.app_width=200
        self.app_height= 100
        self.xpos = (self.screen_width/2)-(self.app_width/2)
        self.ypos = (self.screen_height/2)-(self.app_height/2)
        self.port = None
        popup.geometry("%dx%d+%d+%d" %(self.app_width,self.app_height,self.xpos,
                                      self.ypos))
        popup.wm_title("!")
        label = Label(popup, text=msg)
        label.pack(side="top", fill="x", pady=10)
        B1 = Button(popup, text="Okay", command = popup.destroy)
        B1.pack()
        #popup.mainloop()

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        '''
        This function creates the right frame widgets
        '''
        tk.Frame.__init__(self, parent)
        self.controller = controller


        self.labelPutcard = Label(self, text="Put Your RFID Card", fg="blue", cursor="hand2",height=5,font=20)
        self.labelPutcard.pack(side=BOTTOM, fill=Y)

        self.imgRF=ImageTk.PhotoImage(Image.open ("/home/pi/SB-RFID-HAT/Attendance_System/Images/RFID.gif"))
        self.lab1=Label(self,image=self.imgRF,width = 600,height=400)
        #self.lab1.pack(side=RIGHT, fill='both')
        self.lab1.pack()
        
        '''self.dateLabel = tk.Text(self,height = 1,
                                 width = 27, bd  = 0, highlightthickness = 1,font=16)
        self.dateLabel.place(x=370, y=5)

        self.update_Clock() '''

    #def update_Clock(self):
        '''Updates the clock per second ''' 
        '''timeNow = time.strftime('%H:%M:%S')
        dateNow = time.strftime('%A - %d/%m/%Y  ')
        self.dateLabel.delete(1.0, "end")
        self.dateLabel.insert(1.0, dateNow+timeNow)
        self.after(1000, self.update_Clock)'''


class passwordPage(tk.Frame):
    def __init__(self, parent, controller):
        '''
        This function creates the right frame widgets
        '''
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(1, weight = 1)  
        for i in range(4):
            self.grid_rowconfigure(i, weight = 1)  
            self.grid_columnconfigure(i, weight = 1)


        self.labeltxt = Label(self, text="Enter Password :", fg="blue", height=5,font=("Courier", 23))
        self.labeltxt.grid(row=2, column=0, sticky=NSEW, columnspan =1,ipadx=2,ipady=2)

        self.password = StringVar() #Password variable
        passEntry = Entry(self, textvariable=self.password, show='*', width=18, font=("Calibri",20))
        passEntry.insert(0, '123456')
        passEntry.grid(row=2, column=1, columnspan =1,ipadx=2,ipady=2)

        submit = Button(self, text='Login', command=self.validate_pass, font=("Courier",20))
        submit.place(x=510, y=220)

        self.labelpasserror = Label(self, text=" ", fg="red", cursor="hand2",height=5,font=20)
        self.labelpasserror.grid(row=3, column=0,sticky=NSEW, columnspan =4,ipadx=10,ipady=10)

    def validate_pass(self):
        self.p = self.password.get() #get password from entry
        if(self.p == "123456"):
            self.controller.show_frame("AdminPage")
        else:
            self.labelpasserror.config(text="Invalid Password, Try again !")
    

class AdminPage(tk.Frame):
    def __init__(self, parent, controller):
        '''
        This function creates the right frame widgets
        '''
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(1, weight = 1)  
        for i in range(4):
            self.grid_rowconfigure(i, weight = 1)  
            self.grid_columnconfigure(i, weight = 1)  
        
        self.AddButton=Button(self, text="Add", fg="white", command = lambda:
                              controller.show_frame("AddPage"), bg = "blue", font=("Courier",18),
                              relief="raised", borderwidth=3)
        self.AddButton.grid(row=1, column=1,sticky=NSEW, columnspan =1,ipadx=20,ipady=20,
                            padx=10, pady=10)

        self.Delete=Button(self, text="Delete", fg="white", command = lambda:
                              controller.show_frame("DeletePage"), bg = "blue", font=("Courier",18),
                           relief="raised", borderwidth=3)
        self.Delete.grid(row=1, column=2,sticky=NSEW, columnspan =1,ipadx=20,ipady=20,
                         padx=10, pady=10)

        self.showRecord=Button(self, text="Show Records", fg="white", command = lambda:
                              controller.show_frame("ShowRecordPage"),bg = "blue", font=("Courier",18),
                               relief="raised", borderwidth=3)
        self.showRecord.grid(row=2, column=1,sticky=NSEW, columnspan =2,ipadx=20,ipady=20,
                             padx=10, pady=10)
        
        self.labelPutcard = Label(self, text="Press Add to add a new member\n Press Delete to remove an existing member\n Press Show Records to see logs", fg="blue", cursor="hand2",height=5,font=20)
        self.labelPutcard.grid(row=3, column=0,sticky=NSEW, columnspan =4,ipadx=10,ipady=10)

class AddPage(tk.Frame):
    def __init__(self, parent, controller):
        '''
        This function creates the right frame widgets
        '''
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(1, weight = 1)  
        for i in range(5):
            self.grid_rowconfigure(i, weight = 1)  
            self.grid_columnconfigure(i, weight = 1)  

        self.IDLabel = Label(self, text="Card ID") 
        self.IDLabel.grid(row=1,column=1,sticky =E) 
        self.UserNameLabel = Label(self, text="Member Name") 
        self.UserNameLabel.grid(row=2,column=1,sticky =E) 
  
        self.IDText = StringVar()
        self.UserNameText = StringVar() 
    
        self.IDEntry = Entry(self,textvariable=self.IDText, state=DISABLED).grid(row=1, column=2,sticky=W, padx=10, pady=10) 
        self.UserNameEntry = Entry(self, textvariable=self.UserNameText).grid(row=2,column=2,sticky=W, columnspan =1, padx=10,pady=10) 

        self.SubmitButton=Button(self, text="submit", command = self.add_new_card)
        self.SubmitButton.grid(row=3, column=2, columnspan =1, sticky = NSEW, ipadx=10,ipady=10)

        self.labelAddCard = Label(self, text="1. Place a New Card \n2. Enter Name of new member\n2. Press Submit", fg="blue", cursor="hand2",height=5,font=20)
        self.labelAddCard.grid(row=4, column=0,sticky=NSEW, columnspan =4,ipadx=10,ipady=10)

    def add_new_card(self):
        data = []
        data.insert(0,self.IDText.get())
        data.insert(1,self.UserNameText.get())

        timeNow = time.strftime('%H:%M:%S')
        dateNow = time.strftime('%d/%m/%Y  ')
        data.insert(2,dateNow+timeNow)
        
        ExcelCSV.CSVFile.Write('database.csv',data)

        self.IDText.set('')
        self.UserNameText.set('')
        self.controller.popupmsg('Member Added')

class DeletePage(tk.Frame):
    def __init__(self, parent, controller):
        '''
        This function creates the right frame widgets
        '''
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bind("<<ShowFrame>>", self.on_show_frame)
        
        self.grid_columnconfigure(1, weight = 1)  
        for i in range(5):
            self.grid_rowconfigure(i, weight = 1)  
            self.grid_columnconfigure(i, weight = 1)  

        self.UserNameLabel = Label(self, text="Member Name") 
        self.UserNameLabel.grid(row=0,column=2,sticky = S, padx=10, pady=0) 
  
        self.UserNameText = StringVar() 
        self.UserNameText.trace('w', self.on_change)

        self.UserNameEntry = Entry(self, textvariable=self.UserNameText).grid(row=1,column=2,sticky=S, columnspan =1, padx=0,pady=0) 

        self.UserNamelistbox = Listbox(self)
        self.UserNamelistbox.grid(row=2, column=2, columnspan =1, sticky=N, padx=0,pady=0)
        #listbox.bind('<Double-Button-1>', on_select)
        self.UserNamelistbox.bind('<<ListboxSelect>>', self.on_select)
        self.UserNamelistbox.bind('<Return>', self.on_select)

        self.SubmitButton=Button(self, text="Delete", command = self.Delete_card)
        self.SubmitButton.grid(row=3, column=2, columnspan =1,sticky = NSEW, ipadx=10,ipady=10)

        self.labelAddCard = Label(self, text="1. Write or select a member name\n2. Press Delete", fg="blue", cursor="hand2",height=5,font=20)
        self.labelAddCard.grid(row=4, column=0,sticky=NSEW, columnspan =4,ipadx=10,ipady=10)

    def on_show_frame(self, event=''):
        rows = ExcelCSV.CSVFile.Read('database.csv')
        userNameList = []
        for row in rows:
            userNameList.append(row[1])
        self.listbox_update(userNameList)

    def Delete_card(self):
        try:
            userNameText = self.UserNameText.get()
            rows = ExcelCSV.CSVFile.Read('database.csv')
            rowsNew = []
            for row in rows:
                if row[1] != userNameText:
                    rowsNew.append(row)
            ExcelCSV.CSVFile.remove('database.csv')
            for row in rowsNew:
                ExcelCSV.CSVFile.Write('database.csv', row)
        
            self.on_show_frame()
            self.UserNameText.set('')
            self.controller.popupmsg('Member Deleted')
        except:
            pass

    def on_select(self,event):
        # display element selected on list
        text = event.widget.get(event.widget.curselection())
        if text != '':
            self.UserNameText.set(text)

    def on_change(self,*args):
        rows = ExcelCSV.CSVFile.Read('database.csv')
        userNameList = []
        for row in rows:
            userNameList.append(row[1])
        value = self.UserNameText.get()
        value = value.strip().lower()

        # get data from test_list
        if value == '':
            data = userNameList
        else:
            data = []
            i=0
            for item in userNameList:
                if value in item.lower():
                    data.append(item)
                i=i+1

        # update data in listbox
        self.listbox_update(data,)

    def listbox_update(self,data):
        # delete previous data
        self.UserNamelistbox.delete(0, 'end')
        # sorting data 
        data = sorted(data, key=str.lower)

        # put new data
        for item in data:
            self.UserNamelistbox.insert('end', item)


class ShowRecordPage(tk.Frame):
    def __init__(self, parent, controller):
        '''
        This function creates the right frame widgets
        '''
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bind("<<ShowFrame>>", self.on_show_frame)
        
    def on_show_frame(self, event=''):
        try:
            rows = ExcelCSV.CSVFile.Read('record.csv')
            total_column = 3
            rowCount = 0
            for row in rows:
                for j in range(total_column): 
                  
                    self.e = Entry(self ,fg = "black" ,bg="white",
                                 width = 25, bd  = 0, highlightthickness = 1,font=16) 
                  
                    self.e.grid(row=rowCount, column=j,sticky = NSEW) 
                    self.e.insert(END, rows[rowCount][j])
            
                rowCount = rowCount + 1
        except:
            pass
    

#######################################################################################################################
logo = None
img = None
Root_Dir = path.dirname(path.realpath(__file__))
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

if __name__ == "__main__":
    app = MainApp()
#    app.tk.call('wm', 'iconphoto', app._w, img)
    app.resizable(0,0)
    app.mainloop()
