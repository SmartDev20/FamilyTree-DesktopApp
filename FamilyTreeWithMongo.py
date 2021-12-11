# -*- coding: UTF-8 -*-
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pymongo
import datetime
from tkcalendar import Calendar, DateEntry
import easygui as eg
from PIL import Image, ImageTk
import io
from bson import Binary
import matplotlib.pyplot as plt





root = Tk()
root.geometry('940x700')
root.title('Family Tree')
root.bg='#0B5A81'
root.config(bg='#0B5A81')



try:
     URI = "mongodb://127.0.0.1:27017"
     client = pymongo.MongoClient(URI)
     db = client['FamilyTree']
      
except Exception as ex :
       messagebox.showerror('SQL Eroor' , ex)

 
gen = StringVar()
cup_name = StringVar()
cup_add = StringVar()
cup_tel = StringVar()
brd = StringVar()
ded = StringVar()
img_path = StringVar()
name = StringVar()
add = StringVar()
prt_name = StringVar()
tel = StringVar()
job = StringVar()
prt_name_lb = StringVar()
cup_name_lb_var = StringVar()
cup_add_lb_var = StringVar()
cup_tel_lb_var = StringVar()
img_obj_lb_var = StringVar()

def insert(collection , data) :
    db[collection].insert_one(data)
    
    
              
def get_all_data(collection , query):
    return db[collection].find(query)
    
 
def get_one_item(collection , query):
    return db[collection].find_one(query)
               
               
def populate_tree() :
    item_list = [item for item in get_all_data('tree' , {})]
    for row in item_list :
        tv.insert( row["perant_id"], value = row["name"] , index = 10 , text = row["name"] , iid = row["_id"])
        
def clear_widg() :
    name_ent.delete( first=0, last=END )
    add_ent.delete( 0, END )
    tel_ent.delete( 0, last=END )
    gen.set('')
    job_ent.delete(0, END )
    prt_ent.delete( first=0, last=END )
    brd_ent.delete( 0, last=END )
    ded_ent.delete( 0, last=END )
    cup_name.set('')
    cup_add.set('')
    cup_tel.set('')
    
    
def get_json_format(item_id , prt_id) :
    record = { "_id" : item_id , "perant_id" : prt_id , "name" : name_ent.get() ,
               "address" : add_ent.get() , "telephone" : tel_ent.get() , "birthday" :brd_ent.get() ,
                "parent_name" : prt_ent.get() , "cup_name" : cup_name_ent.get() ,
               "cup_add" : cup_add_ent.get() , "cup_tel" : cup_tel_ent.get() , "deathday" : ded_ent.get() , 
               "image" : img_pt_lb['text'] , "job" : job_ent.get() , "gender" : gen.get() , "id" : str(item_id) ,"img" : get_img_opj() }
    return record
    
    

    
def selected(event) :
    
    item_id = str(tv.focus())
    row = get_one_item('tree' , {"_id" : item_id})
    name.set(row["name"])
    add.set(row["address"])
    prt_name.set(row["parent_name"])
    cup_name.set(row["cup_name"])
    cup_add.set(row["cup_add"])
    cup_tel.set(row["cup_tel" ])
    brd.set(row["birthday"])
    ded.set(row["deathday"])
    tel.set(row["telephone"])
    img_path.set(row["image"])
    job.set(row["job"])
    img_path.set(row["image"])
    gen.set(row["gender"])
    
    #plt.imshow(pil_img)
    #plt.show()
   
    try :
        
        #path = row["image"]
        #img = Image.open(path)
        #img = img.resize((200,200) , Image.ANTIALIAS)
        #img_opj = ImageTk.PhotoImage(img)
        #img_obj_lb.configure(image = img_opj)
        #img_obj_lb.image = img_opj
        pil_img = Image.open(io.BytesIO(row['img']))
        img_opj = ImageTk.PhotoImage(pil_img)
        img_obj_lb.configure(image = img_opj)
        img_obj_lb.image = img_opj
    except Exception as ex :
           messagebox.showinfo('' , ex)
           img_obj_lb.image = None
           img_obj_lb_var.set('Can not show image')
    gen_labels()
    
    def prt_gen(prt_id) :
        pt_row = get_one_item('tree' , {"_id" : prt_id})
        
        try :
           if pt_row["gender"] == 'male' :
              prt_name_lb.set('Mother Name')
           elif pt_row["gender"] == 'female' :
               prt_name_lb.set('Father Name')
        except TypeError as tr :
                prt_name_lb.set('Father Name')
    prt_id = row["perant_id"]
    prt_gen(prt_id)
    
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
    
