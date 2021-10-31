#import libraries
from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from PIL import ImageTk,Image
from sqlite3 import *
import matplotlib.pyplot as plt
import requests
from tkinter import ttk
import bs4
from tkinter.ttk import Separator, Style

#--------------Getting Location : City---------------------------------------------

try:
	web_address = "https://ipinfo.io/"
	response = requests.get(web_address)
	print(response)

	data = response.json()

	city = data['city']
except Exception as e:
	showerror("Error", e)
#-----------------Getting Temperature : Celcius--------------------------------
try:
	a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
	a2 = "&q=kalyan"
	a3 = "&appid=" + "c6e315d09197cec231495138183954bd"

	wa = a1 + a2 + a3
	res = requests.get(wa)
	print(res)

	data = res.json()

	temperature = data['main']['temp']
	print(temperature)
	
except Exception as e:
	print("Issue", e)

#------------------Getting Quote of the Day-------------------------------------
try:
	web_address = "https://www.brainyquote.com/quote_of_the_day"
	response = requests.get(web_address)
	
	data = bs4.BeautifulSoup(response.text, 'html.parser')
	#print(data)

	info = data.find('img', {'class' : 'p-qotd'})
	#print(info)

	qotd = info['alt']
	print(qotd)	
except Exception as e:
	print(e)
#------------------------------------------------------------------------------
def view_add_btn():
	master.withdraw()
	add_window.deiconify()

def view_view_btn():
	master.withdraw()
	view_window.deiconify()
	info = ""
	scrolled_text.delete(1.0, END)
	try:
		con = connect("C:\Python 3.9\Database\student.db")
		cursor = con.cursor()
		sql = "select * from student"
		cursor.execute(sql)	
		data = cursor.fetchall()
		if data == []:
			showinfo("Message", "No record available")
			if con is not None:
				con.close()
			view_window.withdraw()
			master.deiconify()
		else:
			for d in data:
				info = info + "R_no = " + str(d[0]) + ", Name = " + str(d[1]) + ", Marks = " + str(d[2]) + "\n\n"
			scrolled_text.insert(INSERT, info)
	except Exception as e:
		showerror("Error", e)
	finally:
		if con is not None:
			con.close()

def view_update_btn():
	master.withdraw()
	update_window.deiconify()

def view_delete_btn():
	master.withdraw()
	delete_window.deiconify()

def back_main_from_add():
	add_window.withdraw()
	master.deiconify()

def back_main_from_view():
	view_window.withdraw()
	master.deiconify()

def back_main_from_update():
	update_window.withdraw()
	master.deiconify()

def back_main_from_delete():
	delete_window.withdraw()
	master.deiconify()

