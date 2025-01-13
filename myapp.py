## Importing required libraries 
import streamlit as st 
import mysql.connector

## setting web_page configuration 
st.set_page_config(
    page_title = "SQL Playground",
    page_icon = "📈"  
)

## Title
st.title(":blue[SQL] Playground")

## subheader 
st.subheader(":blue[Database Management] made :blue[Effortless]" , divider="grey")
st.write(":grey[The objective of this Streamlit app is to provide a user-friendly interface that automates essential SQL operations , enabling users to efficiently manage and interact with databases. The app simplifies tasks such as listing and switching between databases , creating and deleting databases , viewing table structures , listing tables , and performing data manipulation operations like inserting , updating and deleting records. It is designed to streamline database management which making it accessible for both beginners and professionals.]")

## Streamlit inputs for database connection
# user = st.text_input("Enter user name")
# password = st.text_input("Enter password", type="password")
# host = st.text_input("Enter host name")
# port = st.text_input("Enter port number")

# Function to connect to the database
def connect(u, p, h, po):
    config = {
        "user": u,
        "password": p,
        "host": h,
        "port": po
    }
    try:
        conn = mysql.connector.connect(**config)  # Variable arguments
        st.success("Successfully Connected")
        return conn
    except mysql.connector.Error as e:
        # st.error(f"Connection Failed: {e}")
        return None
    
# Connect to MySQL
connection = connect("root","mysql2610","localhost",3306)

