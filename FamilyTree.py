# -*- coding: UTF-8 -*-
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import datetime
from tkcalendar import Calendar, DateEntry
import easygui as eg
from PIL import Image, ImageTk




root = Tk()
root.geometry('940x700')
root.title('Family Tree')
root.bg='#0B5A81'
root.config(bg='#0B5A81')



try:
    con = sqlite3.connect("FamilyTree.db")
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS tree(
               id text , name text , prt_id text  , address text ,
               telephone text , gender text , job text , prt_name text ,
               birthday text , cup_name text , cup_add text , cup_telephone text , image blob , deathday text) ''')
    con.commit()
except Exception as ex :
       messagebox.showerror('SQL Eroor' , ex)

 
var = StringVar()
cup_name = StringVar()
cup_add = StringVar()
cup_tel = StringVar()
brd = StringVar()
ded = StringVar()
img_path = StringVar()
name = StringVar()
add = StringVar()
prt = StringVar()



insert_sql = '''insert into tree (id  , name  , prt_id   , address  ,
               telephone  , gender  , job  , prt_name  ,
               birthday  ,
               cup_name  , cup_add  , cup_telephone ,image , deathday) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
               
              
select_sql = '''select * from tree where id = ? ;'''
               
               
def populate_tree() :
    select_sql = '''select * from tree'''
    cur.execute(select_sql)
    tv_list = cur.fetchall()
    for row in tv_list :
        tv.insert(row[2] , value = row[1] , index = 10 , text = row[1] , iid = row[0])
        
        
def clear_widg() :
    name_ent.delete( first=0, last=END )
    add_ent.delete( 0, END )
    tel_ent.delete( 0, last=END )
    var.set('')
    job_ent.delete(0, END )
    prt_ent.delete( first=0, last=END )
    brd_ent.delete( 0, last=END )
    ded_ent.delete( 0, last=END )
    cup_name.set('')
    cup_add.set('')
    cup_tel.set('')
    
    
def selected(event) :
    for item in tv.selection() :
         item_id = str(tv.focus())
         #messagebox.showinfo('item_id' ,  item_id)
         cur.execute(select_sql , (item_id,))
         item_values = cur.fetchall()
         for row in item_values :
             name.set(row[1])
             add.set(row[3])
             prt.set(row[7])
             cup_name.set(row[9])
             cup_add.set(row[10])
             cup_tel.set(row[11])
             img_obj_lb.configure(row[12])
             img_obj_lb.image = row[12]
    
    
def get_date():
    my_date = StringVar()
    def cal_done():
        #top.withdraw()
        top.quit()
        #top.destroy()
        #new_root.quit()
        
    #new_root = tk.Tk()
    #new_root.withdraw() # keep the root window from appearing

    top = tk.Tk() #Toplevel(new_root)
    top.title("Calendar")

    cal = Calendar(top,font = "Arial 14" , selectmode = 'day' , cursor = "hand1" , textvariable = my_date)
    cal.pack(fill = "both", expand = True)
    ttk.Button(top, text="ok", command = cal_done).pack() #grid(row = 0 , column =0)
    ttk.Button(top, text="exit", command = top.destroy).pack() #grid(row = 0 , column =1)

    selected_date = None
    top.mainloop() #new_root.mainloop()
    return cal.selection_get()

def set_brd() :
    brd.set(get_date())
    
    
def set_ded() :
    ded.set(get_date())
    
    
    
def get_img() :
    path = eg.fileopenbox()
    img_path.set(path)
    img = Image.open(path)
    img = img.resize((200,200) , Image.ANTIALIAS)
    img_opj = ImageTk.PhotoImage(img)
    img_obj_lb.configure(image = img_opj)
    img_obj_lb.image = img_opj
    return img_opj

