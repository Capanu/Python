import mysql.connector


def init_connection():
    my_db = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="example")

    if my_db:
        print("Connection Succescfull!")
    else:
        print("Connection NOT Succescfull!")

    cursor = my_db.cursor()
    ok = False

    cursor.execute("SHOW Tables")
    for elem in cursor:
        if 'employees' == elem[0]:
            ok = True
            break

    if ok:
        print("The table exist!")
    else:
        cursor.execute("""create table employees(
        first_name VARCHAR(32) not null,
        last_name VARCHAR(32) not null,
        age numeric(3) not null,
        job VARCHAR(32) not null,
        gender VARCHAR(10) not null,
        salary numeric(15) not null,
        hire_date date not null);
        """)
    return my_db


def add_emp_in_db(tuple_values, my_db):
    my_cursor = my_db.cursor()
    sql_comm = "insert into employees values"+str(tuple_values)+";"
    my_cursor.execute(sql_comm)
    my_db.commit()
    my_cursor.close()


def delete_emp_from_db(first_name, last_name, my_db):
    my_cursor = my_db.cursor()
    sql_comm = "DELETE FROM employees where first_name=" + "'" + str(first_name)+"'" + " and last_name="+"'" \
               + str(last_name)+"'"+";"
    my_cursor.execute(sql_comm)
    my_db.commit()
    my_cursor.close()


def update_emp_in_bd(my_db, first_name, last_name, age, job, gender, salary, old_first_name, old_last_name):
    starter = "update employees set "
    first_name_str = "first_name="+"'" + first_name + "'"
    last_name_str = "last_name=" + "'" + last_name+ "'"
    age_str = "age=" + age
    job_str = "job=" + "'" + job+ "'"
    gender_str = "gender=" + "'" + gender+ "'"
    salary_str = "salary=" + salary
    sql_comm = starter + first_name_str + "," + last_name_str + "," + age_str + "," + job_str + "," + gender_str + "," \
               + salary_str + " where " + 'first_name='+"'"+old_first_name+"'" \
               + " and last_name=" + "'" + old_last_name+"'" + ";"

    my_cursor = my_db.cursor()
    my_cursor.execute(sql_comm)
    my_db.commit()
    my_cursor.close()