from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import pymysql
from tkinter import ttk
import ttkthemes
import time
from tkinter import filedialog
import csv
from datetime import datetime
import io
import hashlib

MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Rootphilex'

def create_database():
    try:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database='smartprogram'
        )
        cursor = conn.cursor()
        cursor.execute('''   CREATE TABLE IF NOT EXISTS users_details(
    user_Id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(20),
    Name VARCHAR(20),
    Email VARCHAR(30),
    mobile_number VARCHAR(12),
    Id_number INT,
    Gender VARCHAR(20),
    Date VARCHAR(20),
    time_OF_Registration VARCHAR(20),
    Door_Id INT,
    Role VARCHAR(10),
    time_in DATETIME,
    verification_status VARCHAR(15),
    access_count INT
	,face_id INT,
	face_image LONGBLOB,
	secure_password VARCHAR(100)
); 
        ''')

   
        conn.commit()
        conn.close()
    except pymysql.Error as e:
        messagebox.showerror('Error', f'Failed to create database: {e}')

def signup():
    username = userEntry.get()
    passwo = passwordEntry.get()
    fullname = fullnameEntry.get()
    email = emailEntry.get()
    phone = phonenumberEntry.get()
    id_number = idnumberEntry.get()
    user_gender = gender.get()
   

    if username == '' or passwo == '' or fullname == '' or email == '' or phone == '' or id_number == '':
        messagebox.showerror('Error', 'All fields are required.')
    else:
        try:
            conn = pymysql.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database='smartprogram'
            )
            cursor = conn.cursor()
            Securepassword=hashlib.sha256(passwo.encode()).hexdigest()
            cursor.execute('''
            INSERT INTO users_details(user_name,Name,Email,mobile_number,Id_number,Gender,secure_password)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (
            username, fullname, email, phone, id_number, user_gender,  
            Securepassword
            ))
          
            conn.commit()
            conn.close()
            messagebox.showinfo('Success', 'Account created successfully')
            show_signin_page()
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Failed to create account: {e}')

def signin():
    username = userEntry.get()
    passw = passwordEntry.get()
    password = hashlib.sha256(passw.encode()).hexdigest()

    if username == '' or password == '':
        messagebox.showerror('Error', 'All fields are required.')
    else:
        try:
            conn = pymysql.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database='smartprogram'
            )
            cursor = conn.cursor()
            password = hashlib.sha256(passw.encode()).hexdigest()
            cursor.execute("SELECT * FROM users_details WHERE user_name=%s AND secure_password=%s", (username, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                messagebox.showinfo('Success', 'Welcome')
                #window.destroy()
                program()
                
                
            else:
                messagebox.showerror('Error', 'Invalid username or password')
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Failed to sign in: {e}')
            
            

def upload_profile_picture():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
    )
    if file_path:
        try:
           
            image = Image.open(file_path)
            image = image.resize((100, 100)) 
            
           
            display_image = ImageTk.PhotoImage(image)
            profile_image_label.config(image=display_image)
            profile_image_label.image = display_image
            
           
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format=image.format or 'PNG')
            global profile_picture_data
            profile_picture_data = img_byte_arr.getvalue()
            
        except Exception as e:
            messagebox.showerror('Error', f'Failed to load image: {e}')

def show_signup_page():
    signin_button.grid_remove()
    signup_button.grid(row=9, column=1, pady=20)
    show_signup_link.grid_remove()
    show_signin_link.grid(row=10, column=1, pady=10)
    fullnameLabel.grid(row=3, column=0,pady=5)
    fullnameEntry.grid(row=3, column=1,pady=5)
    emailLabel.grid(row=4, column=0,pady=5)
    emailEntry.grid(row=4, column=1,pady=5)
    phonenumberLabel.grid(row=5, column=0,pady=5)
    phonenumberEntry.grid(row=5, column=1,pady=5)
    idnumberLabel.grid(row=6, column=0,pady=5)
    idnumberEntry.grid(row=6, column=1,pady=5)
    genderLabel.grid(row=7, column=0,pady=5)
    gender.grid(row=7, column=1,padx=10,pady=5)
    
    profile_image_label.grid(row=8, column=0, pady=5)
    upload_picture_button.grid(row=8, column=1, pady=5)


def show_signin_page():
    signup_button.grid_remove()
    signin_button.grid(row=9, column=1, pady=20)
    show_signin_link.grid_remove()
    show_signup_link.grid(row=10, column=1, pady=10)
    fullnameLabel.grid_remove()
    fullnameEntry.grid_remove()
    profile_image_label.grid_remove()
    upload_picture_button.grid_remove()
    emailLabel.grid_remove()
    emailEntry.grid_remove()
    phonenumberLabel.grid_remove()
    phonenumberEntry.grid_remove()
    idnumberLabel.grid_remove()
    idnumberEntry.grid_remove()
    genderLabel.grid_remove()
    gender.grid_remove()

create_database()

window = ttkthemes.ThemedTk()
window.get_themes()
window.set_theme('blue')
window.geometry('1288x700+0+0')
window.resizable(False, False)
backgroundImage = ImageTk.PhotoImage(file='c:\\Users\\Administrator\\Downloads\\pexels-rodrigo-souza-1275988-2531709.jpg')
bgimage = Label(window, image=backgroundImage)
window.title('SmartDoor')
Photop = ImageTk.PhotoImage(file='C:\\Users\\Administrator\\Downloads\\pexels-joppe-beurskens-22992471-6689289.jpg')
window.iconphoto(True, Photop)




def program():
    
    try:
        signupFrame.destroy()
    except NameError:
        print("signupFrame is not defined")

    
    s = 'SMART DOOR MANAGEMENT SYSTEM'
    global count, text
    count = 0  
    text = ""
   
    
    sliderLabel = Label(window, text=s, font=('times new roman', 30, 'bold'), bg="light blue")
    sliderLabel.place(x=200, y=28)
    
    
    def slider_p():
        global text, count
        if count == len(s):
            count = 0
            text = ''
        text += s[count]
        sliderLabel.config(text=text)
        count += 1
        sliderLabel.after(300, slider_p)
    
    slider_p()  
    
    
    
    
    text_widget = Text(window, wrap=WORD, width=70, height=90,font=("Arial",20,'bold'),bg='#0F95A3')
    text_widget.place(y=100, x=50,height=250)
    paragraph = (
        "Tkinter is a GUI toolkit for Python that allows you to create "
        "interactive applications. It provides various widgets, such as buttons, "
        "labels, text boxes, and more, to help build user-friendly interfaces. "
        "You can customize these widgets to suit your application's needs."
    )
    text_widget.insert(END, paragraph)
    text_widget.config(state=DISABLED)
    
    
    def project():
        sliderLabel.destroy()
        text_widget.destroy()
        programButton.destroy()
        try:
            mlabel.destroy()
        except NameError:
            print("mlabel is not defined")
        nextpage()

    
    programButton =Button(window, text="continue",font=("Arial",20,'bold'),bg='#0F95A3',command=project)
    programButton.place(y=400, x=500)
    
    mlabel =Label(window, text="Devs                             Smartdoor                             Corporation",font=('Arial',20,"bold"),bg='#0F95A3')
    mlabel.place(y=600, x=200)
   


def modify():
    #window.get_themes()
    #window.set_theme('blue')
    
    groundImage = ImageTk.PhotoImage(file='c:\\Users\\Administrator\\Downloads\\pexels-rodrigo-souza-1275988-2531709.jpg')
    bgimage = Label(window, image=groundImage)

    bottomFrame = ttk.Frame(window)
    bottomFrame.place(x=210, y=80, width=1080, height=620)

    columns = ('user_Id', 'user_name','Name','Email', 'Mobile_number', 'Id_number','Gender','Date','time_OF_registration','Door_id','Role','time_in','verification_status','access_account','face_id','face_image','secure_password')
    user_table = ttk.Treeview(bottomFrame, columns=columns, show='headings')

    for col in columns:
       user_table.heading(col, text=col)
       user_table.column(col, width=100, anchor='center')

    user_table.column('Name', width=150)
    user_table.column('Email', width=200)

    scrollbar_x = ttk.Scrollbar(bottomFrame, orient='horizontal', command=user_table.xview)
    scrollbar_y = ttk.Scrollbar(bottomFrame, orient='vertical', command=user_table.yview)

    user_table.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

    scrollbar_x.pack(side='bottom', fill='x')
    scrollbar_y.pack(side='right', fill='y')
    user_table.pack(expand=True, fill='both')
   

    def delete_user():
            selected_item = user_table.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select a user to delete")
                return

            user_id = user_table.item(selected_item)['values'][0]
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user {user_id}?")
            if confirm:
                try:
                    mycursor.execute("DELETE FROM users_details WHERE id = %s", (user_id,))
                    con.commit()
                    messagebox.showinfo("Success", f"User {user_id} deleted successfully")
                    display_data()
                except pymysql.Error as e:
                    messagebox.showerror("Error", f"Failed to delete user: {str(e)}")

    def update_user():
            selected_item = user_table.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select a user to update")
                return

            user_data = user_table.item(selected_item)['values']
            update_window = Toplevel(window)
            update_window.title("Update User")
            update_window.geometry("400x400")

            fields = ['user_ID', 'username', 'Name', 'Email', 'mobile_number', 'Id_number']
            entries = {}

            for i, field in enumerate(fields):
                Label(update_window, text=field).grid(row=i, column=0, padx=10, pady=5)
                entry = Entry(update_window)
                entry.insert(0, user_data[i])
                entry.grid(row=i, column=1, padx=10, pady=5)
                entries[field.lower()] = entry

            def save_changes():
                values = [entries[field.lower()].get() for field in fields]
                if not all(values):
                    messagebox.showerror("Error", "All fields are required", parent=update_window)
                    return

                try:
                    mycursor.execute("""
                        UPDATE users_details
                        SET user_name = %s, Name = %s, Email = %s, mobile_number = %s, Id_number = %s
                        WHERE user_id = %s
                    """, (values[1], values[2], values[3], values[4], values[5], values[0]))
                    con.commit()
                    messagebox.showinfo("Success", "User updated successfully", parent=update_window)
                    update_window.destroy()
                    display_data()
                except pymysql.Error as e:
                    messagebox.showerror("Error", f"Failed to update user: {str(e)}", parent=update_window)

            ttk.Button(update_window, text="Save Changes", command=save_changes).grid(row=len(fields), column=0, columnspan=2, pady=20)





            
            
            
    def search_user():
        search_window = Toplevel()
        search_window.title("Search User")
        search_window.geometry("400x200")

        Label(search_window, text="Search by:").grid(row=0, column=0, padx=10, pady=5)
        search_by = ttk.Combobox(search_window, values=['Id_number', 'Name', 'Email', 'Mobile_number'])
        search_by.grid(row=0, column=1, padx=10, pady=5)
        search_by.set('ID')

        Label(search_window, text="Search value:").grid(row=1, column=0, padx=10, pady=5)
        search_value = Entry(search_window)
        search_value.grid(row=1, column=1, padx=10, pady=5)

        def perform_search():
            field = search_by.get().lower()
            value = search_value.get()
            if not value:
                messagebox.showerror("Error", "Please enter a search value", parent=search_window)
                return

            try:
                mycursor.execute(f"SELECT * FROM users_details WHERE {field} LIKE %s", (f"%{value}%",))
                results = mycursor.fetchall()
                user_table.delete(*user_table.get_children())
                for row in results:
                    user_table.insert('', 'end', values=row)
                search_window.destroy()
            except pymysql.Error as e:
                messagebox.showerror("Error", f"Search failed: {str(e)}", parent=search_window)

        ttk.Button(search_window, text="Search", command=perform_search).grid(row=2, column=0, columnspan=2, pady=20)



    def export_data():
        if len(user_table.get_children()) < 1:
            messagebox.showerror('No Data', 'No data available to export')
            return
        file = filedialog.asksaveasfilename(defaultextension='.csv')
        with open(file, mode='w', newline='') as myfile:
            exp_writer = csv.writer(myfile, delimiter=',')
            for i in user_table.get_children():
                row = user_table.item(i)['values']
                exp_writer.writerow(row)
        messagebox.showinfo('Data Exported', 'Your data has been exported to ' + file + ' successfully.')


    #search_window = Toplevel()
    #search_window.grab_set()
    #search_window.title('Search Data')



    #nameLabel = Label(search_window, text='NAME', font=('times new roman', 20, 'bold'))
    #nameLabel.grid(row=1, column=0, padx=30, pady=20)
    #nameEntry = Entry(search_window, font=('roman', 20, 'bold'), width=20)
    #nameEntry.grid(row=1, column=1)

    #emailLabel = Label(search_window, text='EMAIL', font=('times new roman', 20, 'bold'))
    #emailLabel.grid(row=2, column=0, padx=30, pady=20)
    #emailEntry = Entry(search_window, font=('roman', 20, 'bold'), width=20)
    #emailEntry.grid(row=2, column=1)

    #mobileLabel = Label(search_window, text='MOBILE NUMBER', font=('times new roman', 20, 'bold'))
    #mobileLabel.grid(row=3, column=0, padx=30, pady=20)
    #mobileEntry = Entry(search_window, font=('roman', 20, 'bold'), width=20)
    #mobileEntry.grid(row=3, column=1)

    #search_button = Button(search_window, text='SEARCH', command=search_data)
    #search_button.grid(row=4, column=1, pady=20)

    def add():
        def add_data():
            if idEntry.get() == '' or nameEntry.get() == '':
                messagebox.showerror('Error', 'All fields are required', parent=add_window)
            else:
                date = time.strftime('%d/%m/%y')
                currenttime = time.strftime('%H:%M:%S')

                try:
                    query = 'INSERT INTO users_details (Id_number, Name, Email, mobile_number, Role, Door_id, Date, time_OF_registration) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
                    mycursor.execute(query, (idEntry.get(), nameEntry.get(), emailEntry.get(), mobileEntry.get(), roleEntry.get(), dooridEntry.get(), date, currenttime))
                    con.commit()
                    result = messagebox.askyesno('Confirm', 'Data added successfully. Do you want to clear the form?', parent=add_window)
                    if result:
                        idEntry.delete(0, END)
                        nameEntry.delete(0, END)
                        emailEntry.delete(0, END)
                        mobileEntry.delete(0, END)
                        dooridEntry.delete(0, END)
                        roleEntry.delete(0, END)
                except pymysql.err.IntegrityError:
                    messagebox.showerror('Error', 'ID cannot be repeated', parent=add_window)
                    return

                display_data() 

        add_window = Toplevel()
        add_window.grab_set()
        add_window.title('Add User')

        idLabel = Label(add_window, text='ID NUMBER', font=('times new roman', 20, 'bold'))
        idLabel.grid(row=0, column=0, padx=30, pady=20)
        idEntry = Entry(add_window, font=('roman', 20, 'bold'), width=20)
        idEntry.grid(row=0, column=1)

        nameLabel = Label(add_window, text='NAME', font=('times new roman', 20, 'bold'))
        nameLabel.grid(row=1, column=0, padx=30, pady=20)
        nameEntry = Entry(add_window, font=('roman', 20, 'bold'), width=20)
        nameEntry.grid(row=1, column=1)

        emailLabel = Label(add_window, text='EMAIL', font=('times new roman', 20, 'bold'))
        emailLabel.grid(row=2, column=0, padx=30, pady=20)
        emailEntry = Entry(add_window, font=('roman', 20, 'bold'), width=20)
        emailEntry.grid(row=2, column=1)

        mobileLabel = Label(add_window, text='MOBILE NUMBER', font=('times new roman', 20, 'bold'))
        mobileLabel.grid(row=3, column=0, padx=30, pady=20)
        mobileEntry = Entry(add_window, font=('roman', 20, 'bold'), width=20)
        mobileEntry.grid(row=3, column=1)

        roleLabel = Label(add_window, text='ROLE', font=('times new roman', 20, 'bold'))
        roleLabel.grid(row=4, column=0, padx=30, pady=20)
        roleEntry = Entry(add_window, font=('roman', 20, 'bold'), width=20)
        roleEntry.grid(row=4, column=1)

        dooridLabel = Label(add_window, text='DOOR ID', font=('times new roman', 20, 'bold'))
        dooridLabel.grid(row=5, column=0, padx=30, pady=20)
        dooridEntry = Entry(add_window, font=('roman', 20, 'bold'), width=20)
        dooridEntry.grid(row=5, column=1)

        add_button = ttk.Button(add_window, text='ADD INFO', command=add_data)
        add_button.grid(row=6, column=1, pady=20)  

    def display_data():
        user_table.delete(*user_table.get_children())
        query = 'SELECT * FROM users_details'
        mycursor.execute(query)
        for row in mycursor.fetchall():
            user_table.insert('', END, values=row)
   

    def connect_database():
        def connect():
            global mycursor, con
            try:
                con = pymysql.connect(
                    host=hostEntry.get(),
                    user=userEntry.get(),
                    password=passwordEntry.get()
            )
                mycursor = con.cursor()
            
                mycursor.execute("CREATE DATABASE IF NOT EXISTS smartprograam")
                mycursor.execute("USE smartprogram")
                mycursor.execute("""
                                 
                                 CREATE TABLE IF NOT EXISTS users_details (
    user_Id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(20),
    Name VARCHAR(20),
    Email VARCHAR(30),
    mobile_number VARCHAR(12),
    Id_number INT,
    Gender VARCHAR(20),
    Date VARCHAR(20),
    time_OF_Registration VARCHAR(20),
    Door_Id INT,
    Role VARCHAR(10),
    time_in DATETIME,
    verification_status VARCHAR(15),
    access_count INT
);
                                
                   
            """)
            
                con.commit()
                messagebox.showinfo('Success', 'Database connection successful', parent=connectproject)
                connectproject.destroy()
                addbutton.config(state=NORMAL)
                searchbutton.config(state=NORMAL)
                deletebutton.config(state=NORMAL)
                exportbutton.config(state=NORMAL)
                updatebutton.config(state=NORMAL)
                 
                display_data() 
            except pymysql.Error as e:
                messagebox.showerror('Error', f'Database connection failed: {str(e)}', parent=connectproject)

        connectproject = Toplevel()
        connectproject.grab_set()
        connectproject.geometry('470x250+730+230')
        connectproject.title('Database Connection')
        connectproject.resizable(0, 0)

        hostnameLabel = Label(connectproject, text='Host name', font=('Arial', 10, 'bold'))
        hostnameLabel.grid(row=0, column=0, padx=20)
        hostEntry = Entry(connectproject, font=('roman', 10, 'bold'), bd=2)
        hostEntry.grid(row=0, column=1, padx=40, pady=20)

        userLabel = Label(connectproject, text='User Name', font=('arial', 10, 'bold'))
        userLabel.grid(row=1, column=0, padx=20)
        userEntry = Entry(connectproject, font=('roman', 10, 'bold'), bd=2)
        userEntry.grid(row=1, column=1, padx=40, pady=20)

        passwordLabel = Label(connectproject, text='Password', font=('Arial', 10, 'bold'))
        passwordLabel.grid(row=2, column=0, padx=20)
        passwordEntry = Entry(connectproject, font=('roman', 10, 'bold'), bd=2, show='*')
        passwordEntry.grid(row=2, column=1, padx=40, pady=20)

        ctbutton = ttk.Button(connectproject, text='CONNECT', command=connect)
        ctbutton.grid(row=3, columnspan=2)

    topFrame = ttk.Frame(window)
    topFrame.place(x=5, y=80, width=205, height=650)

    addbutton = ttk.Button(topFrame, text='ADD', width=20, command=add, state=DISABLED)
    addbutton.grid(row=1, column=0, pady=30)

    deletebutton = ttk.Button(topFrame, text='DELETE', width=20, command=delete_user, state=DISABLED)
    deletebutton.grid(row=3, column=0, pady=30)



    updatebutton = ttk.Button(topFrame, text='UPDATE', width=20, command=update_user, state=DISABLED)
    updatebutton.grid(row=4, column=0, pady=30)

    searchbutton = ttk.Button(topFrame, text='SEARCH', width=20, command=search_user, state=DISABLED)
    searchbutton.grid(row=5, column=0, pady=30)



    exportbutton = ttk.Button(topFrame, text='EXPORT INFO', width=20, command=export_data, state=DISABLED)
    exportbutton.grid(row=6, column=0, pady=30)

    mybuttonc = ttk.Button(topFrame, text='SHOW DATA',width=20, command=connect_database)
    mybuttonc.grid(row=0,column=0,pady=30)
    
    
    

    def timed():
        date = time.strftime('%d/%m/%y')
        currenttime = time.strftime('%H:%M:%S')
        datetimeLabel.config(text=f'Date: {date}\nTime: {currenttime}')   
        datetimeLabel.after(1000, timed)



    datetimeLabel = Label(window, text='Hi', font=('times new roman', 20, 'bold'),bg="light blue")
    datetimeLabel.place(x=5, y=10)

    timed()
    
    s = 'SMART DOOR MANAGEMENT SYSTEM'
    global count,text
    cout=0
    text=""
    
    def slider_p():
      global text, count
      if count == len(s):
            count = 0
            text = ''
      text = text + s[count]
      sliderLabel.config(text=text)
      count += 1
      sliderLabel.after(300, slider_p)
    
    
    sliderLabel = Label(window, text=s, font=('times new roman', 30, 'bold'),bg="light blue")
    sliderLabel.place(x=200, y=28)
  
   
    def exit_program():
        #exitlabel =Label(window,text="THANK YOU FOR USING THE SMART DOOR MANAGEMENT SYSTEM",FONT=("ARIAL",70,"BOLD"))
        #exitlabel.pack()
        window.quit()

    exitbutton = ttk.Button(topFrame, text='EXIT', command= exit_program)
    exitbutton.grid(row=7,column=0,pady=30)

    
   


    






#profileFrame = Frame(window, bg='Indigo')
#profileFrame.place(x=0, y=0)

bgimage.place(x=0, y=0)
#profilePhoto = PhotoImage(file='C:\\Users\\Administrator\\Downloads\\student.png')
#profileLabel = Label(profileFrame, image=profilePhoto)
#profileLabel.grid(row=0, column=10)

signupFrame = Frame(window, bg="#0F95A3",relief='solid')
signupFrame.place(x=400, y=100)

profile_image_label = Label(signupFrame, text="No image selected", bg='#0F95A3')
upload_picture_button = ttk.Button(signupFrame, text="Upload Profile Picture", command=upload_profile_picture)


logoSignup = PhotoImage(file='C:\\Users\\Administrator\\Downloads\\student.png')
logoLabel = Label(signupFrame, image=logoSignup, bg='#0F95A3')
logoLabel.grid(row=0, column=0, columnspan=3)

userImage = PhotoImage(file='C:\\Users\\Administrator\\Downloads\\user.png')

usernameLabel = Label(signupFrame, image=userImage, text='Username', compound=LEFT, font=('times new roman', 15, 'bold'),bg='#0F95A3')
usernameLabel.grid(row=1, column=0)

userEntry = Entry(signupFrame, font=('times new roman', 15, 'bold'),width=20,)
userEntry.grid(row=1, column=1,padx=10)

passwordImage = PhotoImage(file='C:\\Users\\Administrator\\Downloads\\padlock (2).png')

passwordLabel = Label(signupFrame, image=passwordImage, compound=LEFT, text='Password', font=('times new roman', 15, 'bold'),bg='#0F95A3')
passwordLabel.grid(row=2, column=0,pady=5)

passwordEntry = Entry(signupFrame, font=('times new roman', 15, 'bold'), show='*')
passwordEntry.grid(row=2, column=1,pady=5)

fullnameLabel = Label(signupFrame, text='Full Name', font=('times new roman', 15, 'bold'),bg='#0F95A3')
fullnameEntry = Entry(signupFrame, font=('times new roman', 15, 'bold'))

emailLabel = Label(signupFrame, text='Email', font=('times new roman', 15, 'bold'),bg='#0F95A3')
emailEntry = Entry(signupFrame, font=('times new roman', 15, 'bold'))

phonenumberLabel = Label(signupFrame, text='Phone Number', font=('times new roman', 15, 'bold'),bg='#0F95A3')
phonenumberEntry = Entry(signupFrame, font=('times new roman', 15, 'bold'))

idnumberLabel = Label(signupFrame, text='ID Number', font=('times new roman', 15, 'bold'),bg='#0F95A3')
idnumberEntry = Entry(signupFrame, font=('times new roman', 15, 'bold'),width=20)

genderLabel = Label(signupFrame, text='Select Gender(Optional)', font=('times new roman', 15, 'bold'),bg='#0F95A3')
gender = ttk.Combobox(signupFrame, font=('times new roman', 15, 'bold'),values=["Male","Female"])
gender.set("Male")

signup_button = Button(signupFrame, text='SIGN UP', font=('times new roman', 20, 'bold'), bg='cornflowerblue', fg='white', activeforeground='white', activebackground='cornflowerblue', command=signup)
signin_button = Button(signupFrame, text='SIGN IN', font=('times new roman', 20, 'bold'), bg='cornflowerblue', fg='white', activeforeground='white', activebackground='cornflowerblue', command=signin)

show_signup_link = Button(signupFrame, text="Don't have an account? Sign up", font=('times new roman', 10), bg='#0F95A3', fg='black', bd=0, command=show_signup_page)
show_signin_link = Button(signupFrame, text="Already have an account? Sign in", font=('times new roman', 10), bg='#0F95A3', fg='black', bd=0, command=show_signin_page)

show_signin_page()  

def remove():
    bgimage.config(image="")


def nextpage():
    
    modify()
    
    


window.mainloop()