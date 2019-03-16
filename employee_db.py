import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
from .api_data import api_data


# todays date and time
now = datetime.now()
date_now = now.strftime("%Y-%m-%d")
time_now = now.strftime("%H:%M:%S")
time_now1 = now.strftime("%H:%M:%S %p")
print("Today's Date: ", date_now)
print("Current Time: ", time_now)
print('\n')

# ofiice time
office_start = '10:00:00'
office_end = '06:00:00'

# time format
FMT = '%H:%M:%S'

# connect to the db
try:
    conn = psycopg2.connect("dbname='datahead' user='postgres' host='localhost' password='datahead'")
except:
    print("I am unable to connect to the database")

# cursor
cur = conn.cursor()


# data insert into database
def insert_data_into_db():
    insert_query = "INSERT INTO employee (id, name, log_date, log_time, login, logout) VALUES %s \
                   ON CONFLICT (id) DO UPDATE \
                   SET name = excluded.name, log_date = excluded.log_date, log_time = excluded.log_time,\
                   login = excluded.login, logout = excluded.logout"

    execute_values(cur, insert_query, api_data())
    conn.commit()

    # execute query
    cur.execute("Select id, name, log_date, log_time, login, logout, current_out_time, total_out_time_day, "
                "total_out_time_month, count_total_out_number, absent_name from employee")
    db_data = cur.fetchall()
    return db_data


# update data insert
for id, name, log_date, log_time, login, logout, current_out_time, total_out_time_day,\
        total_out_time_month, count_total_out_number, absent_name  in insert_data_into_db():
    if id and log_date and log_time:
        log_time = str(log_time)
        employee_enter_time = datetime.strptime(log_time, FMT) - datetime.strptime(office_start, FMT)
        if logout:
            if login:
                current_out_time = datetime.strptime(str(login), FMT) - datetime.strptime(str(logout), FMT)
                count = 0
                count = count + 1
                cur.execute("UPDATE employee SET (current_out_time, count_total_out_number) = ('{}', {}) where id={}".format(current_out_time, count, id))
                conn.commit()
                print(id, current_out_time)

    elif id:
        print("Absent Today",id, name)
        cur.execute("UPDATE employee SET absent_name = '{}' where id={}".format(name, id))
        conn.commit()



# employes all data
history = []
for i in insert_data_into_db():
    history.append(list(i))


cur.execute("SELECT COUNT(absent_name) FROM employee;")
absent_name_count = cur.fetchall()
cur.execute("SELECT COUNT(logout) FROM employee;")
logout_count = cur.fetchall()
cur.execute("SELECT COUNT(login) FROM employee;")
login_count_data = cur.fetchall()
cur.execute("SELECT COUNT(name) FROM employee;")
all_employee = cur.fetchall()
# login count data
for i in login_count_data:
    print("Login Count:",i[0])
    login_count = i[0]
# total employee
for i in all_employee:
    print("All Employee Count:",i[0])
    total_employee = i[0]
print(absent_name_count)
# absent and out count
for i in absent_name_count:
    print("Absent name Count:",i[0])
    absent_count = i[0]
    absent = (absent_count / 100) * total_employee
    active_count = total_employee - i[0]
    active = (active_count / 100) * total_employee

# logout count
for i in logout_count:
    print("Total Logout Count:",i[0])
    total_out_count = i[0]
    out_count = total_out_count - login_count
    out = (out_count / 100) * total_employee
    # still out employee
    print("Still Out",out_count)


# close the cursor
cur.close()

# close the connection
conn.close()