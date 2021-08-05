from tkinter import *
from tkinter import ttk
from PIL import ImageTk
from PIL import Image
from api_db.op_api import *
from tkinter import messagebox
import datetime
from tkinter.filedialog import asksaveasfile
import csv
import matplotlib.pyplot as drawer


def disable_close():
    return None


# initialize db connection and windows of app
my_db = init_connection()
root_page = Tk()
employee_page = Toplevel()
employees_page = Toplevel()

# hide pages
employee_page.withdraw()
employees_page.withdraw()

# disable x from right up corner
employee_page.protocol("WM_DELETE_WINDOW", disable_close)
employees_page.protocol("WM_DELETE_WINDOW", disable_close)

# initialize logo for root page
logo_root_img = Image.open("logo.png")
logo_root_img = logo_root_img.resize((300, 230))
logo_root_img = ImageTk.PhotoImage(logo_root_img)

# initialize logo for man page
emp_img_man = Image.open("emp_img.png")
emp_img_man = emp_img_man.resize((250, 200))
emp_img_man = ImageTk.PhotoImage(emp_img_man)

# initialize logo for woman page
emp_emp_female = Image.open("emp_img_f.png")
emp_emp_female = emp_emp_female.resize((250, 200))
emp_emp_female = ImageTk.PhotoImage(emp_emp_female)

# first_last_dict_names is used  to maintain the uniqueness of first_name, last_name couple
first_last_dict_names = {}

# is a list used to  retain the credentials of employee that is logged in
employee_person_logged_in = []

# detached_rows is used to retain  rows  of table that are hidden on search process
detached_rows = []

# retain the number of employees per job from database, used for statistics
nr_emp_per_job = {}

# it is used to retain the first selected emp from table on pushing select button
selected_first_emp = None


def update_emp_page(page):
    showed_img = None

    # extract credentials for logged in employee
    first_name_emp = employee_person_logged_in[0]
    last_name_emp = employee_person_logged_in[1]
    age_emp = employee_person_logged_in[2]
    job_emp = employee_person_logged_in[3]
    gender_emp = employee_person_logged_in[4]
    salary_emp = employee_person_logged_in[5]
    created_date_emp = employee_person_logged_in[6]

    if gender_emp == 'male':
        showed_img = emp_img_man
    elif gender_emp == 'female':
        showed_img = emp_emp_female

    img_lbl = Label(page, image=showed_img)
    first_name_lbl = Label(page, text=first_name_emp, font=("Segoe UI Black", 12),bg="#ff6666", fg = "#333300")
    last_name_lbl = Label(page, text=last_name_emp,  font=("Segoe UI Black", 12), bg="#ff6666", fg = "#333300")
    age_lbl = Label(page, text=age_emp, font=("Segoe UI Black", 12),  bg="#ff6666", fg = "#333300")
    job_lbl = Label(page, text=job_emp, font=("Segoe UI Black", 12),  bg="#ff6666",fg = "#333300")
    gender_lbl = Label(page, text=gender_emp, font=("Segoe UI Black", 12),  bg="#ff6666", fg = "#333300")
    salary_lbl = Label(page, text=salary_emp, font=("Segoe UI Black", 12),  bg="#ff6666", fg = "#333300")
    date_created_lbl = Label(page, text=created_date_emp,  bg="#ff6666", fg = "#333300", font=("Segoe UI Black", 12))

    first_name_txt = Label(page, text="First name is: ", bg ="#99ffcc", fg="#3366ff",font=("Segoe UI Black", 12))
    last_name_txt = Label(page, text="Last name is: ", bg ="#99ffcc", fg="#3366ff", font=("Segoe UI Black", 12))
    age_txt = Label(page, text="His/Her age is: ", bg ="#99ffcc", fg="#3366ff", font=("Segoe UI Black", 12))
    job_txt = Label(page, text="His/her job is: ", bg ="#99ffcc", fg="#3366ff", font=("Segoe UI Black", 12))
    gender_txt = Label(page, text="His/Her gender is: ", bg ="#99ffcc", fg="#3366ff", font=("Segoe UI Black", 12))
    salary_txt = Label(page, text="His/Her salary is: ", bg ="#99ffcc", fg="#3366ff", font=("Segoe UI Black", 12))
    date_created_txt = Label(page, text="Created/Last updated date: ", bg ="#99ffcc", fg="#3366ff", font=("Segoe UI Black", 12))

    img_lbl.place(relx=0.59, rely=0.15, anchor=CENTER)
    first_name_lbl.place(relx=0.55, rely=0.35, anchor=CENTER)
    last_name_lbl.place(relx=0.55, rely=0.4, anchor=CENTER)
    age_lbl.place(relx=0.55, rely=0.45, anchor=CENTER)
    job_lbl.place(relx=0.55, rely=0.5, anchor=CENTER)
    gender_lbl.place(relx=0.55, rely=0.55, anchor=CENTER)
    salary_lbl.place(relx=0.55, rely=0.6, anchor=CENTER)
    date_created_lbl.place(relx=0.6, rely=0.65, anchor=CENTER)

    first_name_txt.place(relx=0.3, rely=0.35, anchor=CENTER)
    last_name_txt.place(relx=0.3, rely=0.4, anchor=CENTER)
    age_txt.place(relx=0.3, rely=0.45, anchor=CENTER)
    job_txt.place(relx=0.3, rely=0.5, anchor=CENTER)
    gender_txt.place(relx=0.3, rely=0.55, anchor=CENTER)
    salary_txt.place(relx=0.3, rely=0.6, anchor=CENTER)
    date_created_txt.place(relx=0.3, rely=0.65, anchor=CENTER)

    back_btn = Button(page, width=20, bg="#99ccff", fg="#000000", font=("Segoe UI Black", 12),
                      command=lambda: back_to_prev_page(page), text="Back!")
    back_btn.place(relx=0.5, rely=0.90, anchor=CENTER)


