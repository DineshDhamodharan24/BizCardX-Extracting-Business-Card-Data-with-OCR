# import in library this project
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import pandas as pd
import numpy as np
import mysql.connector as sql
import requests
from PIL import Image
import easyocr
import cv2
import re
import time

# To create streamlit First step._.
def set_page_config():
    st.set_page_config(
        page_title="BizCardX: Extracting Business Card Data with OCR",
        page_icon="https://uxwing.com/wp-content/themes/uxwing/download/business-professional-services/address-card-icon.png",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={'About': """# This OCR app is created by *DINESH*!"""}
    )

set_page_config()

# Add a styled page title
st.markdown("<h1 style='text-align: center; color:Indigo ;'>BizCardX: Extracting Business Card Data with OCR</h1>", unsafe_allow_html=True)

# This is Application background image._.
def setting_bg():
    st.markdown(
        """
        <style>
            .stApp {
                background: url("https://cdn.pixabay.com/photo/2015/12/01/15/43/black-1072366_1280.jpg");
                background-size: 100% 100vh;
                background-repeat: no-repeat;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

setting_bg()

# Database Connection._.
Mydb = sql.connect(host = "localhost",
                   user = "root",
                   password = "Din@9600",
                   database = "BussinessCard")
mycursor = Mydb.cursor(buffered=True)

 # --------The command to create the table has already been executed. -----
 
# mycursor = Mydb.cursor()
# mycursor.execute("CREATE TABLE Card_data("
#                  "id INT AUTO_INCREMENT PRIMARY KEY,"
#                  "name VARCHAR(255),"
#                  "designation VARCHAR(255),"
#                  "company VARCHAR(255),"
#                  "contact VARCHAR(255),"
#                  "email VARCHAR(255),"
#                  "website VARCHAR(255),"
#                  "address VARCHAR(255),"
#                  "city VARCHAR(255),"
#                  "state VARCHAR(255),"
#                  "pincode VARCHAR(255),"
#                  "image LONGBLOB )")


# This is selecting option menu._.
selected = option_menu(None, ["Home", "Upload & Extract", "Database", "Profile"],
                       icons=["house", "cloud-upload", "pencil-square"],
                       default_index=0,
                       orientation="horizontal",
                       styles={"nav-link": {"font-size": "35px", "text-align": "center", "margin": "0px",
                                           "--hover-color": "#6495ED"},
                               "icon": {"font-size": "35px"},
                               "container": {"max-width": "6000px"},
                               "nav-link-selected": {"background-color": "#93cbf2"}})

text_process = st.expander("Text Processing", expanded=False)

# I have creating Home page what are the in this project work in small description._.
if selected == 'Home':
    left, right = st.columns(2)
    with right:
        st.write('### TECHNOLOGIES USED')
        st.write('### *:red[Python]  *:red[Streamlit] *:red[EasyOCR]  *:red[OpenCV]  *:red[MySQL]')
        st.write("###   *To Learn more about easyOCR [press here](https://pypi.org/project/easyocr/) ")

    with left:
        st.markdown("### Welcome to the Business Card Application!")
        st.markdown('### Bizcard is a Python application designed to extract information from business cards. It utilizes various technologies such as :blue[Streamlit, Streamlit_lottie, Python, EasyOCR , RegEx function, OpenCV, and MySQL] database to achieve this functionality.')
        st.write('### The main purpose of Bizcard is to automate the process of extracting key details from business card images, such as the name, designation, company, contact information, and other relevant data. By leveraging the power of OCR (Optical Character Recognition) provided by EasyOCR, Bizcard is able to extract text from the images.')
        st.write("### Click on the ****:red[Image to text]**** option to start exploring the Bizcard extraction.")
        
if selected=='Upload & Extract':
    file,text = st.columns([3,2.5])
    with file:
        uploaded_file = st.file_uploader("Choose an image of a business card", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            file_bytes = uploaded_file.read()
            #original image
            nparr = np.frombuffer(file_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            st.image(image,channels='BGR' ,use_column_width=True)

            #text extraction bounding image 
            if st.button('TEXT BOUNDING'):
                with st.spinner('Detecting text...'):
                    time.sleep(1)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                # Apply threshold to create a binary image
                new, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
                # Find contours in the binary image
                contours,new = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                # Iterate through each contour and draw it with a different color
                for i in contours:
                    # Get the bounding rectangle coordinates
                    x, y, w, h = cv2.boundingRect(i)
                    # Change the text color to green (BGR format)
                    color = (0, 255, 0)
                    # Draw a rectangle around the contour with the specified color
                    new=cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                st.write('Compare the images')
                st.image(new,use_column_width=True)
                st.info('Image might be inaccurate detection of text', icon='ℹ️')
  # This is image details to show them...
    with text:
        left,right = st.tabs(['Undefined text extraction','Pre_defined text extraction'])
        with left:
            st.markdown('##### *Here you can view an undefined text extraction using :red[easyOCR]* and this is advanced tool for random text extraction.')
            st.write("Please note: It will accept all image and further update will available soon!")
            if st.button('RANDOM EXTRACTION'):
                with st.spinner('Extracting text...'):
                    reader =easyocr.Reader(['en'])
                    results = reader.readtext(image)
                    for i in results:
                        st.write(i[1])
    
        with right:
            st.markdown("###### *Press below extract button to view structered text format & upload to database Using :blue[easyOCR] & :blue[python regular expression]*")
            st.write('Please note: This tab only for *:blue[business card image]* alone it will not accept random image')
            if st.button('Extract & Upload'):
                with st.spinner('Exracting text...'):
                    reader=easyocr.Reader(['en'])
                    results = reader.readtext(image)
                    card_info = [i[1] for i in results]
                    demilater = ' '
                    #convert to string
                    card = demilater.join(card_info)
                    replacement =[
                        (",",""),
                        (',',''),
                        ("WWW ", "www."),
                        ("www ", "www."),
                        ('www', 'www.'),
                        ('www.', 'www'),
                        ('wwW', 'www'),
                        ('wWW', 'www'),
                        ('.com', 'com'),
                        ('com', '.com'),
                    ] 
                    for old,new in replacement:
                        card = card.replace(old,new)
                    # Phone Details.
                    ph_pattern = r"\+*\d{2,3}-\d{3}-\d{4}"
                    ph = re.findall(ph_pattern,card)
                    Phone = ''
                    for i in ph:
                        Phone = Phone+' '+i
                        card =card.replace(i, '')
                    
                    # Mail_id
                    mail_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}\b"
                    mail = re.findall(mail_pattern, card)
                    Email_id = ''
                    for ids in mail:
                        Email_id = Email_id + ids
                        card = card.replace(ids, '')
                    
                    # website
                    url_pattern = r"www\.[A-Za-z0-9]+\.[A-Za-z]{2,3}"
                    url = re.findall(url_pattern,card)
                    URL = ''
                    for i in url:
                        URL =URL+i
                        card = card.replace(i,'')
                    # Pincode
                    pin_pattern = r'\d+'
                    match = re.findall(pin_pattern,card)
                    Pincode = ''
                    for i in match:
                        if len(i) == 6 or len(i) ==7:
                            Pincode = Pincode+i
                            card = card.replace(i,'')
                    # name,designation,compan_name.
                    name_pattern = r'^[A-Za-z]+ [A-Za-z]+$|^[A-Za-z]+$|^[A-Za-z]+ & [A-Za-z]+$'
                    name_data = []  # empty list
                    for i in card_info:
                        if re.findall(name_pattern, i):
                            if i not in 'WWW':
                                name_data.append(i)
                                card = card.replace(i, '')
                    name = name_data[0]
                    designation = name_data[1]
                    
                    if len(name_data)==3:
                        company = name_data[2]
                    else:
                        company = name_data[2]+' '+name_data[3]
                    card = card.replace(name,'')
                    card = card.replace(designation,'')
                    #city,state,address
                    new = card.split()
                    if new[4] == 'St':
                        city = new[2]
                    else:
                        city = new[3]
                    # state
                    if new[4] == 'St':
                        state = new[3]
                    else:
                        state = new[4]
                    # address
                    if new[4] == 'St':
                        s = new[2]
                        s1 = new[4]
                        new[2] = s1
                        new[4] = s  # swapping the St variable
                        Address = new[0:3]
                        Address = ' '.join(Address)  # list to string
                    else:
                        Address = new[0:3]
                        Address = ' '.join(Address)  # list to string      
                        
                    st.write('')
                    print(st.write('##### :red[Name]       :',name))
                    print(st.write('##### :red[Designation]:',designation))
                    print(st.write('##### :red[company]    :',company))
                    print(st.write('##### :red[Phone]      :',Phone))
                    print(st.write('###### :red[Email_id]  :',Email_id))
                    print(st.write('###### :red[URL]       :',URL))
                    print(st.write('###### :red[Address]   :',Address))
                    print(st.write('###### :red[city]      :',city))
                    print(st.write('###### :red[state]     :',state))
                    print(st.write('###### :red[Pincode]   :',Pincode))
                    
                    Sql = "INSERT INTO card_data(name,designation,company,contact,email,website,address,city,state,pincode,image)"\
                        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    value = (name,designation,company,Phone,Email_id,URL,Address,city,state,Pincode,file_bytes)
                    mycursor.execute(Sql,value)
                    Mydb.commit()
                    st.success('Text Extracted Successfully Upload to Database',icon="☑️")
navigation,text_process=st.columns([1.2,4.55])
# Database :-
if selected=='Database':
        with st.spinner('Connecting...'):
            time.sleep(1)
        with navigation:
            option = option_menu(None, ['Image data', "Update data", "Delete data"],
                                 icons=["image", "pencil-fill", 'exclamation-diamond'], default_index=0)
        mycursor.execute("SELECT * FROM card_data")
        myresult = mycursor.fetchall()
        #convert into dataframe using pandas
        df=pd.DataFrame(myresult,columns=['id','name','designation','company','contact','email','website','address','city','state','pincode','image'])
        df.set_index('id', drop=True, inplace=True)
        st.write(df)

        # showing the image for selected name and designation
        if option=='Image data':
            left, right = st.columns([2, 2.5])
            with left:
                mycursor.execute("SELECT name,designation FROM card_data")
                rows = mycursor.fetchall()
                row_name = [row[0] for row in rows]   #using list comprehension for loop through where the name and designation
                row_designation = [row[1] for row in rows]
                # Display the selection box
                selection_name = st.selectbox("Select name", row_name)     #selection box for avoiding the user input
                selection_designation = st.selectbox("Select designation", row_designation)
                if st.button('Show Image'):
                    with right:
                        sql = "SELECT image FROM card_data WHERE name = %s AND designation = %s"
                        mycursor.execute(sql, (selection_name, selection_designation))
                        result = mycursor.fetchone()
                        # Check if image data exists
                        if result is not None:
                        # Retrieve the image data from the result
                            image_data = result[0]
                        # Create a file-like object from the image data
                            nparr = np.frombuffer(image_data, np.uint8)
                            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                            st.image(image, channels="BGR", use_column_width=True)
                        if result is None:
                            st.error("Image not found for the given name and designation.")
        #update data in database for selected name and designation
        elif option=='Update data':
            name,new_name=st.columns(2)
            with name:
                # Get the available row IDs from the database
                mycursor.execute("SELECT name,designation FROM card_data")
                rows = mycursor.fetchall()
                row_name = [row[0] for row in rows]
                row_designation = [row[1] for row in rows]

                # Display the selection box
                selection_name = st.selectbox("Select name to update", row_name)
                selection_designation = st.selectbox("Select designation to update", row_designation)
            with new_name:
                # Get the column names from the table
                mycursor.execute("SHOW COLUMNS FROM card_data")
                columns = mycursor.fetchall()
                column_names = [i[0] for i in columns if i[0] not in ['id', 'image','name','designation']]

                # Display the selection box for column name
                selection = st.selectbox("Select specific column to update", column_names)
                new_data = st.text_input(f"Enter the new {selection}")

                # Define the SQL query to update the selected rows
                sql = f"UPDATE card_data SET {selection} = %s WHERE name = %s AND designation = %s"

                # Execute the query with the new values
                if st.button("Update"):
                    mycursor.execute(sql, (new_data, selection_name, selection_designation))
                    # Commit the changes to the database
                    Mydb.commit()
                    st.success("updated successfully",icon="👆")


        #===delete data for selected name and dsignation===
        else:
            left,right=st.columns([2,2.5])
            with left:
                mycursor.execute("SELECT name,designation FROM card_data")
                rows = mycursor.fetchall()    #collecting all the data
                row_name = [row[0] for row in rows]
                row_designation = [row[1] for row in rows]
            # Display the selection box
                selection_name = st.selectbox("Select name to delete", row_name)
            with right:
                selection_designation = st.selectbox("Select designation to delete", row_designation)
            with left:
                if st.button('DELETE'):
                    sql = "DELETE FROM card_data WHERE name = %s AND designation = %s"
                # Execute the query with the values as a tuple
                    mycursor.execute(sql, (selection_name, selection_designation))
                    Mydb.commit()
                    st.success('Deleted successfully',icon='✅')

            st.write('')
            st.markdown('### Result')
            st.write('To provide a user-friendly interface, Bizcard utilizes Streamlit, a Python framework for building interactive web applications. Users can upload business card images through the Streamlit interface, and the application will process the images, extract the information, and display it on the screen. The application also provides options to view, update, and analyze the extracted data directly from the database.')
            st.info('The detected text on image might be inaccurate. Still application under development fixing bugs.There is lot to explore on easyOCR and openCV',icon='ℹ️')

# profile 
if selected == 'Profile':
    col1,col2 = st.columns([3,3],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.subheader(":white[BizCardX Extracting business card Data ]",divider='rainbow')
        st.markdown("""
                    <div style="text-align: justify; font-size: 30px;">
                        <h3 style="color: black;">The objective of this project is to:</h3>
                        <p style="font-size: 25px; text-align: justify;">
                            The main purpose of Bizcard is to automate the process of extracting key details from business card images, such as the name, designation, company, contact information, and other relevant data. By leveraging the power of OCR (Optical Character Recognition) provided by EasyOCR, Bizcard is able to extract text from the images.
                        </p></div>""", unsafe_allow_html=True)
                # Create vertical space using empty containers
        for _ in range(6):
            st.write(" ")
        # Create additional vertical space
        for _ in range(4):
            st.write(" ")

        st.markdown("### :gray[Name:  ] :blue[Dinesh Dhamodharan]")
        st.markdown("### :violet[My Project GitHub link] ⬇️")
        github_url = "https://github.com/DineshDhamodharan24/BizCardX-Extracting-Business-Card-Data-with-OCR"
        button_color = "#781734"
        # Create a button with a hyperlink
        button_html = f'<a href="{github_url}" target="_blank"><button style="font-size: 16px; background-color: {button_color}; color: #fff; padding: 8px 16px; border: none; border-radius: 4px;">GitHub My Phonepe Project</button></a>'
        st.markdown(button_html, unsafe_allow_html=True)
    
    with col2:
        # Create vertical space using empty containers
        for _ in range(21):
            st.write(" ")
        # Create additional vertical space
        for _ in range(10):
            st.write(" ")
        st.markdown("### :gray[Email: ] dineshdin9600@gmail.com")
        st.markdown("### :violet[My LinkedIn] ⬇️")
        linkedin_url = "https://www.linkedin.com/in/dinesh-dhamodharan-2bbb9722b/"
        button_color = "#781734"
        button_html = f'<a href="{linkedin_url}" target="_blank"><button style="font-size: 16px; background-color: {button_color}; color: #fff; padding: 8px 16px; border: none; border-radius: 4px;">My LinkedIn profile</button></a>'
        st.markdown(button_html, unsafe_allow_html=True)