#------------------------------------------------------------------------------
def add_student():
	if (add_window_enter_rno.get() == "" or add_window_enter_name.get() == "" or add_window_enter_marks.get() == ""):
		showerror("Error", "Please fill all the details")
	elif (add_window_enter_rno.get().isdigit() == False):
		showerror("Erro", "Roll number can have integers only")
		add_window_enter_rno.delete(0, END)
		add_window_enter_name.delete(0, END)
		add_window_enter_marks.delete(0, END)
	elif (int(add_window_enter_rno.get()) <= 0) :
		showerror("Error", "Roll number can't be negative")
		add_window_enter_rno.delete(0, END)
		add_window_enter_name.delete(0, END)
		add_window_enter_marks.delete(0, END)
	elif (len(add_window_enter_name.get()) < 2):
		showerror("Error", "Name can't consist of only one alphabet")
		add_window_enter_rno.delete(0, END)
		add_window_enter_name.delete(0, END)
		add_window_enter_marks.delete(0, END)
	elif ((((add_window_enter_name.get()).replace(" ","")).isalpha()) == False):
		showerror("Error", "Name can't consist of digits")
		add_window_enter_rno.delete(0, END)
		add_window_enter_name.delete(0, END)
		add_window_enter_marks.delete(0, END)
	elif (add_window_enter_marks.get().isdigit() == False):
		showerror("Error", "Marks can be integers only")
		add_window_enter_rno.delete(0, END)
		add_window_enter_name.delete(0, END)
		add_window_enter_marks.delete(0, END)
	elif int(add_window_enter_marks.get()) < 0:
		showerror("Error", "Marks can't be negative")
		add_window_enter_rno.delete(0, END)
		add_window_enter_name.delete(0, END)
		add_window_enter_marks.delete(0, END)
	elif int(add_window_enter_marks.get()) > 100:
		showerror("Error", "Marks can't be greater than 100")
		add_window_enter_rno.delete(0, END)
		add_window_enter_name.delete(0, END)
		add_window_enter_marks.delete(0, END)
	else:
		list_rno = []
		con = None
		try:
			con=connect('C:\Python 3.9\Database\student.db')
			cursor=con.cursor()
			sql="select rno from student"
			cursor.execute(sql)
			data=cursor.fetchall()
			print(data)
			for d in data:	
				list_rno.append(int(str(d[0])))
				print(list_rno)
		except Exception as e:
			showerror("OOPS!", e)
		finally:
			if con is not None:
				con.close()
	
		rno = int(add_window_enter_rno.get())
		if rno in list_rno:
			showerror("OOPS!", "Student already present!")
			add_window_enter_rno.delete(0, END)
			add_window_enter_name.delete(0, END)
			add_window_enter_marks.delete(0, END)	
		else:
                        con = None
                        try:
                                rno = int(add_window_enter_rno.get())
                                name = add_window_enter_name.get()
                                marks = int(add_window_enter_marks.get())
                                con = connect("C:\Python 3.9\Database\student.db")
                                cursor = con.cursor()
                                sql = "insert into student values('%d', '%s', '%d')"
                                cursor.execute(sql % (rno, name, marks))
                                con.commit()
                                showinfo("Success", "Record inserted")
                                add_window_enter_rno.delete(0, END)
                                add_window_enter_name.delete(0, END)
                                add_window_enter_marks.delete(0, END)
                        except Exception as e:
                                showerror("OOPS!", e)
                                add_window_enter_rno.delete(0, END)
                                add_window_enter_name.delete(0, END)
                                add_window_enter_marks.delete(0, END)
                        finally:
                                if con is not None:
                                        con.close()

#-------------------------------------------------------------------------------
def update_student():
	if (update_window_enter_rno.get() == "" or update_window_enter_name.get() == "" or update_window_enter_marks.get() == ""):
		showerror("Error", "Please fill all the details")
	elif (update_window_enter_rno.get().isdigit() == False):
		showerror("Error", "Roll number can have integers only")
		update_window_enter_rno.delete(0, END)
		update_window_enter_name.delete(0, END)
		update_window_enter_marks.delete(0, END)
	elif int(update_window_enter_rno.get()) <= 0 :
		showerror("Error", "Roll number can't be negative")
		update_window_enter_rno.delete(0, END)
		update_window_enter_name.delete(0, END)
		update_window_enter_marks.delete(0, END)
	elif (len(update_window_enter_name.get()) < 2):
		showerror("Error", "Name can't consist of only one alphabet")
		update_window_enter_rno.delete(0, END)
		update_window_enter_name.delete(0, END)
		update_window_enter_marks.delete(0, END)
	elif ((((update_window_enter_name.get()).replace(" ","")).isalpha()) == False):
		showerror("Error", "Name can't consist of digits")
		update_window_enter_rno.delete(0, END)
		update_window_enter_name.delete(0, END)
		update_window_enter_marks.delete(0, END)
	elif (update_window_enter_marks.get().isdigit() == False):
		showerror("Error", "Marks can be integers only")
		update_window_enter_rno.delete(0, END)
		update_window_enter_name.delete(0, END)
		update_window_enter_marks.delete(0, END)
	elif int(update_window_enter_marks.get()) < 0:
		showerror("Error", "Marks can't be negative")
		update_window_enter_rno.delete(0, END)
		update_window_enter_name.delete(0, END)
		update_window_enter_marks.delete(0, END)
	elif int(update_window_enter_marks.get()) > 100:
		showerror("Error", "Marks can't be greater than 100")
		update_window_enter_rno.delete(0, END)
		update_window_enter_name.delete(0, END)
		update_window_enter_marks.delete(0, END)
	else:
		con = None
		try:
			rno = int(update_window_enter_rno.get())
			name = update_window_enter_name.get()
			marks = int(update_window_enter_marks.get())
			con = connect("C:\Python 3.9\Database\student.db")
			cursor = con.cursor()
			sql = "update student set name = '%s', marks = '%d' where rno = '%d'"
			cursor.execute(sql % (name, marks, rno))
			if cursor.rowcount > 0:
				con.commit()
				showinfo("Success", "Details updated successfully")
				update_window_enter_rno.delete(0, END)
				update_window_enter_name.delete(0, END)
				update_window_enter_marks.delete(0, END)
			else:
				showwarning("Error", "Record does not exist")
				update_window_enter_rno.delete(0, END)
				update_window_enter_name.delete(0, END)
				update_window_enter_marks.delete(0, END)
		except Exception as e:
			showerror("Error", e)
		finally:
			if con is not None:
					con.close()
		