def go_to_next_page(is_admin=0):

    if not is_admin:
        employee_page.deiconify()  # show employee page
        root_page.withdraw()  # hide root page

        # clean employee page
        for child in employee_page.winfo_children():
            child.destroy()

        # update  employee page
        update_emp_page(employee_page)

    else:
        employees_page.deiconify()  # show employees page
        root_page.withdraw()  # hide root page


def check_authentication_input_form(user_field, pass_field):
    global employee_person_logged_in

    # extract credentials from fields
    username_emp_in = user_field.get()
    password_emp_in = pass_field.get()

    if username_emp_in == 'Admin' and password_emp_in == 'admin':  # if it is admin
        go_to_next_page(1)  # go to page for admin
    else:  # else search for employee credentials
        is_emp_found = False
        my_cursor = my_db.cursor(buffered=True)  # set to extract all the data at once
        my_cursor.execute(f'Select * from employees')  # extract needed data

        for emp in my_cursor:
            username_emp = emp[0]  # get username == first_name
            password_emp = emp[1]  # get password == last_name

            if username_emp_in == username_emp and password_emp_in == password_emp:  # if employee is found in database
                is_emp_found = True
                employee_person_logged_in = emp  # extract emp credentials
                break

        my_cursor.close()

        if is_emp_found:
            go_to_next_page(0)  # go to page for employee
        else:
            messagebox.showwarning("Warning!", "The credentials are not registered!")

    # delete content of fields from index zero to the end
    user_field.delete(0, 'end')
    pass_field.delete(0, 'end')


def init_main_frame():
    root_page.title("Management of employees")
    root_page.geometry('600x600')
    root_page.iconbitmap("my_icon.ico")
    root_page.configure(bg="#66ff66")
    root_page.resizable(False, False)

    user_lbl = Label(root_page, width=10, text="Username: ", bg ="#99ffcc", fg="#3366ff", font=("Segoe UI Black", 12))
    pass_lbl = Label(root_page, width=10, text="Password: ", bg="#99ffcc", fg="#3366ff", font=("Segoe UI Black", 12))
    img_lbl = Label(image=logo_root_img)

    user_field = Entry(root_page, width=30)
    passwd_field = Entry(root_page, width=30)
    login_btn = Button(root_page, text="Login", width=20, bg="#99ccff", fg="#000000",
                       font=("Segoe UI Black", 12),
                       command=lambda: check_authentication_input_form(user_field, passwd_field))

    img_lbl.place(relx=0.5, rely=0.25, anchor=CENTER)
    user_lbl.place(relx=0.27, rely=0.5, anchor=CENTER)
    pass_lbl.place(relx=0.27, rely=0.6, anchor=CENTER)
    user_field.place(relx=0.5, rely=0.5, anchor=CENTER)
    passwd_field.place(relx=0.5, rely=0.6, anchor=CENTER)
    login_btn.place(relx=0.5, rely=0.7, anchor=CENTER)