def add_root() :
    ok = verify_data() 
    if ok == 1 :
       messagebox.showinfo('' , 'Complete Data')
       return
    item_id = tv.insert('' , value = name_ent.get() , index = 10 , text = name_ent.get())
    #messagebox.showinfo('New ID' , item_id)
    try :
         '''insert into tree (id  , name  , prt_id   , address  ,
               telephone  , gender  , job  , prt_name  ,
               birthday  ,
               cup_name  , cup_add  , cup_telephone ,image , deathday) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
               
         cur.execute(insert_sql , (str(item_id) , name_ent.get() , '' , add_ent.get() ,
                   tel_ent.get() , var.get() , job_ent.get() , prt_ent.get() ,
                   brd_ent.get() , cup_name.get() , cup_add.get(), 
                   cup_tel.get() , get_img() , ded.get()))
         con.commit()
         messagebox.showinfo('confirmation', 'Record Saved')
         clear_widg()
    except Exception as ex :
          messagebox.showerror('SQL Eroor' , ex)
def add_branch() :
    ok = verify_data() 
    if ok == 1 :
       messagebox.showinfo('' , 'Complete Data')
       return
    prt_id = str(tv.focus())
    item_id = tv.insert(prt_id , value = name_ent.get() , index = 10 , text = name_ent.get())
    try :
         cur.execute(insert_sql , (item_id , name_ent.get() , prt_id , add_ent.get() ,
                  tel_ent.get() , var.get() , job_ent.get() , prt_ent.get() ,
                   brd_ent.get() , 
                   cup_name.get() , cup_add_ent.get() , cup_tel_ent.get() , get_img() , ded.get() ))
         con.commit()
         messagebox.showinfo('confirmation', 'Record Saved')
         clear_widg()
    except Exception as ex :
          messagebox.showerror('SQL Eroor' , ex)
          

 
def verify_data():
     if name_ent.get() == '' :
         messagebox.showerror('' , 'Complete Data')
         return 1
     elif add_ent.get() == '' :
          messagebox.showerror('' , 'Address can not be empty')
          return 1
     if cup_name_ent.get() == '' :
         messagebox.showerror('' , 'couple name can not be empty')
         return 1
     elif cup_add_ent.get() == '' :
          messagebox.showerror('' , 'couple address can not be empty')
          return 1
     elif var.get() == '' :
          messagebox.showerror('' , 'Please select gender')
          return 1
     else :
           return 0
    

    
tv_frame = Frame(root , bd = 2 , bg = '#CCCCCC' , relief = SOLID , height = 28 , width = 200 , padx = 2 , pady = 2)
tv = ttk.Treeview(tv_frame , height = 28)
tv.heading('#0' , text = 'Tree')


comm_frame = Frame(root , bd = 2 , bg = '#CCCCCC' , relief = SOLID , padx = 2 , pady = 2)
rot_btn = Button(comm_frame , text = 'Add Root' , command = add_root)
brn_btn = Button(comm_frame , text = 'Add Branch' , command = add_branch)



det_frame = Frame(root , bd = 2 , bg = '#CCCCCC' , relief = SOLID , padx = 2 , pady = 2)
per_frame = LabelFrame(det_frame , bd = 2 , bg = '#CCCCCC'  , padx = 2 , pady = 2 , text = 'Personal')
cup_frame = LabelFrame(det_frame , bd = 2 , bg = '#CCCCCC'  , padx = 2 , pady = 2 , text = 'Couple')
#cal = Calendar(det_frame,font = "Arial 14" , selectmode = 'day' , cursor = "hand1")
#Name
name_lb = Label(per_frame , text =  'Name' , bg = '#CCCCCC')
name_ent = Entry(per_frame , textvariable = name )
#Address
add_lb = Label(per_frame , text =  'Address' , bg = '#CCCCCC')
add_ent = Entry(per_frame , textvariable = add)
#Parent
prt_lb = Label(per_frame , text = 'Parent Name', bg = '#CCCCCC')
prt_ent = Entry(per_frame , textvariable = prt)
#Gender
gen_frame = LabelFrame(per_frame , text = 'Gender' , bg = '#CCCCCC' , padx = 2 , pady = 2)
male_rb = Radiobutton(gen_frame , text = 'Male' , value = 'male' , bg = '#CCCCCC' , variable = var )
feml_rb = Radiobutton(gen_frame , text = 'Female' , value = 'female' , variable = var, bg = '#CCCCCC')
#Telephone
tel_lb = Label(per_frame , text =  'Telephone' , bg = '#CCCCCC')
tel_ent = Entry(per_frame )
#Job
job_lb = Label(per_frame , text =  'Job' , bg = '#CCCCCC')
job_ent = Entry(per_frame )
#Birth Day
brd_lb = Label(per_frame , text =  'Birth Day' , bg = '#CCCCCC')
brd_ent = Entry(per_frame  , textvariable = brd)
brd_btn = Button(per_frame , text = 'Birth Date' , command = set_brd)
#Death Day
ded_lb = Label(per_frame , text =  'Death Day' , bg = '#CCCCCC')
ded_ent = Entry(per_frame , textvariable = ded )
ded_btn = Button(per_frame , text = 'Death Date' , command = set_ded)
#image
img_btn = Button(per_frame , text = 'Select Image' , command = get_img)
img_pt_lb = Label(per_frame , text =  '' , bg = '#CCCCCC' , textvariable = img_path)
img_obj_lb = Label(det_frame)
#couple Name
cup_name_lb = Label(cup_frame , text = 'Couple Name', bg = '#CCCCCC')
cup_name_ent = Entry(cup_frame , textvariable = cup_name)
#Couple Address
cup_add_lb = Label(cup_frame , text = 'Couple Address', bg = '#CCCCCC')
cup_add_ent = Entry(cup_frame , textvariable = cup_add)
#Couple Telephone
cup_tel_lb = Label(cup_frame , text = 'Couple Telephone', bg = '#CCCCCC')
cup_tel_ent = Entry(cup_frame , textvariable = cup_tel)


tv_frame.place(x = 50 , y = 55  )
tv.grid(row = 0 , column = 0 , padx = 10 , pady = 10)


comm_frame.place(x = 300 , y = 5)
rot_btn.grid(row = 0 , column = 0 , padx = 2 , pady = 2)
brn_btn.grid(row = 0 , column = 1 , padx = 2 , pady = 2)


det_frame.place(x = 300 , y = 55)
per_frame.grid(row = 0 , column = 0 , padx = 2 , pady = 2)
cup_frame.grid(row = 1 , column = 0 , padx = 2 , pady = 2)
img_obj_lb.grid(row = 2 , column = 0 , padx = 2 , pady = 2)
#cal.grid(row = 2 , column = 0 , padx = 2 , pady = 2)
name_lb.grid(row = 0  , column = 0 , padx = 2 , pady = 2)
name_ent.grid(row = 0 , column = 1 , padx = 2 , pady = 2)
prt_lb.grid(row = 0 , column = 3 , padx = 2 , pady = 2)
prt_ent.grid(row = 0 , column = 4 , padx = 2 , pady = 2)
gen_frame.grid(row = 1 , column = 0 , padx = 2 , pady = 2)
add_lb.grid(row = 1 , column = 3 , padx = 2 , pady = 2)
add_ent.grid(row = 1 , column = 4 , padx = 2 , pady = 2)
male_rb.pack(expand = True , side = LEFT)
feml_rb.pack(expand = True , side = LEFT)
tel_lb.grid(row = 2 , column = 0 , padx = 2 , pady = 2)
tel_ent.grid(row = 2 , column = 1 , padx = 2 , pady = 2)
job_lb.grid(row = 2 , column = 3 , padx = 2 , pady = 2)
job_ent.grid(row = 2 , column = 4 , padx = 2 , pady = 2)
brd_lb.grid(row = 3 , column = 0 , padx = 2 , pady = 2)
brd_btn.grid(row = 3 , column = 0 , padx = 2 , pady = 2)
brd_ent.grid(row = 3 , column = 1 , padx = 2 , pady = 2)
ded_lb.grid(row = 3 , column = 3 , padx = 2 , pady = 2)
ded_btn.grid(row = 3 , column = 3 , padx = 2 , pady = 2)
ded_ent.grid(row = 3 , column = 4 , padx = 2 , pady = 2)
img_btn.grid(row = 4 , column = 0 , padx = 2 , pady = 2)
img_pt_lb.grid(row = 4 , column = 1 , padx = 2 , pady = 2)
cup_name_lb.grid(row = 0 , column = 0 , padx = 2 , pady = 2)
cup_name_ent.grid(row = 0 , column = 1 , padx = 2 , pady = 2)
cup_add_lb.grid(row = 1 , column = 0 , padx = 2 , pady = 2)
cup_add_ent.grid(row = 1 , column = 1 , padx = 2 , pady = 2)
cup_tel_lb.grid(row = 2 , column = 0 , padx = 2 , pady = 2)
cup_tel_ent.grid(row = 2 , column = 1 , padx = 2 , pady = 2)


populate_tree()
tv.bind('<<TreeviewSelect>>', selected)
mainloop()