if connection :
    st.subheader(":blue[Database Commands]",divider="grey")
    st.write(":grey[These commands are essential for managing and interacting with databases in SQL. They allow users to list available databases , switch to a specific database , create new databases, delete existing ones , view table structures and list tables within a database. Together they provide the foundational tools for database management and organization.]")
    ## creating tabs 
    tab1,tab3,tab2,tab8,tab5,tab4= st.tabs([":blue[Show Databases]","Use Database",":blue[Create Database]","Drop Database",":blue[Describe Table]","Show Tables"])

    cur = connection.cursor()

    ## show databases
    with tab1 : 
        if st.button(":blue[Show]",key="a1"):
            cur.execute("SHOW DATABASES")
            for data in cur:
                st.info((data[0]))

    ## create database 
    with tab2 : 
        db_name = st.text_input("Enter Database name")
        sql = f"CREATE DATABASE {db_name}"
        if st.button(":blue[Create]"):
            if db_name.strip():
                try:
                    cur.execute(sql)
                    st.success(f"Database {db_name} Created successfully ")
                except mysql.connector.Error as e : 
                    st.error(f"Error creating database : {e}")
            else :
                st.warning("Not a valid database name")
        if st.button(":blue[View databases]"):
            cur.execute("SHOW DATABASES")
            for data in cur:
              st.info(data[0])

    ## creating database list
    cur.execute("SHOW DATABASES")
    db_lst = []
    for data in cur:
        db_lst.append(data[0])

    ## using database 
    with tab3:
        db_in_use = st.selectbox("Choose Database",options=db_lst)
        sql = f"USE {db_in_use}"
        try : 
            cur.execute(sql)
            st.success(f"Database {db_in_use} used successfully")
        except mysql.connector.Error as e :
            st.warning(f"Not valid database")

    ## show tables in database 
    with tab4 :
            if st.button(":blue[Show]",key="a2"):
                sql = "Show tables"
                cur.execute(sql)
                for table in cur:
                   if(table):
                      st.info(table[0])
                   else:
                    st.write("No table exists")

    ## counting tables
    cur.execute("Show tables")
    table_names = []
    for table in cur:
        table_names.append(table[0])

    ## Describing tables
    with tab5 :
        table_name = st.selectbox("Choose table ",options=table_names)
        if st.button(":blue[Describe table]"):
            if table_name.strip():
                try : 
                    sql = f"DESC {table_name}"
                    cur.execute(sql)
                    count = 0
                    for data in cur:
                        count = count + 1
                        st.info(f"row number = {count}")
                        for i in range(len(data)):
                            if(data[i] == None):
                                st.write("NULL")
                            else:
                                st.write(data[i])
                except mysql.connector.Error as e:
                    st.error(f"Error describing table '{table_name}': {e}")
            else:
                    st.warning("Please enter a valid table name.")

    ## Delete database 
    with tab8 : 
        db_drop = st.text_input("Enter Database name : ",key="a")
        sql = f"DROP DATABASE {db_drop}"
        if st.button(":blue[Drop]"):
            if db_drop.strip():
                try:
                    cur.execute(sql)
                    st.success(f"Database {db_drop} deleted successfully ")
                except mysql.connector.Error as e : 
                    st.error(f"Error deleting database : {e}")
            else :
                st.warning("Not a valid database name")
        if st.button(":blue[View databases]",key="b"):
            cur.execute("SHOW DATABASES")
            for data in cur:
              st.info(data[0])

    st.subheader(":blue[Data Fetch Commands]",divider="grey")
    st.write(":grey[The SELECT command is used to retrieve data from a database. It allows users to either fetch all records from a table or filter specific columns or rows based on requirements. These commands are fundamental for querying and analyzing data stored in tables.]")            
    tab6 , tab7  = st.tabs([":blue[Select ALL]","Select Specific"])

    ## Fetch ALL data
    with tab6:
        tab_name = st.selectbox("Choose table",options=table_names)
        if st.button(":blue[Fetch All data]"):
            try:
                sql = f"SELECT * FROM {tab_name}"
                cur.execute(sql)
                data = cur.fetchall()
                count = 0
                for rows in data:
                    count = count + 1
                    st.write(f"Data in row {count} = {rows}")
            except:
                st.error("Data cannot be fetched")

    ## Fetch Specific data
    with tab7:
        ## taking no. of rows as input
        number = st.text_input("Enter number of rows",key=int)
        try:
            a = int(number)
        except:
            st.write()
        if st.button(":blue[Fetch Specific data]"):
            sql = f"SELECT * FROM {tab_name}"
            try :
                cur.execute(sql)
                data = cur.fetchmany(a)
                count = 0
                for rows in data:
                    count = count + 1
                    st.write(f"Data in row {count} = {rows}")
            except : 
                    st.error("Cannot be fetched")
    
    st.subheader(":blue[Data Manipulation Commands]",divider="grey")
    st.write(":grey[These commands are essential for managing and modifying data in SQL. They allow users to add new records , update existing data and remove specific records from tables. Together they provide the foundational tools for maintaining and organizing data within a database.]")
    tab12 , tab10 , tab11 = st.tabs([":blue[Insert]","Update",":blue[Delete]"])
    
    ## Update data
    with tab10:
                table_name_up = st.selectbox("Choose table",options=table_names,key="e")
                column_list = [] 
                sql1 = f"DESC {table_name_up}" 
                try:  
                    cur.execute(sql1)     
                    for data in cur:
                        column_list.append(data[0])
                except :
                    st.write("")
                column_to_update = st.selectbox("Choose column name(Set)",options=column_list,key="f")
                by_column = st.selectbox("Choose Column name(Where)",options=column_list)
                value1 = st.text_input(f"Enter {column_to_update} value ")
                value2 = st.text_input(f"Enter {by_column} value")
                if st.button(":blue[Make Changes]"):
                    try:
                        sql = f"UPDATE {table_name_up} SET {column_to_update} = {value1} WHERE {by_column} = {value2}"
                        cur.execute(sql)
                        connection.commit()
                        st.success("Data Successfully Updated")
                    except mysql.connector.Error as e:
                        st.error(f"Failed to update : {e}")
    
    ## Delete data 
    with tab11:
                table_name_del = st.selectbox("Choose table",options=table_names,key="def")
                column_list = [] 
                sql1 = f"DESC {table_name_del}" 
                try:  
                    cur.execute(sql1)     
                    for data in cur:
                        column_list.append(data[0])
                except : 
                    st.write()
                column_to_delete = st.selectbox("Choose column name(Where)",options=column_list,key="abc")
                value3 = st.text_input(f"Enter {column_to_delete} value",key="zzz")
                if st.button(":blue[Delete]"):
                    try:
                        sql = f"DELETE FROM {table_name_del} WHERE {column_to_delete} = {value3}"
                        cur.execute(sql)
                        connection.commit()
                        st.success("Data Successfully Deleted")
                    except mysql.connector.Error as e:
                        st.error(f"Failed to Delete : {e}")

    ## Insert data
    with tab12:
                table_name_ins = st.selectbox("Choose table",options=table_names,key="Ins")
                column_list = [] 
                sql1 = f"DESC {table_name_ins}" 
                try:  
                    cur.execute(sql1)     
                    for data in cur:
                        column_list.append(data[0])        
                except : 
                    st.write()
                lst = []
                str = ""
                for i in range(len(column_list)):
                    value = st.text_input(f"Enter value for column : [ {column_list[i]} ]")
                    lst.append(value)
                    if(i==(len(column_list)-1)):
                        str = str+value
                    else:
                        str = str+value+","
                
                ## st.write(str)
                sql = f"Insert into {table_name_ins} values({str})"
                ## st.write(sql)
                if st.button(":blue[Insert]",key="inst"):
                    try :
                        cur.execute(sql)
                        connection.commit()
                        st.success("Data Inserted Successfully")
                    except mysql.connector.Error as e :
                        st.error(f"Failed to Insert : {e}")
                    