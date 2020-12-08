import mysql.connector
from datetime import datetime, timedelta
from Create_Database import create_database
from Insert_Data import insert_data
import tkinter as tk
from tkinter import ttk, filedialog, Text
from tkinter import messagebox
from random import choice
from PIL import Image, ImageTk

resource_file = open("resources.txt", "r")
resource = {}
data = resource_file.readlines()
for lines in data:
	lines = list(lines.split())
	resource[lines[0]] = bool(int(lines[1]))

if resource["first_time"]:
	create_database()
	insert_data()
	resource_file.close()
	resource_file = open('resources.txt', 'w')
	resource_file.write('first_time 0')

mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="dbms_project")
cur = mydb.cursor()

grd_flr_room = [i for i in range(1000, 1100)]
for i in range(2000, 2100):
	grd_flr_room.append(i)

fir_flr_room = [i for i in range(1100, 1200)]
for i in range(2100, 2200):
	fir_flr_room.append(i)

sec_flr_room = [i for i in range(1200, 1250)]
for i in range(2200, 2250):
	sec_flr_room.append(i)

cur.execute("select discharge_date, room_no, floor_no, hostel_no from personal_details p, hostel_details h, dates d WHERE p.p_id = h.p_id AND p.p_id = d.p_id")
for p in cur:
	date, room, f_no, h_no = p[0], int(p[1]), int(p[2]), int(p[3])
	today = datetime.now().date()
	room = room + f_no*100 + h_no*1000
	if date > today:
		if f_no == 0:   grd_flr_room.remove(room)
		elif f_no == 1: fir_flr_room.remove(room)
		else: sec_flr_room.remove(room)

cur.close()
mydb.close()

class DatabaseView:
	def __init__(self, data):
		self.databaseViewWindow = tk.Tk()
		self.databaseViewWindow.wm_title("Database View")

		# Label widgets
		tk.Label(self.databaseViewWindow, text = "Database View Window",  width = 25).grid(pady = 5, column = 1, row = 1)

		self.databaseView = ttk.Treeview(self.databaseViewWindow)
		self.databaseView.grid(pady = 5, column = 1, row = 2)
		self.databaseView["show"] = "headings"
		self.databaseView["columns"] = ("p_id", "name", "age", "arrival_date", "discharge_date", "coming_from", "going_to", "phone", "street_name", "area", "city", "pincode", "state", "country", "hostel_no", "floor_no", "room_no")

		# Treeview column headings
		self.databaseView.heading("p_id", text = "Patient ID")
		self.databaseView.heading("name", text = "Name")
		self.databaseView.heading("age", text = "Age")
		self.databaseView.heading("arrival_date", text = "Arrival Date")
		self.databaseView.heading("discharge_date", text = "Discharge Date")
		self.databaseView.heading("coming_from", text = "Coming From")
		self.databaseView.heading("going_to", text = "Going To")
		self.databaseView.heading("phone", text = "Phone Number")
		self.databaseView.heading("street_name", text = "Street Name")
		self.databaseView.heading("area", text = "Area")
		self.databaseView.heading("city", text = "City")
		self.databaseView.heading("pincode", text = "Pincode")
		self.databaseView.heading("state", text = "State")
		self.databaseView.heading("country", text = "Country")
		self.databaseView.heading("hostel_no", text = "Hostel No")
		self.databaseView.heading("floor_no", text = "Floor")
		self.databaseView.heading("room_no", text = "Room No")

		# Treeview columns
		self.databaseView.column("p_id", width = 40)
		self.databaseView.column("name", width = 100)
		self.databaseView.column("age", width = 40)
		self.databaseView.column("arrival_date", width = 70)
		self.databaseView.column("discharge_date", width = 70)
		self.databaseView.column("coming_from", width = 90)
		self.databaseView.column("going_to", width = 90)
		self.databaseView.column("phone", width = 70)
		self.databaseView.column("street_name", width = 100)
		self.databaseView.column("area", width = 100)
		self.databaseView.column("city", width = 100)
		self.databaseView.column("pincode", width = 50)
		self.databaseView.column("state", width = 80)
		self.databaseView.column("country", width = 60)
		self.databaseView.column("hostel_no", width = 40)
		self.databaseView.column("floor_no", width = 40)
		self.databaseView.column("room_no", width = 40)

		for x in data:
			self.databaseView.insert('', 'end', values=x)

		self.databaseViewWindow.mainloop()