def back_to_prev_page(curr_page):
    curr_page.withdraw()  # hide current page
    root_page.deiconify()  # show root page


def init_employee_frame():
    employee_page.title("Employee page")
    employee_page.geometry('700x700')
    employee_page.iconbitmap("my_icon.ico")
    employee_page.configure(bg="#66ff66")
    employee_page.resizable(False, False)


def update_first_last_couple_dict(first_name_emp, last_name_emp):
    if first_name_emp not in first_last_dict_names:
        first_last_dict_names[first_name_emp] = []
        first_last_dict_names[first_name_emp].append(last_name_emp)
    else:
        first_last_dict_names[first_name_emp].append(last_name_emp)


def update_nr_emp_per_job_dict(job_emp):
    if job_emp not in nr_emp_per_job:
        nr_emp_per_job[job_emp] = 1
    else:
        nr_emp_per_job[job_emp] += 1


def create_table_employees(my_cursor):
    # create table
    # show just columns with headings, without column 0,
    # to insert things in column 0 you must used text='something in column 0' in order to complete column 0
    # values is used for new columns created
    my_table = ttk.Treeview(employees_page, show='headings')
    my_table['columns'] = ('First_Name', 'Last_Name', 'Age', 'Job', 'Gender', 'Salary', 'Hire_date')

    # define headings
    my_table.heading('First_Name', text='First_Name')
    my_table.heading('Last_Name', text='Last_Name')
    my_table.heading('Age', text='Age')
    my_table.heading('Age', text='Age')
    my_table.heading('Job', text='Job')
    my_table.heading('Gender', text='Gender')
    my_table.heading('Salary', text='Salary')
    my_table.heading('Hire_date', text='Hire_date')

    for emp in my_cursor:
        first_name_emp = emp[0]
        last_name_emp = emp[1]
        job_emp = emp[3]

        update_first_last_couple_dict(first_name_emp, last_name_emp)
        update_nr_emp_per_job_dict(job_emp)

        # insert credentials of every emp to the root node '', after all created nodes(that is the meaning of END)
        my_table.insert('', END, values=emp)

    # place the table in the page
    my_table.place(relx=0.5, rely=0.5, anchor=CENTER)
    return my_table


def check_values_add_employee_form(age, gender, salary):
    are_values_ok = True

    # verify if age is number!
    try:
        int(age)
    except ValueError:
        are_values_ok = False

    # verify if salary is number!
    try:
        int(salary)
    except ValueError:
        are_values_ok = False

    # verify if gender  has correct value!
    if not(gender.lower() == 'male' or gender.lower() == 'female'):
        are_values_ok = False

    return are_values_ok


def reset_table(my_table):
    global detached_rows

    # attach nodes, in order to have all the data in table
    for row in detached_rows:
        my_table.reattach(row, '', 0)  # attach node to tree, with parent node '', at index 0

    detached_rows = []  # clean detached rows