#-------------------------------------------------------------------------------
def delete_student():
	con = None
	if (delete_window_enter_rno.get() == ""):
		showerror("Error", "Please enter roll number")
	elif ((delete_window_enter_rno.get()).isdigit() == False):
		showerror("Error", "Roll number can consist of integers only")
		delete_window_enter_rno.delete(0, END)
	elif (int(delete_window_enter_rno.get()) <= 0):
		showerror("Error", "Roll number can't be negative")
		delete_window_enter_rno.delete(0, END)
	else:
		try:
			con = connect("C:\Python 3.9\Database\student.db")
			cursor = con.cursor()
			rno = int(delete_window_enter_rno.get())
			sql = "delete from student where rno = '%d' "
			cursor.execute(sql % (rno))
			if cursor.rowcount > 0:
				con.commit()
				showinfo("Success", "Student deleted successfully :)")
				delete_window_enter_rno.delete(0, END)
			else:
				showerror("Failure", "Student does not exist")
				delete_window_enter_rno.delete(0, END)
		except Exception as e:
			showerror("Error", e)
			delete_window_enter_rno.delete(0, END)
		finally:
			if con is not None:
				con.close()
#-------------------------------------------------------------------------------
def show_graph():
	list_marks = []
	list_names = []	
	con=None
	try:
		con=connect('C:\Python 3.9\Database\student.db')
		cursor=con.cursor()
		sql="select marks from student"
		cursor.execute(sql)
		data=cursor.fetchall()
		# print(data)
		for d in data:	
			list_marks.append(int(str(d[0])))
			#print(list_marks)
	except Exception as e:
		showerror("OOPS!", e)
	finally:
		if con is not None:
			con.close()

	con=None
	try:
		con=connect('C:\Python 3.9\Database\student.db')
		cursor=con.cursor()
		sql="select name from student"
		cursor.execute(sql)
		data=cursor.fetchall()
		#print(data)
		for d in data:	
			list_names.append(str(d[0]))
		#print(list_names)
	except Exception as e:
		showerror("Error", e)
	finally:
		if con is not None:
			con.close()


	plt.bar(list_names, list_marks, width = 0.6, color = ['red', 'green', 'cyan', 'orange'])
	plt.title("Batch Information!")
	plt.xlabel("Students")
	plt.ylabel("Marks")

	plt.show()
#-------------------------------------------------------------------------------
master = Tk()
master.title("Student Management System")
master.geometry("900x600+400+25")
master.config(background = "#1DB9C3")
#master.resizable(0, 0)


label1 = Label(master)
label1.place(x = 0, y = 0)

main_window_add_btn = Button(master, text = 'Add', font = ('Arial', 20, 'bold'), width = 10, bg = '#C32BAD', fg = 'white', command = view_add_btn)
main_window_add_btn.pack(pady = 10)

