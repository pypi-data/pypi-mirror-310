import matplotlib.pyplot as plt
import pandas as pd
import time
import sqlite3
from the_secret_file import secret_dict


File = "Sales.db"
db =sqlite3.connect(File)
db.execute("create table if not exists sold (S_No INTEGER PRIMARY KEY AUTOINCREMENT,Buyer_Name varchar(50) DEFAULT REFIL, No_of_papers int(11), Money_Received int(11), Extra_paper_givenForFree int(11), Profit float, Remaining_Pages_after_selling int(11))")
cursor = db.cursor()

# cursor.execute('insert into sold(Buyer_name,no_of_papers,money_received,extra_paper_givenforfree,profit,remaining_pages_after_selling) values("akhand",10,20,1,3.2,219)')
# db.commit()

def refil_sheets():
    cursor.execute('select Remaining_Pages_after_selling from sold where Remaining_Pages_after_selling = 0')
    record_exist = cursor.fetchone()
    if record_exist:
        cursor.execute('select Remaining_Pages_after_selling from sold')
        get_remaining_pages = cursor.fetchall()
        index_val = len(get_remaining_pages)

        remaining_pages = get_remaining_pages[index_val-1][0] + (500-(get_remaining_pages[index_val-1][0]))
        db.execute('insert into sold(remaining_pages_after_selling) values(?)', [remaining_pages])
        db.commit()
        print('Refil Sucessfull!')

    else:
        print('Cannot refill now as there are sufficient sheets left!')

def add_record():
    welcome_section_string = ' WELCOME TO RECORD ADDING SECTION '
    print(welcome_section_string.center(150))

    name = input('Enter the name of buyer : ')
    number_of_pages = int(input('Enter the number of pages : '))
    money_received = (2/3)*number_of_pages
    extra_paper = int(input("Enter the number of extra papers given : "))
    profit = (((2/3)-(220/500))*number_of_pages)-(((2/3)-(220/500))*extra_paper)

    cursor.execute('select * from sold where s_no = 1')
    record_exist = cursor.fetchone()
    if record_exist:
        cursor.execute('select Remaining_Pages_after_selling from sold')
        get_remaining_pages = cursor.fetchall()
        index_val = len(get_remaining_pages)
        remaining_pages = (get_remaining_pages[index_val-1][0])-(number_of_pages+extra_paper)
        db.execute('insert into sold(Buyer_name,no_of_papers,money_received,extra_paper_givenforfree,profit,remaining_pages_after_selling) values(?,?,?,?,?,?)', [name,number_of_pages,money_received,extra_paper,profit,remaining_pages])
        db.commit()

    
    else:
        remaining_pages = 500-(number_of_pages+extra_paper)
        db.execute('insert into sold(Buyer_name,no_of_papers,money_received,extra_paper_givenforfree,profit,remaining_pages_after_selling) values(?,?,?,?,?,?)', [name,number_of_pages,money_received,extra_paper,profit,remaining_pages])
        db.commit()

    main()

def exp_to_csv():
    df = pd.read_sql_query("SELECT Buyer_name,no_of_papers,money_received,extra_paper_givenforfree,profit from sold where buyer_name != 'REFILL'", db)
    # print(df)
    df.to_html('SaleRecords.html',index=False)
    df.to_csv('SaleRecords.csv',index=False)
    print("\nFile sucessfully converted to CSV and HTML\n")

    profits = round(df['Profit'].sum())
    moneyearned = round(df['Money_Received'].sum())

    print('\nYou have made a total sale of ₹'+str(moneyearned),'and a profit of ₹'+str(profits),'\n')

    cust_name = df['Buyer_Name']
    page_quantity = df['No_of_papers']

    plt.bar(cust_name, page_quantity)
    plt.xlabel('Customer Name')
    plt.ylabel("Amount of Papers Purchased")
    plt.title("Customer's Report")
    recordName = time.strftime('%d-%m-%Y')
    plt.savefig(f'CustomerRecord-On-{recordName}.jpg')
    plt.show()

def view_record():
    # df = pd.read_sql_query("SELECT Buyer_name,no_of_papers,money_received,extra_paper_givenforfree,profit from sold where buyer_name != 'REFILL'", db)
    # print(df)

    print("\t\t\t\t\t\t---------------Sales Record---------------\n")
    takename = cursor.execute("select Buyer_Name,No_of_papers,Money_Received,Extra_paper_givenForFree,Profit from sold where Buyer_Name != 'REFILL'").fetchall()
    totnames = len(takename)
    i = 0    
    print("Customer Name\t\tNo of Paper\t\tMoney Receiived\t\tExtra Paper Given\t\tProfit")

    for i in range(totnames):
        print(takename[i][0],'|\t\t\t|',takename[i][1],'|\t\t\t|',takename[i][2],'|\t\t\t\t|',takename[i][3],'|\t\t|',takename[i][4],'|\t\t')
        i=i+1
        print('\t\t\t\t\t\t•••••••••••••••••••••••••••••••••••••••••••••••••••••••\n')
        time.sleep(1)
        
    print("\t\t\t\t\t\t\t\t<END OF RECORDS>")

def main():

        greating_akhand_string = ' WELCOME BACK AKHAND TO YOUR STORE '
        print(greating_akhand_string.center(150))

        cursor.execute('select * from sold where s_no = 1')
        record_exist = cursor.fetchone()
        if record_exist:
            cursor.execute('select Remaining_Pages_after_selling from sold')
            get_remaining_pages = cursor.fetchall()
            index_val = len(get_remaining_pages)
            remaining_pages = str(get_remaining_pages[index_val-1][0])
        else:
            remaining_pages = str(500)

        while True:
            cursor.execute('select * from sold where s_no = 1')
            record_exist = cursor.fetchone()
            if record_exist:
                cursor.execute('select Remaining_Pages_after_selling from sold')
                get_remaining_pages = cursor.fetchall()
                index_val = len(get_remaining_pages)
                remaining_pages = str(get_remaining_pages[index_val-1][0])
            else:
                remaining_pages = str(500)
            print('\n\t ** REMAINING PAGES :',remaining_pages+'/500 **\n')

            option_choice = int(input(''' Select an option from the below mentioned options
                                1. Insert Selling Details
                                2. View Record
                                3. Refil Sheets 
                                4. Export To CSV \n'''))
            
            if option_choice == 1:
                ask_choice = input('Do you want to continue adding a record?(Y/N) : ')
                if ask_choice == 'Y':
                    add_record()
                elif ask_choice == 'N':
                    print('Exiting from software in 3 seconds')
                    time.sleep(1)
                    print('3')
                    time.sleep(1)
                    print('2')
                    time.sleep(1)
                    print('1')
                    main()
                else:
                    print('This software is case-sensitive make sure to enter the input as required!')

            elif option_choice == 2:
                view_record()

            elif option_choice == 3:
                refil_sheets()

            elif option_choice == 4:
                exp_to_csv()

            else:
                print("Invalid Option!!")


welcome_string = ' WELCOME TO CENTUARY PAPER STORE '
print(welcome_string.center(150))

print(secret_dict['Akhand']) # This is the password
Input_password = input("ENTER YOUR PASSWORD TO CONTINUE : ")

if Input_password == secret_dict['Akhand']:
    main()

else:
    leave_string = ' INCORRECT PASSWORD ENTERED!! PLEASE TRY AGAIN... '
    print(leave_string.center(150))