def add_employee(my_table, first_name_in, last_name_in, age_in, gender_in, salary_in, job_in):
    # get the content from add emp form
    first_name_emp = first_name_in.get()
    last_name_emp = last_name_in.get()
    age_emp = age_in.get()
    gender_emp = gender_in.get()
    salary_emp = salary_in.get()
    job_emp = job_in.get()

    # check if al the fields content are not empty
    if first_name_emp != '' and last_name_emp != '' and  age_emp != ''  \
            and gender_emp != '' and salary_emp != '' and job_emp != '':

        # check the values for age, gender and salary if these are correct!
        if check_values_add_employee_form(age_emp, gender_emp, salary_emp) is False:
            messagebox.showwarning("Warning!", "The values for gender age and salary are not all correct!")
            return

        # if the employee is not in the table
        if not(first_name_emp in first_last_dict_names and last_name_emp in first_last_dict_names[first_name_emp]):
            update_first_last_couple_dict(first_name_emp, last_name_emp)
            update_nr_emp_per_job_dict(job_emp)

            # get teh current time
            time_now = datetime.datetime.now()

            # create the a new row for a new emp
            new_emp = (first_name_emp, last_name_emp, int(age_emp), job_emp, gender_emp,
                       int(salary_emp), time_now.strftime('%Y-%m-%d %H:%M:%S'))

            # add emp in database
            add_emp_in_db(new_emp, my_db)

            # insert emp in table of employees, with parent ='', at index 0
            my_table.insert('', 0, values=new_emp)

            # clean input fields
            first_name_in.delete(0, END)
            last_name_in.delete(0, END)
            age_in.delete(0, END)
            gender_in.delete(0, END)
            job_in.delete(0, END)
            salary_in.delete(0, END)

        # else if employee is already registered
        else:
            messagebox.showwarning("Warning!", "The Employee "
                                               "with this first name and this last name is already registered!")
    # else if all the fields are not completed!
    else:
        messagebox.showwarning("Warning!", "Complete all the fields in order to add!")


def delete_employees(my_table):
    # get the selected employees
    records = my_table.selection()

    if records != ():  # if some employees are selected
        for record in records:
            # get info about emp
            first_name = my_table.item(record)['values'][0]
            last_name = my_table.item(record)['values'][1]
            job = my_table.item(record)['values'][3]

            # decrement the person with that job
            nr_emp_per_job[job] -= 1

            # eliminate (first,last names) couple
            first_last_dict_names[first_name].remove(last_name)

            # delete from table of the employees page
            my_table.delete(record)

            # delete emp from database
            delete_emp_from_db(first_name, last_name, my_db)
    else:
        messagebox.showwarning("Warning!", "You didn't select any employee!")


def select_line(first_name_in, last_name_in, age_in, job_in, gender_in, salary_in, my_table):
    global selected_first_emp
    first_name_in.delete(0, END)
    last_name_in.delete(0, END)
    age_in.delete(0, END)
    job_in.delete(0, END)
    gender_in.delete(0, END)
    salary_in.delete(0, END)

    if my_table.selection() != ():  # if something is selected

        # get info for for first employee selected
        first_emp_selected = my_table.item(my_table.selection()[0])
        selected_first_emp = my_table.selection()[0]
        first_name_emp = first_emp_selected['values'][0]
        last_name_emp = first_emp_selected['values'][1]
        age_emp = first_emp_selected['values'][2]
        job_emp = first_emp_selected['values'][3]
        gender_emp = first_emp_selected['values'][4]
        salary_emp = first_emp_selected['values'][5]

        # put the info in to the input fields, starting with index 0 in content
        first_name_in.insert(0, first_name_emp)
        last_name_in.insert(0, last_name_emp)
        age_in.insert(0, age_emp)
        job_in.insert(0, job_emp)
        gender_in.insert(0, gender_emp)
        salary_in.insert(0, salary_emp)

    # if is not  selected
    else:
        messagebox.showwarning("Warning!", "You didn't select anything!")