def gen_labels() :
    if gen.get() == 'male' :
       
       cup_name_lb_var.set('Wife Name')
       cup_add_lb_var.set('Wife Address')
       cup_tel_lb_var.set('Wife Telephone')
    elif gen.get() == 'female' :
       
       cup_name_lb_var.set('Husbund Name')
       cup_add_lb_var.set('Husbund Address')
       cup_tel_lb_var.set('Husbund Telephone')

def set_brd() :
    brd.set(get_date())
    
    
def set_ded() :
    ded.set(get_date())
    
    
    
def get_img() :
    path = eg.fileopenbox()
    img_path.set(path)
    
    
def get_img_opj() :
    path =  img_pt_lb['text']
    img = Image.open(path)
    img = img.resize((200,200) , Image.ANTIALIAS)
    #img_opj = ImageTk.PhotoImage(img)
    imgByteArr = io.BytesIO()
    img.save(imgByteArr , format='jpeg')
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr
    
    
def add_root() :
    ok = verify_data() 
    if ok == 1 :
       messagebox.showinfo('' , 'Complete Data')
       return
    item_id = tv.insert('' , value = name_ent.get() , index = 10 , text = name_ent.get())
    #messagebox.showinfo('New ID' , item_id)
    try :
         record = get_json_format(item_id , prt_id = '')
         #messagebox.showinfo('' , record)
         insert('tree' , record)
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
         record = get_json_format(item_id , prt_id)
         #messagebox.showinfo('' , record)
         insert('tree' , record)
         messagebox.showinfo('confirmation', 'Record Saved')
         clear_widg()
    except Exception as ex :
          messagebox.showerror('SQL Eroor' , ex)
          

 
def verify_data():
     if name_ent.get() == '' :
         messagebox.showerror('' , 'Name can not be empty')
         return 1
     elif add_ent.get() == '' :
          messagebox.showerror('' , 'Address can not be empty')
          return 1
     if prt_name.get() == '' :
         messagebox.showerror('' , 'Parent name can not be empty')
         return 1
     elif job_ent.get() == '' :
          messagebox.showerror('' , 'Job can not be empty')
          return 1
     elif gen.get() == '' :
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
prt_lb = Label(per_frame , text = 'Parent Name', bg = '#CCCCCC' ,  textvariable = prt_name_lb)
prt_ent = Entry(per_frame , textvariable = prt_name)
#Gender
gen_frame = LabelFrame(per_frame , text = 'Gender' , bg = '#CCCCCC' , padx = 2 , pady = 2)
male_rb = Radiobutton(gen_frame , text = 'Male' , value = 'male' , bg = '#CCCCCC' , variable = gen )
feml_rb = Radiobutton(gen_frame , text = 'Female' , value = 'female' , variable = gen, bg = '#CCCCCC')
#Telephone
tel_lb = Label(per_frame , text =  'Telephone' , bg = '#CCCCCC')
tel_ent = Entry(per_frame , textvariable = tel )
#Job
job_lb = Label(per_frame , text =  'Job' , bg = '#CCCCCC')
job_ent = Entry(per_frame , textvariable = job )
#Birth Day
brd_lb = Label(per_frame , text =  'Birth Day' , bg = '#CCCCCC')
brd_ent = Entry(per_frame  , textvariable = brd)
brd_btn = Button(per_frame , text = 'Birth Date' , command = set_brd)
#Death Day
ded_lb = Label(det_frame , text =  'Death Day' , bg = '#CCCCCC')
ded_ent = Entry(det_frame , textvariable = ded )
ded_btn = Button(det_frame , text = 'Death Date' , command = set_ded)
#image
img_btn = Button(per_frame , text = 'Select Image' , command = get_img)
img_pt_lb = Label(per_frame , text =  '' , bg = '#CCCCCC' , textvariable = img_path)
img_obj_lb = Label(det_frame , textvariable = img_obj_lb_var )
#couple Name
cup_name_lb = Label(cup_frame , text = 'Couple Name', bg = '#CCCCCC' , textvariable = cup_name_lb_var)
cup_name_ent = Entry(cup_frame , textvariable = cup_name)
#Couple Address
cup_add_lb = Label(cup_frame , text = 'Couple Address', bg = '#CCCCCC' , textvariable = cup_add_lb_var)
cup_add_ent = Entry(cup_frame , textvariable = cup_add)
#Couple Telephone
cup_tel_lb = Label(cup_frame , text = 'Couple Telephone', bg = '#CCCCCC' , textvariable = cup_tel_lb_var)
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
ded_lb.grid(row = 3 , column = 0 , padx = 2 , pady = 2)
ded_btn.grid(row = 3 , column = 0 , padx = 2 , pady = 2)
ded_ent.grid(row = 3 , column = 1 , padx = 2 , pady = 2)
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