main_window_view_btn = Button(master, text = 'View', font = ('Arial', 20, 'bold'), width = 10, bg = '#C32BAD', fg = 'white', command = view_view_btn)
main_window_view_btn.pack(pady = 10)

main_window_update_btn = Button(master, text = 'Update', font = ('Arial', 20, 'bold'), width = 10, bg = '#C32BAD', fg = 'white', command = view_update_btn)
main_window_update_btn.pack(pady = 10)

main_window_delete_btn = Button(master, text = 'Delete', font = ('Arial', 20, 'bold'), width = 10, bg = '#C32BAD', fg = 'white', command = view_delete_btn)
main_window_delete_btn.pack(pady = 10)

main_window_charts_btn = Button(master, text = 'Charts', font = ('Arial', 20, 'bold'), width = 10, bg = '#C32BAD', fg = 'white', command = show_graph)
main_window_charts_btn.pack(pady = 10)

main_window_location_lbl = Label(master, text = "Location : " + city, font = ('Arial', 18, 'bold'), fg = "dark blue",bg = "#1DB9C3")
main_window_location_lbl.place(x = 4, y = 400)

main_window_temperature_lbl = Label(master, text = "Temperature : " + str(temperature) + "\u00B0" + "C", font = ('Arial', 18, 'bold'), fg = "dark blue",bg = "#1DB9C3")
main_window_temperature_lbl.place(x = 4, y = 450)

sty = Style(master)
sty.configure("TSeparator", background="#C32BAD")

separator = ttk.Separator(master, orient = 'horizontal') 
separator.pack(fill = 'x', pady = 10)

separator = ttk.Separator(master, orient = 'horizontal') 
separator.pack(fill = 'x', pady = 90)

main_window_qotd_lbl = Label(master, text = "Quote : " + qotd, font = ('Arial', 18, 'bold'), fg = "dark blue",bg = "#1DB9C3", wraplength = 900)
main_window_qotd_lbl.place(x = 4, y = 501)

# main_window_qotd_lbl = Label(master, text = qotd , font = ('Arial', 18, 'bold'), fg = "dark blue",bg = "#1DB9C3", wraplength = 500)
# main_window_qotd_lbl.place(x = 94, y = 501)


# ---------------------------------------------------------------------------------------------------------------------------
def quit():
	if askokcancel("Quit", "Do you want to quit?"):
		master.destroy()	


master.protocol("WM_DELETE_WINDOW", quit)

#--------------------------------------------------------------------------------------------------------------------------------

add_window = Toplevel(master)
add_window.title("Add student")
add_window.geometry("500x600+400+25")
add_window.config(bg="#1DB9C3")

label2 = Label(add_window)
label2.place(x = 0, y = 0)

add_window_lbl_rno = Label(add_window, text = "Enter roll number", font = ('Arial', 20, 'bold'),bg = "#1DB9C3")
add_window_lbl_rno.pack(pady = 10)

add_window_enter_rno = Entry(add_window, bd = 5, font = ('Arial', 20, 'bold'))
add_window_enter_rno.pack(pady = 10)

add_window_lbl_name = Label(add_window, text = "Enter name", font = ('Arial', 20, 'bold'),bg = "#1DB9C3")
add_window_lbl_name.pack(pady = 10)

add_window_enter_name = Entry(add_window, bd = 5, font = ('Arial', 20, 'bold'))
add_window_enter_name.pack(pady = 10)

add_window_lbl_marks = Label(add_window, text = "Enter marks", font = ('Arial', 20, 'bold'),bg = "#1DB9C3")
add_window_lbl_marks.pack(pady = 10)

add_window_enter_marks = Entry(add_window, bd = 5, font = ('Arial', 20, 'bold'))
add_window_enter_marks.pack(pady = 10)

add_window_btn_save = Button(add_window, text = 'Save', borderwidth = 9, font = ('Arial', 20, 'bold'), width = 10, bg = '#C32BAD', fg = 'white', command = add_student)
add_window_btn_save.pack(pady = 10)