def update_employee(first_name_in, last_name_in, age_in, job_in, gender_in, salary_in, my_table):
    global selected_first_emp
    if selected_first_emp is not None:
        # get the information from form
        first_name_form = first_name_in.get()
        last_name_form = last_name_in.get()
        age_form = age_in.get()
        job_form = job_in.get()
        gender_form = gender_in.get()
        salary_form = salary_in.get()

        # check if all the fields are completed
        if not(first_name_form != '' and last_name_form != '' and age_form != '' \
                and job_form != '' and gender_form != '' and salary_form != ''):
            messagebox.showwarning("Warning!", "You must have all the fields completed in order to update!!")
            return

        # check if age, gender, and salary have correct values!
        if check_values_add_employee_form(age_form, gender_form, salary_form) is False:
            messagebox.showwarning("Warning!", "The values for gender age and salary are not all correct!")
            return

        # get the selected person
        selected_emp = selected_first_emp
        # get the attributes of selected emp
        selected_emp = my_table.item(selected_emp)

        first_name_emp = selected_emp['values'][0]
        last_name_emp = selected_emp['values'][1]
        job_emp = selected_emp['values'][3]
        data_created_emp = selected_emp['values'][6]

        # decrement the person with that job
        nr_emp_per_job[job_emp] -= 1

        # eliminate (first,last names) couple
        first_last_dict_names[first_name_emp].remove(last_name_emp)

        update_first_last_couple_dict(first_name_form, last_name_form)
        update_nr_emp_per_job_dict(job_form)

        update_emp_in_bd(my_db, first_name_form, last_name_form, age_form, job_form, gender_form, salary_form,
                         first_name_emp,  last_name_emp)

        # update for select emp the data
        my_table.item(selected_first_emp, values=(first_name_form, last_name_form, age_form, job_form, gender_form,
                                                  salary_form, data_created_emp))

        # clean the input fields, from index 0 to the end
        first_name_in.delete(0, END)
        last_name_in.delete(0, END)
        age_in.delete(0, END)
        job_in.delete(0, END)
        gender_in.delete(0, END)
        salary_in.delete(0, END)
        selected_first_emp = None
    else:
        messagebox.showwarning("Warning!", "You didn't select anything in order to update!")


def search_employees(text_to_search, my_table):
    global detached_rows
    for row in detached_rows:
        my_table.reattach(row, '', 0)  # reattach the nodes row at index 0, with parent ''

    detached_rows = []  # clean detached nodes

    children = my_table.get_children()  # get the children nodes(rows)
    for child in children:
        # extract values from rows
        first_name_emp = my_table.item(child)['values'][0].lower()
        last_name_emp = my_table.item(child)['values'][1].lower()
        job_emp = my_table.item(child)['values'][3].lower()
        gender_emp = my_table.item(child)['values'][4].lower()

        # in TreeView values per nod in list are
        # 0 -> first name(string)
        # 1 -> last name(string)
        # 2 -> age(numerical)
        # 3 -> job(string)
        # 4 -> gender(string)
        # 5 -> salary(numerical)
        # 6 -> hire date(also string)

        # if the value is not in one column, detach  the node
        if text_to_search.get().lower() not in first_name_emp.lower() \
                and text_to_search.get().lower() not in last_name_emp.lower() \
                and text_to_search.get().lower() not in job_emp.lower() \
                and text_to_search.get().lower() != gender_emp.lower() :
            detached_rows.append(child)
            my_table.detach(child)


def write_to_excel(my_table):
    # save the cv file
    my_file = asksaveasfile(initialfile='Untitled.csv', defaultextension=".csv", filetypes=[("CSV File", "*.csv")])

    if my_file is not  None:
        # open the csv file
        opener_file = open(my_file.name, 'w', newline="")
        csv_writer = csv.writer(opener_file, dialect='excel')

        # write the headings
        csv_writer.writerow(('first_Name', 'last_name', 'age', 'job', 'gender', 'salary', 'hire_date'))

        # write the records
        for child in my_table.get_children():
            record = my_table.item(child)['values']
            csv_writer.writerow(record)


def draw_statistics():
    nr_persons = []
    jobs = []
    for job in nr_emp_per_job.keys():
        if nr_emp_per_job[job] != 0:
            jobs.append(job)
            nr_persons.append(nr_emp_per_job[job])

    # display statistics
    # set the values, labels. and to show percentage with 2 decimals
    drawer.pie(nr_persons, labels=jobs, autopct='%.2f')
    drawer.legend(loc=(1.04, 0))  # set where to place legend
    drawer.show()  # show the pie


