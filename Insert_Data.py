import mysql.connector
from random import choice
from datetime import datetime, timedelta

mydb = mysql.connector.connect(host="localhost", user="root", passwd="root")
cur = mydb.cursor()

def insert_data():
	person_details = open('person_details.txt', 'r')
	contact_details = open('contact_details.txt', 'r')
	address_details = open('address.txt', 'r')

	cur.execute("USE dbms_project")

	cmd = "INSERT INTO personal_details (name, age, coming_from, going_to)" \
		"VALUES (%s, %s, %s, %s)"

	for line in person_details.readlines():
		val = line.split(',')
		val[-1] = val[-1][0:-1]
		ins = (val[0], int(val[1]), val[3], val[4])
		cur.execute(cmd, ins)
		find_p_id = "SELECT P_id FROM personal_details WHERE name = %s AND age = %s AND coming_from = %s AND going_to = %s"
		cur.execute(find_p_id, (val[0], int(val[1]), val[3], val[4]))
		data = cur.fetchall()
		p_id = data[0][0]
		cmd2 = "INSERT INTO Dates(p_id, arrival_date, discharge_date) " \
			   "VALUES (%s, %s, %s)"
		date = datetime.strptime(val[2], "%Y-%m-%d").date()
		# print(str(date))
		cur.execute(cmd2, (p_id, date, date+timedelta(days=14)))

	cmd = "INSERT INTO contact_details (P_id, phone)" \
		"VALUES (%s, %s)"
	ins = []

	for line in contact_details.readlines():
		val = line.split(',')
		val[-1] = val[-1][0:-1]
		# p_id = 0
		find_p_id = "SELECT P_id FROM personal_details WHERE name = %s AND age = %s AND coming_from = %s AND going_to = %s"
		to_find = (val[0], val[1], val[2], val[3])
		cur.execute(find_p_id, to_find)
		data = cur.fetchall()
		p_id = data[0][0]
		# print(p_id)
		ins.append((p_id, int(val[4])))

	cur.executemany(cmd, ins)

	cmd = "INSERT INTO address (p_id, street_name, area, city, pincode, state, country)" \
		"VALUES (%s, %s, %s, %s, %s, %s, %s)"
	ins = []

	for line in address_details.readlines():
		val = line.split(',')
		val[-1] = val[-1][0:-1]
		# p_id = 0
		find_p_id = "SELECT P_id FROM personal_details WHERE name = %s AND age = %s AND coming_from = %s AND going_to = %s"
		to_find = (val[0], val[1], val[2], val[3])
		cur.execute(find_p_id, to_find)
		for t in cur: 
			for x in t: p_id = x
		ins.append((p_id, val[4], val[5], val[6], int(val[7]), val[8], val[9]))

	cur.executemany(cmd, ins)

	cmd = "INSERT INTO hostel_details (P_id, hostel_no, floor_no, room_no)" \
		"VALUES (%s, %s, %s, %s)"
	ins = []

	cur.execute("SELECT p_id, age FROM personal_details")

	grd_flr_room = [i for i in range(1000, 1100)]
	for i in range(2000, 2100):
		grd_flr_room.append(i)

	fir_flr_room = [i for i in range(1100, 1200)]
	for i in range(2100, 2200):
		fir_flr_room.append(i)

	sec_flr_room = [i for i in range(1200, 1250)]
	for i in range(2200, 2250):
		sec_flr_room.append(i)

	for t in cur:
		p_id, age = t[0], t[1]
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
		ins.append((p_id, hostel_no, floor_no, room_no%100))

	cur.executemany(cmd, ins)

	cmd = "CREATE TRIGGER ins_date " \
		   "AFTER INSERT " \
		   "ON address " \
		   "FOR EACH ROW " \
		   "INSERT INTO Dates(P_id, arrival_date, discharge_date) VALUES(NEW.P_id, CURDATE(), ADDDATE(CURDATE(), INTERVAL 14 DAY)) "

	cur.execute(cmd)

	mydb.commit()