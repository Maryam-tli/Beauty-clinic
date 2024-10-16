from tkinter import *
from tkinter import ttk
from pymongo import MongoClient

# اتصال به MongoDB
Client = MongoClient("localhost", 27017)
db = Client["person"]
persons = db["persons"]

# ایجاد پنجره اصلی
screen = Tk()
screen.geometry("700x600+10+10")
screen.configure(background="light gray")

# بارگذاری تصویر پس‌زمینه
back = PhotoImage(file="back.png")
screen.title("Beauty Clinic")
lbback = Label(screen, image=back).pack()

screen.iconbitmap("up.ico")

# تعریف متغیرهای ورودی
id = IntVar()
Name = StringVar()
Family = StringVar()
Age = StringVar()
Date = StringVar()
Time = StringVar()

# ایجاد و تنظیم برچسب و ورودی‌ها
bigtit = Label(screen, text="Beauty Clinic Reservation Portal", font=("Alegreya", 20), bg="#054919", fg="white")
bigtit.place(x=140, y=10)

laname = Label(screen, text="Full name", fg="white", bg="#063714", font=("Alegreya", 15))
laname.place(x=10, y=80)

# تعریف ورودی نام
enname = Entry(screen, textvariable=Name)
enname.insert(0, "MaryamTavakoli")
enname.config(fg="gray")
enname.place(x=120, y=85)

lafamily = Label(screen, text="Phone", bg="#063714", fg="white", font=("Alegreya", 15))
lafamily.place(x=10, y=125)

# تعریف ورودی Phone
enfamily = Entry(screen, textvariable=Family)
enfamily.insert(0, "09123456789")  # متن پیش‌فرض برای Phone
enfamily.config(fg="gray")
enfamily.place(x=120, y=125)

laage = Label(screen, text="Age", bg="#063714", fg="white", font=("Alegreya", 15))
laage.place(x=10, y=170)

# تعریف ورودی Age
enage = Entry(screen, textvariable=Age)
enage.insert(0, "25")  # متن پیش‌فرض برای Age
enage.config(fg="gray")
enage.place(x=120, y=170)

ladate = Label(screen, text="Date", bg="#063714", fg="white", font=("Alegreya", 15))
ladate.place(x=10, y=220)

# تعریف ورودی Date
endate = Entry(screen, textvariable=Date)
endate.insert(0, "YYYY-MM-DD")  # متن پیش‌فرض برای Date
endate.config(fg="gray")
endate.place(x=120, y=220)

latime = Label(screen, text="Time", bg="#063714", fg="white", font=("Alegreya", 15))
latime.place(x=10, y=270)

# تعریف ورودی Time
entime = Entry(screen, textvariable=Time)
entime.insert(0, "HH:MM")  # متن پیش‌فرض برای Time
entime.config(fg="gray")
entime.place(x=120, y=270)

# ایجاد یک فریم برای جدول و اسکرول
frame = Frame(screen)
frame.place(x=10, y=320, width=680, height=260)

# ایجاد اسکرول عمودی
scrollbar = Scrollbar(frame)
scrollbar.pack(side=RIGHT, fill=Y)

# ایجاد جدول و اتصال آن به اسکرول عمودی
tbl = ttk.Treeview(frame, columns=("a1", "a2", "a3", "a4", "a5", "a6"), show="headings", height=12,
                   yscrollcommand=scrollbar.set)
tbl.column("a1", width=50)
tbl.heading("a1", text="Id")
tbl.column("a2", width=110)
tbl.heading("a2", text="Full Name")
tbl.column("a3", width=130)
tbl.heading("a3", text="Phone")
tbl.column("a4", width=80)
tbl.heading("a4", text="Age")
tbl.column("a5", width=110)
tbl.heading("a5", text="Date")
tbl.column("a6", width=80)
tbl.heading("a6", text="Time")
tbl.pack(side=LEFT, fill=BOTH, expand=True)

# اتصال اسکرول به جدول
scrollbar.config(command=tbl.yview)

# تابع برای اضافه کردن شخص به جدول و MongoDB
def add_person():
    # ایجاد دیکشنری از اطلاعات وارد شده
    person = {
        "Id": len(tbl.get_children()) + 1,  # Id بر اساس تعداد رکوردهای موجود
        "Full Name": Name.get(),
        "Phone": Family.get(),
        "Age": Age.get(),
        "Date": Date.get(),
        "Time": Time.get()
    }

    # اضافه کردن شخص به جدول
    tbl.insert("", "end", values=(
    person["Id"], person["Full Name"], person["Phone"], person["Age"], person["Date"], person["Time"]))

    # اضافه کردن شخص به پایگاه داده MongoDB
    persons.insert_one(person)


# بازیابی داده‌ها از MongoDB و نمایش در جدول هنگام راه‌اندازی برنامه
def load_data():
    for person in persons.find():
        tbl.insert("", "end", values=(
        person["Id"], person["Full Name"], person["Phone"], person["Age"], person["Date"], person["Time"]))

# تابع برای انتقال داده‌های سطر انتخابی به ورودی‌ها
def set_to_entries(event):
    selected_item = tbl.focus()  # آیتم انتخاب شده
    if selected_item:
        values = tbl.item(selected_item, 'values')
        if values:
            Name.set(values[1])
            Family.set(values[2])
            Age.set(values[3])
            Date.set(values[4])
            Time.set(values[5])

# تابع برای حذف سطر انتخابی و پاک کردن ورودی‌ها
def delete_selected():
    selected_item = tbl.focus()  # آیتم انتخاب شده
    if selected_item:
        values = tbl.item(selected_item, 'values')
        if values:
            # حذف از MongoDB
            persons.delete_one({"Id": int(values[0])})
            # حذف از جدول
            tbl.delete(selected_item)
            # پاک کردن ورودی‌ها
            Name.set("")
            Family.set("")
            Age.set("")
            Date.set("")
            Time.set("")