def create_employees_page():
    # set to extract all the the data at once
    my_cursor = my_db.cursor(buffered=True)
    my_cursor.execute("select * from employees order by hire_date desc;")

    # create input fields
    first_name_in = Entry(employees_page)
    last_name_in = Entry(employees_page)
    age_in = Entry(employees_page)
    job_in = Entry(employees_page)
    gender_in = Entry(employees_page)
    salary_in = Entry(employees_page)
    search_bar_in = Entry(employees_page, width=32)

    # create table
    my_table = create_table_employees(my_cursor)

    # back button
    bck_btn = Button(employees_page, text="Back!",  width=20, bg="#99ccff", fg="#000000", font=("Segoe UI Black", 12),
                     command=lambda: back_to_prev_page(employees_page))
    bck_btn.place(relx=0.3, rely=0.05, anchor=CENTER)

    # add employee button
    add_btn = Button(employees_page, text="Insert employee!",
                     width=20, bg="#99ccff", fg="#000000", font=("Segoe UI Black", 12),
                     command=lambda: add_employee(my_table,
                                                  first_name_in, last_name_in, age_in, gender_in, salary_in, job_in))
    add_btn.place(relx=0.5, rely=0.05, anchor=CENTER)

    # delete employees button
    del_btn = Button(employees_page, text="Delete Some Employees!", width=20, bg="#99ccff", fg="#000000",
                     font=("Segoe UI Black", 12),
                     command=lambda: delete_employees(my_table))
    del_btn.place(relx=0.7, rely=0.05, anchor=CENTER)

    # reset table to initial state button
    reset_table_btn = Button(employees_page, text="Reset table!!", width=20, bg="#99ccff",
                             fg="#000000", font=("Segoe UI Black", 12),
                             command=lambda: reset_table(my_table))
    reset_table_btn.place(relx=0.87, rely=0.05, anchor=CENTER)

    # update the employee button
    update_btn = Button(employees_page, text="Update!", width=20, bg="#99ccff", fg="#000000",
                        font=("Segoe UI Black", 12),
                        command=lambda: update_employee(first_name_in, last_name_in, age_in,
                                                        job_in, gender_in, salary_in, my_table))
    update_btn.place(relx=0.3, rely=0.15, anchor=CENTER)

    # select the employee to be update button
    select_btn = Button(employees_page, text="Select!",
                        width=20, bg="#99ccff", fg="#000000", font=("Segoe UI Black", 12),
                        command=lambda: select_line(first_name_in,
                                                    last_name_in, age_in, job_in, gender_in, salary_in, my_table))
    select_btn.place(relx=0.5, rely=0.15, anchor=CENTER)

    # button to activate search process
    search_btn = Button(employees_page, text="Search employees!", width=20, bg="#99ccff", fg="#000000",
                        font=("Segoe UI Black", 12),
                        command=lambda: search_employees(search_bar_in, my_table))
    search_btn.place(relx=0.7, rely=0.15, anchor=CENTER)

    imp_btn = Button(employees_page, text="Export to Excel File!", width=20, bg="#99ccff", fg="#000000",
                     font=("Segoe UI Black", 12),
                     command=lambda: write_to_excel(my_table))
    imp_btn.place(relx=0.1, rely=0.05, anchor=CENTER)

    st_btn = Button(employees_page, text="Show statistics!", width=20, bg="#99ccff", fg="#000000",
                    font=("Segoe UI Black", 12), command=lambda: draw_statistics())
    st_btn.place(relx=0.1, rely=0.15, anchor=CENTER)

    # input place on the window
    first_name_in.place(relx=0.10, rely=0.27, anchor=CENTER)
    last_name_in.place(relx=0.23, rely=0.27, anchor=CENTER)
    age_in.place(relx=0.36, rely=0.27, anchor=CENTER)
    job_in.place(relx=0.49, rely=0.27, anchor=CENTER)
    gender_in.place(relx=0.62, rely=0.27, anchor=CENTER)
    salary_in.place(relx=0.75, rely=0.27, anchor=CENTER)
    search_bar_in.place(relx=0.85, rely=0.15, anchor=CENTER)
    my_cursor.close()


def init_employees_frame():
    employees_page.title("Employees page")
    employees_page.geometry('1500x600')
    employees_page.iconbitmap("my_icon.ico")
    employees_page.configure(bg="#66ff66")
    employees_page.resizable(False, False)
    create_employees_page()