add_window_btn_back = Button(add_window, text = 'Back', borderwidth = 9, font = ('Arial', 20, 'bold'), width = 10, bg = '#C32BAD', fg = 'white', command = back_main_from_add)
add_window_btn_back.pack(pady = 10)

add_window.withdraw()

#---------------------------------------------------------------------------------------------------------------------------------

view_window = Toplevel(master)
view_window.title("View student")
view_window.geometry("500x600+400+25")

label3 = Label(view_window)
label3.place(x = 0, y = 0)

scrolled_text = ScrolledText(view_window, width = 40, height = 15, font = ("Arial", 16, "bold"))
scrolled_text.pack(pady = 10)

view_window_btn_back = Button(view_window, text = 'Back', borderwidth = 9, font = ('Arial', 20, 'bold'), width = 10, bg = '#C32BAD', fg = 'white', command = back_main_from_view)
view_window_btn_back.pack(pady = 10)

view_window.withdraw()

#----------------------------------------------------------------------------------------------------------------------------

update_window = Toplevel(master)
update_window.title("Update student")
update_window.geometry("500x600+400+25")
update_window.config(bg = "#1DB9C3")

label4 = Label(update_window)
label4.place(x = 0, y = 0)

update_window_lbl_rno = Label(update_window, text = "Enter roll number", font = ('Arial', 20, 'bold'),bg = "#1DB9C3")
update_window_lbl_rno.pack(pady = 10)

update_window_enter_rno = Entry(update_window, bd = 5, font = ('Arial', 20, 'bold'))
update_window_enter_rno.pack(pady = 10)

update_window_lbl_name = Label(update_window, text = "Enter name", font = ('Arial', 20, 'bold'),bg = "#1DB9C3")
update_window_lbl_name.pack(pady = 10)

update_window_enter_name = Entry(update_window, bd = 5, font = ('Arial', 20, 'bold'))
update_window_enter_name.pack(pady = 10)

update_window_lbl_marks = Label(update_window, text = "Enter marks", font = ('Arial', 20, 'bold'),bg = "#1DB9C3")
update_window_lbl_marks.pack(pady = 10)

update_window_enter_marks = Entry(update_window, bd = 5, font = ('Arial', 20, 'bold'))
update_window_enter_marks.pack(pady = 10)

update_window_btn_save = Button(update_window, text = 'Save', borderwidth = 9, font = ('Arial', 20, 'bold'), width = 10, bg = '#C32BAD', fg = 'white', command = update_student)
update_window_btn_save.pack(pady = 10)

update_window_btn_back = Button(update_window, text = 'Back', borderwidth = 9, font = ('Arial', 20, 'bold'), width = 10, bg = '#C32BAD', fg = 'white', command = back_main_from_update)
update_window_btn_back.pack(pady = 10)

update_window.withdraw()

# ---------------------------------------------------------------------------------------------------------------------------

delete_window = Toplevel(master)
delete_window.title("Delete student")
delete_window.geometry("500x600+400+25")
delete_window.config(bg = "#1DB9C3")

label5 = Label(delete_window)
label5.place(x = 0, y = 0)

delete_window_lbl_rno = Label(delete_window, text = "Enter roll number", font = ('Arial', 20, 'bold'),bg = "#1DB9C3")
delete_window_lbl_rno.pack(pady = 10)

delete_window_enter_rno = Entry(delete_window, bd = 5, font = ('Arial', 20, 'bold'))
delete_window_enter_rno.pack(pady = 10)

delete_window_btn_save = Button(delete_window, text = 'Save', borderwidth = 9, font = ('Arial', 20, 'bold'), width = 10, bg = '#C32BAD', fg = 'white', command = delete_student)
delete_window_btn_save.pack(pady = 10)

delete_window_btn_back = Button(delete_window, text = 'Back', borderwidth = 9, font = ('Arial', 20, 'bold'), width = 10, bg = '#C32BAD', fg = 'white', command = back_main_from_delete)
delete_window_btn_back.pack(pady = 10)

delete_window.withdraw()

master.mainloop()