# تابع برای به‌روزرسانی سطر انتخابی در جدول و MongoDB
def update_selected():
    selected_item = tbl.focus()  # آیتم انتخاب شده
    if selected_item:
        values = tbl.item(selected_item, 'values')
        if values:
            updated_person = {
                "Full Name": Name.get(),
                "Phone": Family.get(),
                "Age": Age.get(),
                "Date": Date.get(),
                "Time": Time.get()
            }

            # به‌روزرسانی در MongoDB
            persons.update_one({"Id": int(values[0])}, {"$set": updated_person})

            # به‌روزرسانی در جدول
            tbl.item(selected_item, values=(
                values[0], updated_person["Full Name"], updated_person["Phone"],
                updated_person["Age"], updated_person["Date"], updated_person["Time"]
            ))


# تعریف توابع
def Inenname(e):
    if enname.get() == "MaryamTavakoli":
        enname.delete(0, "end")
        enname.config(fg="black")  # تغییر رنگ متن به مشکی


def Outenname(e):
    if enname.get() == "":
        enname.insert(0, "MaryamTavakoli")
        enname.config(fg="gray")  # تغییر رنگ متن به خاکستری


def Infamily(e):
    if enfamily.get() == "09123456789":
        enfamily.delete(0, "end")
        enfamily.config(fg="black")  # تغییر رنگ متن به مشکی


def Outfamily(e):
    if enfamily.get() == "":
        enfamily.insert(0, "09123456789")
        enfamily.config(fg="gray")  # تغییر رنگ متن به خاکستری


def Inage(e):
    if enage.get() == "25":
        enage.delete(0, "end")
        enage.config(fg="black")  # تغییر رنگ متن به مشکی


def Outage(e):
    if enage.get() == "":
        enage.insert(0, "25")
        enage.config(fg="gray")  # تغییر رنگ متن به خاکستری

def Indate(e):
    if endate.get() == "YYYY-MM-DD":
        endate.delete(0,"end")
        endate.config(fg="black")

def Outdate(e):
    if endate.get() == "":
        endate.insert(0,"YYYY-MM-DD")
        endate.config(fg="gray")


def Intime(e):
    if entime.get() == "HH:MM":
        entime.delete(0, "end")
        entime.config(fg="black")  # تغییر رنگ متن به مشکی


def Outtime(e):
    if entime.get() == "":
        entime.insert(0, "HH:MM")
        entime.config(fg="gray")  # تغییر رنگ متن به خاکستری


# اتصال رویدادهای FocusIn و FocusOut به ورودی‌ها
enname.bind("<FocusIn>", Inenname)
enname.bind("<FocusOut>", Outenname)

enfamily.bind("<FocusIn>", Infamily)
enfamily.bind("<FocusOut>", Outfamily)

enage.bind("<FocusIn>", Inage)
enage.bind("<FocusOut>", Outage)

endate.bind("<FocusIn>", Indate)
endate.bind("<FocusOut>", Outdate)

entime.bind("<FocusIn>", Intime)
entime.bind("<FocusOut>", Outtime)

# دکمه افزودن شخص
btnadd = Button(screen, text="Create", bg="#76312c", fg="white", font=("Alegreya", 12), command=add_person)
btnadd.place(x=270, y=260)

# دکمه حذف شخص
btndelete = Button(screen, text="Delete", fg="white", bg="#76312c", font=("Alegreya", 12), command=delete_selected)
btndelete.place(x=350, y=262)

# دکمه به‌روزرسانی شخص
btnupdate = Button(screen, text="Update", fg="white", bg="#76312c", font=("Alegreya", 12), command=update_selected)
btnupdate.place(x=425, y=263)


# بارگذاری اطلاعات از MongoDB هنگام باز شدن برنامه
load_data()

# اتصال انتخاب سطر به تابع set_to_entries
tbl.bind("<<TreeviewSelect>>", set_to_entries)

# تابع جستجو و نمایش پیشنهادات
def search_records(event):
    search_term = ensearch.get()
    listbox.delete(0, END)  # حذف آیتم‌های قبلی

    # جستجو در پایگاه داده
    search_results = persons.find({"Full Name": {"$regex": search_term, "$options": "i"}})
    for result in search_results:
        listbox.insert(END, f'{result["Full Name"]} ({result["Phone"]})')

# نمایش سطر انتخاب شده از Listbox در جدول
def show_selected_record(event):
    selected_value = listbox.get(listbox.curselection())
    if selected_value:
        selected_name = selected_value.split(" (")[0]  # گرفتن فقط نام کامل
        tbl.delete(*tbl.get_children())  # پاک کردن جدول
        search_result = persons.find_one({"Full Name": selected_name})
        if search_result:
            tbl.insert("", "end", values=(search_result["Id"], search_result["Full Name"], search_result["Phone"],
                                          search_result["Age"], search_result["Date"], search_result["Time"]))

# فریم و جعبه جستجو
searchframe = Frame(screen, height=200, width=200, background="#054919")
searchframe.place(x=400, y=55)
Search = StringVar()
lasearch = Label(searchframe, text="Search", font=("Alegreya", 8))
lasearch.place(x=10, y=5)
ensearch = Entry(searchframe, textvariable=Search)
ensearch.place(x=64, y=6)
ensearch.bind("<KeyRelease>", search_records)

# لیست نتایج
listbox = Listbox(searchframe)
listbox.place(x=10, y=30, width=180, height=150)
listbox.bind("<<ListboxSelect>>", show_selected_record)

screen.mainloop()