class InsertWindow:
	def __init__(self):

		top = tk.Tk()
		top.title('Insert')

		self.mydb = mysql.connector.connect(host='localhost', user="root", password="root", database='dbms_project')
		self.cur = self.mydb.cursor()

		# canvas and frame
		canvas = tk.Canvas(top, height=435, width=730, bg='#263D42')
		canvas.pack()
		frame = tk.Frame(canvas, bg="white")
		frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

		# Initializing all the variables
		self.name = tk.StringVar()
		self.age = tk.IntVar()
		self.coming_from = tk.StringVar()
		self.going_to = tk.StringVar()
		self.street_name = tk.StringVar()
		self.area = tk.StringVar()
		self.city = tk.StringVar()
		self.pincode = tk.IntVar()
		self.state = tk.StringVar()
		self.country = tk.StringVar()
		self.phone_no = tk.StringVar()

		# -------main--------
		# Boxes
		personal_box = tk.LabelFrame(
			frame, text='Personal Details', bg='white', font='Helvetica 11')
		personal_box.grid(padx=10, pady=10)

		address_box = tk.LabelFrame(
			frame, text='Address Details', bg='white', font='Helvetica 11')
		address_box.grid(row=1, column=0, padx=10, sticky=tk.W, rowspan=3)

		travel_box = tk.LabelFrame(
			frame, text='Travelling Details', bg='white', font='Helvetica 11')
		travel_box.grid(row=0, column=1, columnspan=4, padx=10, pady=20, sticky=tk.N)

		contact_box = tk.LabelFrame(
			frame, text='Contact Details', bg='white', font='Helvetica 11')
		contact_box.grid(row=1, column=1, rowspan=2, padx=10, pady=10, sticky=tk.N)

		btn_box = tk.LabelFrame(
			frame, text='', bg='white', font='Helvetica 11', bd='1')
		btn_box.grid(row=3, column=1, padx=10, pady=10, sticky=tk.S)


		# labels------------------------
		personal_labels = ['Name :', 'Age :']
		address_labels = ['Street :', 'Area :', 'City :',
						  'State :', 'Country :', 'Pin Code :']
		travel_labels = ['From ', 'To']

		# personal label
		for i in range(len(personal_labels)):
			cur_label = tk.Label(personal_box, text=personal_labels[i], bg='white')
			cur_label.grid(row=i, padx=10, pady=10, sticky=tk.E)

		# address labels
		for i in range(len(address_labels)):
			cur_label = tk.Label(address_box, text=address_labels[i], bg='white')
			cur_label.grid(row=i, padx=10, pady=5, sticky=tk.E)

		# travel labels
		for i in range(len(travel_labels)):
			cur_label = tk.Label(travel_box, text=travel_labels[i], bg='white')
			cur_label.grid(row=0, column=i, padx=10)

		phn_label = tk.Label(contact_box, text='Phone No.', bg='white')

		# personal entry
		self.nameEntry = tk.Entry(personal_box, width=18, bg='#F0F0F0', textvariable=self.name)
		self.ageEntry = tk.Entry(personal_box, width=18, bg='#F0F0F0', textvariable=self.age)

		# address enrty
		self.street_nameEntry = tk.Entry(address_box, width=24, bg='#F0F0F0', textvariable=self.street_name)
		self.areaEntry = tk.Entry(address_box, width=24, bg='#F0F0F0', textvariable=self.area)
		self.cityEntry = tk.Entry(address_box, width=24, bg='#F0F0F0', textvariable=self.city)
		self.stateEntry = tk.Entry(address_box, width=24, bg='#F0F0F0', textvariable=self.state)
		self.countryEntry = tk.Entry(address_box, width=24, bg='#F0F0F0', textvariable=self.country)
		self.pincodeEntry = tk.Entry(address_box, width=24, bg='#F0F0F0', textvariable=self.pincode)

		# travel entry
		self.coming_fromEntry = tk.Entry(travel_box, width=20, bg='#F0F0F0', textvariable=self.coming_from)
		self.going_toEntry = tk.Entry(travel_box, width=20, bg='#F0F0F0', textvariable=self.going_to)

		self.phone_noEntry = tk.Entry(contact_box, width=40, bg='#F0F0F0', textvariable=self.phone_no)

		self.nameEntry.grid(row=0, column=1, padx=10, pady=5)
		self.ageEntry.grid(row=1, column=1, padx=10, pady=5)

		self.street_nameEntry.grid(row=0, column=1, padx=10, pady=5)
		self.areaEntry.grid(row=1, column=1, padx=10, pady=5)
		self.cityEntry.grid(row=2, column=1, padx=10, pady=5)
		self.stateEntry.grid(row=3, column=1, padx=10, pady=5)
		self.countryEntry.grid(row=4, column=1, padx=10, pady=5)
		self.pincodeEntry.grid(row=5, column=1, padx=10, pady=5)

		self.coming_fromEntry.grid(row=1, column=0, padx=10, pady=10)
		self.going_toEntry.grid(row=1, column=1, padx=10, pady=10)


		# buttons----------------------
		add_btn = tk.Button(btn_box, text='Insert', command=self.Insert)
		reset_btn = tk.Button(btn_box, text='Reset', command=self.Reset)
		cancel_btn = tk.Button(btn_box, text="Close", command=top.destroy)

		phn_label.grid(row=1, column=1, padx=10, sticky=tk.N)
		self.phone_noEntry.grid(row=2, column=1, padx=10, sticky=tk.N, pady=10)
		add_btn.grid(row=0, column=0, padx=10, ipadx=10, pady=10)
		reset_btn.grid(row=0, column=1, padx=10, ipadx=10)
		cancel_btn.grid(row=0, column=2, padx=10, ipadx=10)

		top.mainloop()

	def __del__(self):
		self.cur.close()
		self.mydb.close()

	def Insert(self):
		cmd = "INSERT INTO personal_details(name, age, coming_from, going_to) " \
			  "VALUES (%s, %s, %s, %s)"
		ins = (self.nameEntry.get(), self.ageEntry.get(), self.coming_fromEntry.get(), self.going_toEntry.get())
		self.cur.execute(cmd, ins)

		cmd = "SELECT p_id FROM personal_details WHERE name = %s AND age = %s AND coming_from = %s AND going_to = %s"
		self.cur.execute(cmd, (self.nameEntry.get(), self.ageEntry.get(), self.coming_fromEntry.get(), self.going_toEntry.get()))
		data = self.cur.fetchall()
		print(data)
		p_id = data[0][0]

		cmd = "INSERT INTO address(p_id, street_name, area, city, pincode, state, country) " \
			  "VALUES (%s, %s, %s, %s, %s, %s, %s)"
		ins = (p_id, self.street_nameEntry.get(), self.areaEntry.get(), self.cityEntry.get(), self.pincodeEntry.get(), self.stateEntry.get(), self.countryEntry.get())
		self.cur.execute(cmd, ins)

		phones = self.phone_noEntry.get().split(',')
		cmd = "INSERT INTO contact_details(p_id, phone) VALUES (%s, %s)"
		ins = [(p_id, p) for p in phones]
		self.cur.executemany(cmd, ins)

		self.mydb.commit()

		self.AssignRoom(p_id, self.ageEntry.get())

	def AssignRoom(self, p_id, age):
		global grd_flr_room, fir_flr_room, sec_flr_room
		root = tk.Tk()
		age = int(age)
		root.title('Assigned')

		cmd = "INSERT INTO hostel_details(p_id, hostel_no, floor_no, room_no)" \
			  "VALUES (%s, %s, %s, %s)"

		if age >= 60:
			room_no = choice(grd_flr_room)
			grd_flr_room.remove(room_no)
		elif age >= 40:
			room_no = choice(fir_flr_room)
			fir_flr_room.remove(room_no)
		else:
			room_no = choice(sec_flr_room)
			sec_flr_room.remove(room_no)
		floor_no = (room_no//100)%10
		hostel_no = (room_no//1000)

		self.cur.execute(cmd, (p_id, hostel_no, floor_no, room_no%100))

		self.mydb.commit()

		if floor_no == 0:   floor = "Ground"
		elif floor_no == 1: floor = "First"
		else:               floor = "Second"
		tk.Label(root, width=50, text=f"Room Number : {room_no}").grid(pady=15, padx=2, column = 0, row = 0)
		tk.Label(root, width=50, text=f"Floor : {floor} Floor").grid(pady=10, padx=2, column = 0, row = 1)
		tk.Label(root, width=50, text=f"Hostel Number : {hostel_no}").grid(pady=10, padx=2, column = 0, row = 2)
		tk.Button(root, width = 20, text = "OK", command = root.destroy).grid(pady = 15, padx = 5, column = 0, row = 3)

		root.mainloop()

	def Reset(self):
		self.nameEntry.delete(0, tk.END)
		self.ageEntry.delete(0, tk.END)
		self.coming_fromEntry.delete(0, tk.END)
		self.going_toEntry.delete(0, tk.END)
		self.street_nameEntry.delete(0, tk.END)
		self.areaEntry.delete(0, tk.END)
		self.cityEntry.delete(0, tk.END)
		self.pincodeEntry.delete(0, tk.END)
		self.stateEntry.delete(0, tk.END)
		self.countryEntry.delete(0, tk.END)
		self.phone_noEntry.delete(0, tk.END)

class SearchWindow:
	def __init__(self):
		self.window = tk.Tk()
		self.window.title('Search')
		self.window.geometry('250x200')
		self.p_id = tk.IntVar()
		self.name = tk.StringVar()

		tk.Label(self.window, text='Search data using these values').grid(pady=15, padx=30, columnspan=3, row=0)
		tk.Label(self.window, text="Patient ID ").grid(pady=10, padx=5, column=0, row = 1)
		tk.Label(self.window, text="Name ").grid(pady=10, padx=5, column=0, row = 2)

		p_idEntry = tk.Entry(self.window, width = 20, textvariable=self.p_id)
		nameEntry = tk.Entry(self.window, width = 20, textvariable = self.name)

		p_idEntry.grid(column=1, row = 1)
		nameEntry.grid(column=1, row = 2)

		def submitAction():
			p_id = p_idEntry.get()
			name = nameEntry.get()

			cmd = "SELECT p.p_id, name, age, arrival_date, discharge_date, coming_from, going_to, phone, street_name, area, city, pincode, state, country, hostel_no, floor_no, room_no " \
			    "FROM personal_details p, address a, hostel_details h, contact_details c, dates d " \
			    "WHERE a.p_id = p.p_id AND p.p_id = h.p_id AND p.p_id = c.p_id AND p.p_id = d.p_id AND (p.p_id = %s OR name = %s)"

			mydb = mysql.connector.connect(host='localhost', user='root', passwd='root', database='dbms_project')
			cur = mydb.cursor()
			cur.execute(cmd, (p_id, name, ))
			DatabaseView(cur)
			cur.close()
			mydb.close()

		submitButton = tk.Button(self.window, text='Search', width=28, command=submitAction)
		submitButton.grid(pady=20, padx=20, columnspan=3, row=4)

		self.window.mainloop()

class DeleteWindow:
	def __init__(self):
		self.window = tk.Tk()
		self.window.title('Delete')
		self.p_id = tk.IntVar()

		tk.Label(self.window, text="Patient ID ").grid(pady=10, padx=5, column=0, row = 0)
		p_idEntry = tk.Entry(self.window, width = 20, textvariable=self.p_id)

		p_idEntry.grid(column=1, row = 0)

		def submitAction():
			p_id = p_idEntry.get()
			cmd = "DELETE FROM personal_details WHERE p_id = %s"

			mydb = mysql.connector.connect(host='localhost', user='root', passwd='root', database='dbms_project')
			cur = mydb.cursor()
			cur.execute(cmd, (p_id, ))

			mydb.commit()
			messagebox.showinfo('Result', "Delete Successful")

			cur.close()
			mydb.close()

		submitButton = tk.Button(self.window, text='Delete', width=28, command=submitAction)
		submitButton.grid(pady=20, padx=20, columnspan=2, row=1)

		self.window.mainloop()

class UpdateWindow:
	def __init__(self):
		window = tk.Tk()
		window.title('Update Data')
		self.mydb = mysql.connector.connect(host='localhost', user="root", password="root", database='dbms_project')
		self.cur = self.mydb.cursor()
		self.p_id = tk.IntVar()

		tk.Label(window, text='Enter Patient ID to Update his/her information').grid(padx=5, pady=15, columnspan=2, row=0)
		tk.Label(window, text='Patient ID').grid(pady=5, padx=5, column=0, row=1)
		self.p_idEntry = tk.Entry(window, width=15, textvariable=self.p_id)
		self.p_idEntry.grid(column=1, row=1)

		submitButton = tk.Button(window, text='Enter Details', width=15, command=self.submitAction)
		submitButton.grid(columnspan=2, row=2, padx=5, pady=20)

		window.mainloop()

	def __del__(self):
		self.cur.close()
		self.mydb.close()

	def submitAction(self):

		self.cur.execute("SELECT COUNT(p_id) FROM personal_details WHERE p_id = %s", (self.p_idEntry.get(),))
		data = self.cur.fetchall()
		if data[0][0] == 0:
			messagebox.showerror('Not Found', 'There is no information in the database')
			return

		window = tk.Tk()
		window.title("Update data")

		cmd = "SELECT name, age, coming_from, going_to, street_name, area, city, pincode, state, country, phone " \
			  "FROM personal_details p, address a, hostel_details h, contact_details c, dates d " \
			  "WHERE a.p_id = p.p_id AND p.p_id = h.p_id AND p.p_id = c.p_id AND p.p_id = %s AND p.p_id = d.p_id"

		self.cur.execute(cmd, (self.p_idEntry.get(),))
		data = self.cur.fetchone()
		# print(data)
		self.cur.fetchall()

		# canvas and frame
		canvas = tk.Canvas(window, height=485, width=730, bg='#263D42')
		canvas.pack()
		frame = tk.Frame(canvas, bg="white")
		frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

		# Initializing all the variables
		name = tk.StringVar(window, value=data[0])
		age = tk.IntVar(window, value=data[1])
		coming_from = tk.StringVar(window, value=data[2])
		going_to = tk.StringVar(window, value=data[3])
		street_name = tk.StringVar(window, value=data[4])
		area = tk.StringVar(window, value=data[5])
		city = tk.StringVar(window, value=data[6])
		pincode = tk.IntVar(window, value=data[7])
		state = tk.StringVar(window, value=data[8])
		country = tk.StringVar(window, value=data[9])
		phone_no = tk.StringVar(window, value=data[10])

		# -------main--------
		# Boxes
		personal_box = tk.LabelFrame(
			frame, text='Personal Details', bg='white', font='Helvetica 11')
		personal_box.grid(padx=10, pady=10)

		address_box = tk.LabelFrame(
			frame, text='Address Details', bg='white', font='Helvetica 11')
		address_box.grid(row=1, column=0, padx=10, sticky=tk.W, rowspan=3)

		travel_box = tk.LabelFrame(
			frame, text='Travelling Details', bg='white', font='Helvetica 11')
		travel_box.grid(row=0, column=1, columnspan=4, padx=10, pady=20, sticky=tk.N)

		contact_box = tk.LabelFrame(
			frame, text='Contact Details', bg='white', font='Helvetica 11')
		contact_box.grid(row=1, column=1, rowspan=2, padx=10, pady=10, sticky=tk.N)

		btn_box = tk.LabelFrame(
			frame, text='', bg='white', font='Helvetica 11', bd='1')
		btn_box.grid(row=3, column=1, padx=10, pady=10, sticky=tk.S)

		# labels------------------------
		personal_labels = ['Name :', 'Age :']
		address_labels = ['Street :', 'Area :', 'City :',
						  'State :', 'Country :', 'Pin Code :']
		travel_labels = ['From ', 'To']

		# personal label
		for i in range(len(personal_labels)):
			cur_label = tk.Label(personal_box, text=personal_labels[i], bg='white')
			cur_label.grid(row=i, padx=10, pady=10, sticky=tk.E)

		# address labels
		for i in range(len(address_labels)):
			cur_label = tk.Label(address_box, text=address_labels[i], bg='white')
			cur_label.grid(row=i, padx=10, pady=5, sticky=tk.E)

		# travel labels
		for i in range(len(travel_labels)):
			cur_label = tk.Label(travel_box, text=travel_labels[i], bg='white')
			cur_label.grid(row=0, column=i, padx=10)

		phn_label = tk.Label(contact_box, text='Phone No.', bg='white')

		# personal entry
		nameEntry = tk.Entry(personal_box, width=18, bg='#F0F0F0', textvariable=name)
		ageEntry = tk.Entry(personal_box, width=18, bg='#F0F0F0', textvariable=age)

		# address enrty
		street_nameEntry = tk.Entry(address_box, width=24, bg='#F0F0F0', textvariable=street_name)
		areaEntry = tk.Entry(address_box, width=24, bg='#F0F0F0', textvariable=area)
		cityEntry = tk.Entry(address_box, width=24, bg='#F0F0F0', textvariable=city)
		stateEntry = tk.Entry(address_box, width=24, bg='#F0F0F0', textvariable=state)
		countryEntry = tk.Entry(address_box, width=24, bg='#F0F0F0', textvariable=country)
		pincodeEntry = tk.Entry(address_box, width=24, bg='#F0F0F0', textvariable=pincode)

		# travel entry
		coming_fromEntry = tk.Entry(travel_box, width=20, bg='#F0F0F0', textvariable=coming_from)
		going_toEntry = tk.Entry(travel_box, width=20, bg='#F0F0F0', textvariable=going_to)

		phone_noEntry = tk.Entry(contact_box, width=40, bg='#F0F0F0', textvariable=phone_no)

		nameEntry.grid(row=0, column=1, padx=10, pady=5)
		ageEntry.grid(row=1, column=1, padx=10, pady=5)

		street_nameEntry.grid(row=0, column=1, padx=10, pady=5)
		areaEntry.grid(row=1, column=1, padx=10, pady=5)
		cityEntry.grid(row=2, column=1, padx=10, pady=5)
		stateEntry.grid(row=3, column=1, padx=10, pady=5)
		countryEntry.grid(row=4, column=1, padx=10, pady=5)
		pincodeEntry.grid(row=5, column=1, padx=10, pady=5)

		coming_fromEntry.grid(row=1, column=0, padx=10, pady=10)
		going_toEntry.grid(row=1, column=1, padx=10, pady=10)

		phn_label.grid(row=1, column=1, padx=10, sticky=tk.N)
		phone_noEntry.grid(row=2, column=1, padx=10, sticky=tk.N, pady=10)

		# Button widgets

		def Update():
			cmd = "UPDATE personal_details SET name = %s, age = %s, coming_from = %s, going_to = %s " \
				  "WHERE p_id = %s"
			ins = (nameEntry.get(), ageEntry.get(), coming_fromEntry.get(), going_toEntry.get(), self.p_idEntry.get(), )
			self.cur.execute(cmd, ins)

			p_id = self.p_idEntry.get()

			cmd = "UPDATE address SET street_name = %s, area = %s, city = %s, pincode = %s, state = %s, country = %s " \
				  "WHERE p_id = %s"
			ins = (street_nameEntry.get(), areaEntry.get(), cityEntry.get(), pincodeEntry.get(), stateEntry.get(), countryEntry.get(), p_id, )
			self.cur.execute(cmd, ins)

			cmd = "UPDATE contact_details SET phone = %s WHERE p_id = %s AND phone = %s"
			ins = (phone_noEntry.get(), p_id, data[10], )
			self.cur.execute(cmd, ins)
			messagebox.showinfo('Result', 'Update Successful')

			self.mydb.commit()

			window.destroy()

		def Reset():
			nameEntry.delete(0, tk.END)
			ageEntry.delete(0, tk.END)
			coming_fromEntry.delete(0, tk.END)
			going_toEntry.delete(0, tk.END)
			street_nameEntry.delete(0, tk.END)
			areaEntry.delete(0, tk.END)
			cityEntry.delete(0, tk.END)
			pincodeEntry.delete(0, tk.END)
			stateEntry.delete(0, tk.END)
			countryEntry.delete(0, tk.END)
			phone_noEntry.delete(0, tk.END)

		# buttons----------------------
		add_btn = tk.Button(btn_box, text='Update', command=Update)
		reset_btn = tk.Button(btn_box, text='Reset', command=Reset)
		cancel_btn = tk.Button(btn_box, text="Close", command=window.destroy)

		add_btn.grid(row=0, column=0, padx=10, ipadx=10, pady=10)
		reset_btn.grid(row=0, column=1, padx=10, ipadx=10)
		cancel_btn.grid(row=0, column=2, padx=10, ipadx=10)

		window.mainloop()

class HomePage:
	def __init__(self):
		root = tk.Tk()
		root.title('NIT Silchar Quarantine Center')

		# canvas and frame
		canvas = tk.Canvas(root, height=400, width=700, bg='#263D42')
		canvas.pack()
		frame = tk.Frame(canvas, bg="white")
		frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

		# Home image
		image = Image.open('DBMS_logo.png')
		resized = image.resize((300, 225), Image.ANTIALIAS)
		wall = ImageTk.PhotoImage(resized)

		# // styles for buttons
		style = ttk.Style()
		style.map("C.TButton",
				  foreground=[('pressed', 'red'), ('active', 'blue')],
				  background=[('pressed', '!disabled', 'black'), ('active', 'white')]
				  )

		# Labels-----------
		wall_box = tk.Label(frame, image=wall, bd='0')
		btn_box = tk.LabelFrame(frame, text='Choose the Operation', fg='#213B42', bd='0', font='Helvetica 13')

		# buttons
		insert_btn = ttk.Button(btn_box, text='Insert', style='C.TButton', command=self.Insert)
		update_btn = ttk.Button(btn_box, text='Update', style='C.TButton', command=self.Update)
		search_btn = ttk.Button(btn_box, text='Search', style='C.TButton', command=self.Search)
		delete_btn = ttk.Button(btn_box, text='Delete', style='C.TButton', command=self.Delete)
		display_btn = ttk.Button(btn_box, text='Display', style='C.TButton', command=self.Display)
		exit_btn = ttk.Button(btn_box, text='Exit', style='C.TButton', command=root.destroy)

		# //layouts-----------------
		wall_box.pack(side=(tk.LEFT), fill=tk.X, padx=10)
		btn_box.pack(side=(tk.RIGHT), fill=tk.X, padx=15, ipadx=10)

		insert_btn.pack(padx=10, pady=10, ipadx=10)
		update_btn.pack(padx=10, pady=10, ipadx=10)
		search_btn.pack(padx=10, pady=10, ipadx=10)
		delete_btn.pack(padx=10, pady=10, ipadx=10)
		display_btn.pack(padx=10, pady=10, ipadx=10)
		exit_btn.pack(padx=10, pady=10, ipadx=10)

		root.mainloop()

	def Insert(self):
		insert = InsertWindow()

	def Update(self):
		update = UpdateWindow()

	def Search(self):
		search = SearchWindow()

	def Delete(self):
		delete = DeleteWindow()

	def Display(self):
		mydb = mysql.connector.connect(host='localhost', user='root', passwd='root', database='dbms_project')
		cur = mydb.cursor()
		cmd = "SELECT p.p_id, name, age, arrival_date, discharge_date, coming_from, going_to, phone, street_name, area, city, pincode, state, country, hostel_no, floor_no, room_no " \
			  "FROM personal_details p, address a, hostel_details h, contact_details c, dates d " \
			  "WHERE a.p_id = p.p_id AND p.p_id = h.p_id AND p.p_id = c.p_id AND p.p_id = d.p_id"
		cur.execute(cmd)
		data = cur.fetchall()
		DatabaseView(data)
		cur.close()
		mydb.close()

homepage = HomePage()
