from flask import Flask, render_template, request, session, redirect, url_for, flash,send_file
import hashlib
import pandas as pd
from flask_mail import *
import secrets
import os
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import secrets
from werkzeug.utils import secure_filename
from blockchain import *
import mysql.connector
from collections import defaultdict

mydb = mysql.connector.connect(host="localhost",user="root",passwd="",database="directmarketingagriculture",charset='utf8',port=3306)
mycursor = mydb.cursor()


# def mydb():
#     mydb = mysql.connector.connect(host="localhost",user="root",passwd="",database="directmarketingagriculture",charset='utf8',port=3307)
#     mycursor = mydb.cursor()
#     return mycursor,mydb





UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/noti')
def noti():
    return render_template('noti.html')

@app.route("/sellershome")
def sellershome():
    return render_template('sellershome.html')

@app.route("/buyerhome")
def buyerhome():
    return render_template('buyerhome.html')

@app.route("/adminhome")
def adminhome():
    return render_template('adminhome.html')

@app.route("/adminlog", methods=["POST", "GET"])
def adminlog():
    if request.method == "POST":
        username = request.form['email']
        password = request.form['password']
        if username == 'admin@gmail.com' and password == 'admin':
            return render_template('adminhome.html', msg="Login successfull")
        else:
            return render_template('admin.html', msg="Login Failed!!")
    return render_template('admin.html')

@app.route("/sellerslog", methods=["POST", "GET"])
def sellerslog():
    if request.method == "POST":
        semail = request.form['semail']
        password = request.form['password']
        sname = request.form['sname']
        hashedpassword = hashlib.md5(password.encode())
        hashpassword = hashedpassword.hexdigest()
        sql = "select * from sellers where semail='%s' and password='%s'" % (semail, hashpassword)
        mycursor.execute(sql)
        results = mycursor.fetchall()
        if results != []:
            session['sellername'] = sname
            session['sellersemail'] = semail
            flash("Login Successfull, Agricultaure Markiting","Success")
            return render_template('sellershome.html',data=results)
        else:
            flash("Credential's Doesn't Exist","warning")
            return render_template('sellerslog.html',)        
    return render_template('sellerslog.html',)

@app.route("/Sellers", methods=["POST", "GET"])
def Sellers():
    if request.method == "POST":
        sname = request.form['sname']
        semail = request.form['semail']
        password = request.form['password']
        password1 = request.form['Con_Password']
        contact = request.form['mobile']
        address = request.form['address']
        myfile = request.files['myfile']
        filename = myfile.filename
        hashedpassword = hashlib.md5(password.encode())
        hashpassword = hashedpassword.hexdigest()
        
        if password == password1:
            print(password)
            sql="select * from sellers where semail='%s' and password='%s'"%(semail,hashpassword)
            mycursor.execute(sql)
            data=mycursor.fetchall()
            print(data)
            if data==[]:
                path=os.path.join("static/profiles/", filename)
                myfile.save(path)
                profilepath = "static/profiles/"+filename
            print(sname, semail, password, address)
            sql = "insert into sellers(sname,semail,password,contact,address,profile)values(%s,%s,%s,%s,%s,%s)"
            val = (sname, semail, hashpassword , contact, address,profilepath)
            mycursor.execute(sql, val)
            mydb.commit()
            return render_template('sellerslog.html')
        else:
                flash('Details already Exist',"warning")
                return render_template('sellers.html')
        
    return render_template('sellers.html')

@app.route("/forgotpassword",methods=['POST','GET'])
def forgotpassword():
    if request.method=="POST":
        semail = request.form['semail']
        sql = "select * from sellers where semail='%s'"%(semail)
        mycursor.execute(sql)
        data = mycursor.fetchall()
        mydb.commit()
        if data !=[]:
            msg ='valid'
            session['sforgotemail'] = semail
            return render_template('forgotpassword.html',msg=msg)
        else:
            msg="notvalid"
            flash("Provide Valid Email","warning")
            return render_template('sellerslog.html',msg=msg)
    return render_template('forgotpassword.html',msg='check')

@app.route("/updatepassword",methods=['POST','GET'])
def updatepassword():
    if request.method=="POST":
        form = request.form
        semail = session['sforgotemail']
        password = form['password']
        confirmpassword =  form['confirmpassword']
        if password == confirmpassword:
            hashedpassword = hashlib.md5(password.encode())
            hashpassword = hashedpassword.hexdigest()
            sql = "select * from sellers where semail='%s'"%(semail)
            mycursor.execute(sql)
            data = mycursor.fetchall()
            mydb.commit()
            if data:
                sql= "update sellers set password='%s' where semail='%s'"%(hashpassword,session['sforgotemail'])
                mycursor.execute(sql)
                mydb.commit()
                flash("Password Updated Successfully","success")
                return redirect(url_for("sellerslog"))
        else:
             return render_template("sellerslog.html")
         
@app.route("/viewsellerprofile")
def viewsellerprofile():
    sql = "select * from sellers where semail='%s'"%session['sellersemail']
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('sellershome.html', cols=data.columns.values, rows=data.values.tolist())

@app.route("/buyerlog", methods=["POST", "GET"])
def buyerlog():
    if request.method == "POST":
        bemail = request.form['bemail']
        password = request.form['password']
        hashedpassword = hashlib.md5(password.encode())
        hashpassword = hashedpassword.hexdigest()
        sql = "select * from buyers where bemail='%s' and password='%s'" % (bemail, hashpassword)
        mycursor.execute(sql)
        results = mycursor.fetchall()
        if results != []:
            session['buyersemail'] = bemail
            session['buyeraddress'] = results[0][5]
            flash("Login Successfull, Agricultaure Markiting","Success")
            return render_template('buyerhome.html',data=results)
        else:
            flash("Credential's Doesn't Exist","warning")
            return render_template('buyerslog.html')        
    return render_template('buyerslog.html')

@app.route("/Buyers", methods=["POST", "GET"])
def Buyers():
    if request.method == "POST":
        bname = request.form['bname']
        bemail = request.form['bemail']
        password = request.form['password']
        password1 = request.form['Con_Password']
        contact = request.form['mobile']
        address = request.form['address']
        myfile = request.files['myfile']
        filename = myfile.filename
        if password == password1:
            hashedpassword = hashlib.md5(password.encode())
            hashpassword = hashedpassword.hexdigest()
            sql="select * from buyers where bemail='%s' and password='%s'"%(bemail,hashpassword)
            mycursor.execute(sql)
            data=mycursor.fetchall()
            print(data)
            if data==[]:
                path=os.path.join("static/profiles/", filename)
                myfile.save(path)
                profilepath = "static/profiles/"+filename
                print(bname, bemail, password, address)
                sql = "insert into buyers(bname,bemail,password,contact,address,profile)values(%s,%s,%s,%s,%s,%s)"
                val = (bname, bemail, hashpassword, contact, address,profilepath)
                mycursor.execute(sql, val)
                mydb.commit()
                return render_template('buyerslog.html')
            else:
                flash('Details already Exist',"warning")
                return render_template('buyres.html')
        else:
            flash('password not matched')
            return render_template('buyres.html')
    return render_template('buyres.html')

@app.route("/bforgotpassword",methods=['POST','GET'])
def bforgotpassword():
    if request.method=="POST":
        bemail = request.form['bemail']
        sql = "select * from buyers where bemail='%s'"%(bemail)
        mycursor.execute(sql)
        data = mycursor.fetchall()
        mydb.commit()
        if data !=[]:
            msg ='valid'
            session['bforgotemail'] = bemail
            return render_template('bforgotpassword.html',msg=msg)
        else:
            msg="notvalid"
            flash("Provide Valid Email","warning")
            return render_template('buyerslog.html',msg=msg)
    return render_template('bforgotpassword.html',msg='check')

@app.route("/bupdatepassword",methods=['POST','GET'])
def bupdatepassword():
    if request.method=="POST":
        form = request.form
        bemail = session['bforgotemail']
        password = form['password']
        confirmpassword =  form['confirmpassword']
        if password == confirmpassword:
            hashedpassword = hashlib.md5(password.encode())
            hashpassword = hashedpassword.hexdigest()
            sql = "select * from buyers where bemail='%s'"%(bemail)
            mycursor.execute(sql)
            data = mycursor.fetchall()
            mydb.commit()
            if data:
                sql= "update buyers set password='%s' where bemail='%s'"%(hashpassword,session['bforgotemail'])
                mycursor.execute(sql)
                mydb.commit()
                flash("Password Updated Successfully","success")
                return redirect(url_for("buyerlog"))
        else:
            return render_template("buyerslog.html")
    return render_template("buyerslog.html")

@app.route("/viewseller")
def viewseller():
    sql = "select * from sellers"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('viewseller.html', cols=data.columns.values, rows=data.values.tolist())

@app.route("/sellerprofile")
def sellerprofile():
    print("sdvsdkvbkjs")
    print(session['sellersemail'])
    val = (session['sellersemail'])
    sql = "select * from sellers where semail='%s'"%(val)
    
    mycursor.execute(sql,val)
    row = mycursor.fetchall()
    return render_template("sellerprofile.html",rows=row)

@app.route("/buyerprofile")
def buyerprofile():
    
    sql = "select * from buyers where bemail='%s'"%(session['buyersemail'])
    mycursor.execute(sql)
    data = mycursor.fetchall()
    return render_template("buyerprofile.html",rows=data)

@app.route("/aspr/<id>")
def aspr(id=0):
    print(id)
    sql = "select * from sellers where status='pending'"
    mycursor.execute(sql)
    dc = mycursor.fetchall()
    print(dc)
    print("**********")
    semail = dc[0][2]
    password = dc[0][3]
    print(semail, password)
    
    status='Accepted'
    otp="Your File accepted and this is your secret Key :"
    skey = secrets.token_hex(4)
    print("secret key", skey)
    mail_content ='Your request is accepted by Admin and email is :'+ semail + ' ' 
    sender_address = 'appcloud887@gmail.com'
    sender_pass = 'uihywuzqiutvfofo'
    receiver_address = semail
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Decentralized Traceability and Direct Marketing of Agriculture Supply Chains'
    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    
    sql = "update sellers set status='Accepted' where id='%s'" % (id)
    mycursor.execute(sql)
    mydb.commit()
    flash('Admin given the authontication for lender', 'success')
    return redirect(url_for('viewseller'))

@app.route("/rejectseller/<id>")
def rejectseller(id=0):
    print(id)
    sql = "select * from sellers where status='pending'"
    mycursor.execute(sql)
    dc = mycursor.fetchall()
    print(dc)
    print("**********")
    semail = dc[0][2]
    password = dc[0][3]
    print(semail, password)
    
    otp="Your File accepted and this is your secret Key :"
    skey = secrets.token_hex(4)
    print("secret key", skey)
    mail_content ='Your request is Rejected by Admin and email is :'+ semail + ' ' 
    sender_address = 'appcloud887@gmail.com'
    sender_pass = 'uihywuzqiutvfofo'
    receiver_address = semail
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Decentralized Traceability and Direct Marketing of Agriculture Supply Chains'
    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    
    sql = "update sellers set status='Rejected' where id='%s'" % (id)
    mycursor.execute(sql)
    mydb.commit()
    return redirect(url_for('viewseller'))

@app.route("/viewbuyer")
def viewbuyer():
    sql = "select * from buyers"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('viewsbuyer.html', cols=data.columns.values, rows=data.values.tolist())

@app.route("/baspr/<id>")
def baspr(id=0):
    print(id)
    sql = "select * from buyers where status='pending'"
    mycursor.execute(sql)
    dc = mycursor.fetchall()
    print(dc)
    print("**********")
    bemail = dc[0][2]
    password = dc[0][3]
    print(bemail, password)
    
    status='Accepted'
    otp="Your File accepted and this is your secret Key :"
    skey = secrets.token_hex(4)
    print("secret key", skey)
    mail_content ='Your request is accepted by Admin and email is :'+ bemail + ' ' 
    sender_address = 'appcloud887@gmail.com'
    sender_pass = 'uihywuzqiutvfofo'
    receiver_address = bemail
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Decentralized Traceability and Direct Marketing of Agriculture Supply Chains'
    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    
    sql = "update buyers set status='Accepted' where id='%s'" % (id)
    mycursor.execute(sql)
    mydb.commit()
    flash('Admin given the authontication for lender', 'success')
    return redirect(url_for('viewbuyer'))

@app.route("/rejectbuyer/<id>")
def rejectbuyer(id=0):
    print(id)
    sql = "select * from buyers where status='pending'"
    mycursor.execute(sql)
    dc = mycursor.fetchall()
    print(dc)
    print("**********")
    bemail = dc[0][2]
    password = dc[0][3]
    print(bemail, password)
    
    otp="Your File accepted and this is your secret Key :"
    skey = secrets.token_hex(4)
    print("secret key", skey)
    mail_content ='Your request is Rejected by Admin and email is :'+ bemail + ' ' 
    sender_address = 'appcloud887@gmail.com'
    sender_pass = 'uihywuzqiutvfofo'
    receiver_address = bemail
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Decentralized Traceability and Direct Marketing of Agriculture Supply Chains'
    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    
    sql = "update buyers set status='Rejected' where id='%s'" % (id)
    mycursor.execute(sql)
    mydb.commit()
    return redirect(url_for('viewbuyer'))

@app.route("/viewcropprice")
def viewcropprice():
    sql = "select * from cropinfo"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('viewcropprice.html', cols=data.columns.values, rows=data.values.tolist())

@app.route("/updatecrop/<int:id>", methods=["POST", "GET"])
def updatecrop(id=0):
    sql = "select * from cropinfo where id='%s'"%(id)
    mycursor.execute(sql)
    data = mycursor.fetchall()
    print(data)
    return render_template('updatecrop.html',loanid=data[0][0],data=data)

@app.route('/updatecropdetails',methods=["POST","GET"])
def updatecropdetails():
    sql = "select * from sellers where semail='%s'"%(session['sellersemail'])
    mycursor.execute(sql)
    data = mycursor.fetchall()
    address = data[0][5]
    print(data)
    if request.method == "POST":
        cropname = request.form['cropname']
        category = request.form['category']
        mincost = request.form['mincost']
        semail =  session['sellersemail']
        quantity = request.form['quantity']
        Yieldtime = request.form['Yieldtime']
        myfile = request.files['myfile']
        filename = myfile.filename
        totalquantity = quantity
        
        path=os.path.join("static/profiles/", filename)
        myfile.save(path)
        profilepath = "static/profiles/"+filename
        print(cropname,category,mincost,semail,quantity,myfile,filename)
        print(semail)
        sql = "insert into cropprice (cropname, category, mincost, quantity,Yieldtime,myfile,semail,address,totalquantity) values (%s, %s, %s, %s, %s ,%s, %s,%s,%s)"
        val = (cropname,category,mincost,quantity,Yieldtime, profilepath,session['sellersemail'],address,totalquantity)
        mycursor.execute(sql, val)
        mydb.commit()
        return redirect(url_for('viewcropprice'))
    
@app.route("/viewupdates")
def viewupdates():
    sql = "select * from cropprice"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('viewupdates.html', cols=data.columns.values, rows=data.values.tolist())

@app.route('/delete/<id>')
def delete(id=0):
    sql = "delete from cropprice where id='%s' " % (id)
    mycursor.execute(sql)
    mydb.commit()
    return redirect(url_for('viewcropprice'))

@app.route("/viewcrop")
def viewcrop():
    sql = "select * from cropprice where semail='%s'"%(session['sellersemail'])
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('viewcrop.html', cols=data.columns.values, rows=data.values.tolist())

@app.route("/addcropinfo", methods=["POST", "GET"])
def addcropinfo():
    
    if request.method == "POST":
        cropname = request.form['subcategory']
        category = request.form['category']
        Minimumcost = request.form['Minimumcost']
        # Yieldtime = request.form['Yieldtime']
        # semail =  session['sellersemail']
        myfile = request.files['myfile']
        filename = myfile.filename
        
        path=os.path.join("static/profiles/", filename)
        myfile.save(path)
        profilepath = "static/profiles/"+filename
        
        sql = "insert into cropinfo (cropname, category, Minimumcost,myfile) values (%s, %s, %s, %s)"
        val = (cropname, category, Minimumcost,profilepath)
        mycursor.execute(sql, val)
        mydb.commit()
        return redirect(url_for('addcropinfo'))
    return render_template('addcropinfo.html', msg="Crop Details added successfully")

@app.route("/viewcropinfo")
def viewcropinfo():
    sql = "select * from cropprice"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('viewcropinfo.html', cols=data.columns.values, rows=data.values.tolist())

@app.route("/farmerproducts/<category>")
def farmerproducts(category):
    print(category)
    sql=""
    return render_template()
# @app.route("/updatecropinfo/<int:id>", methods=["POST", "GET"])
# def updatecropinfo(id=0):
#     sql = "select * from cropinfo where id='%s'"%(id)
#     mycursor.execute(sql)
#     data = mycursor.fetchall()
#     print(data)
#     return render_template('updatecropinfo.html',id=data[0][0],data=data)

@app.route('/updatecropinfodetails', methods=["POST"])
def updatecropinfodetails():
    if request.method == "POST":
        # Retrieve form data
        id = request.form['id']
        cropname = request.form['subcategory']
        category = request.form['category']
        Minimumcost = request.form['Minimumcost']
        myfile = request.files['myfile']
        filename = myfile.filename
        
        path=os.path.join("static/profiles/", filename)
        myfile.save(path)
        profilepath = "static/profiles/"+filename

        # SQL update statement with WHERE clause
        sql = "UPDATE cropinfo SET cropname=%s, category=%s, Minimumcost=%s, myfile=%s  WHERE id=%s"
        val = (cropname, category, Minimumcost, profilepath, id)

        # Execute the update statement
        mycursor.execute(sql, val)
        mydb.commit()

        # Redirect to the viewcropinfo page after updating
        return redirect(url_for('viewcropinfo'))

# @app.route('/deletecropinfo/<id>')
# def deletecropinfo(id=0):
#     sql = "delete from cropinfo where id='%s' " % (id)
#     mycursor.execute(sql)
#     mydb.commit()
#     return redirect(url_for('viewcropinfo'))

@app.route("/adminsearchproduct",methods=["POST","GET"])
def adminsearchproduct():
    if request.method=="POST":
        
        try:
            searchproduct = request.form['search']    
            sql = "SELECT count(distinct semail),SUM(quantity) FROM cropprice WHERE cropname='%s' OR category='%s'" % (searchproduct, searchproduct)
            data = pd.read_sql_query(sql,mydb)      
            farmer_count = data.values[0][0]
            quantity_count = data.values[0][1]
            newsql = "SELECT * FROM cropprice WHERE cropname='%s' OR category='%s'" % (searchproduct, searchproduct)
            data = pd.read_sql_query(newsql,mydb)

        except:
            searchproduct = request.form['address']
            sql = "SELECT count(distinct semail),SUM(quantity) FROM cropprice WHERE address='%s'"%(searchproduct)
            data = pd.read_sql_query(sql,mydb)      
            farmer_count = data.values[0][0]
            quantity_count = data.values[0][1]
            newsql = "SELECT * FROM cropprice WHERE address='%s'" % (searchproduct)
            data = pd.read_sql_query(newsql,mydb)
        return render_template('viewcropinfo.html', cols=data.columns.values, rows=data.values.tolist(),farmercount=farmer_count,quantity_count=quantity_count)
    return redirect("viewcropinfo")


@app.route("/searchproduct",methods=["POST","GET"])
def searchproduct():
    if request.method=="POST":
        try:
            searchproduct = request.form['search']
            sql = "SELECT count(distinct semail),SUM(quantity) FROM cropprice WHERE cropname='%s' OR category='%s'" % (searchproduct, searchproduct)
            data = pd.read_sql_query(sql,mydb)      
            farmer_count = data.values[0][0]
            quantity_count = data.values[0][1]
            newsql = "SELECT * FROM cropprice WHERE cropname='%s' OR category='%s'" % (searchproduct, searchproduct)
            data = pd.read_sql_query(newsql,mydb)
        except:
            searchproduct = request.form['address']
           
            sql = "SELECT count(distinct semail),SUM(quantity) FROM cropprice WHERE address='%s'" %( searchproduct)
            data = pd.read_sql_query(sql,mydb)      
            farmer_count = data.values[0][0]
            quantity_count = data.values[0][1]
            newsql = "SELECT * FROM cropprice WHERE address='%s'" %(searchproduct)
            data = pd.read_sql_query(newsql,mydb)
        return render_template('viewallcrop.html', cols=data.columns.values, rows=data.values.tolist(),farmer_count=farmer_count,quantity_count=quantity_count)
    return redirect("viewallcrop")

@app.route("/viewallcrop")
def viewallcrop():
    
    sql = "select * from cropprice "
    mycursor.execute(sql)
    data1 = mycursor.fetchall()
    print(data1)
    cropname = data1[0][1]
    address = data1[0][8]
    print(cropname,address)
    print("^^^^^^^^^^^^^^")
    
    sql = "select * from buyers where bemail='%s'"%(session['buyersemail'])
    mycursor.execute(sql)
    all_buyers = mycursor.fetchall()
    address_all = "select * from sellers where address='%s'"%(all_buyers[0][5])
    mycursor.execute(address_all)
    mydata = mycursor.fetchall()
    print(mydata)
    print("###########")
    sql = "select * from cropprice"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    print("*********")
    
    
    # address_all = "select * from sellers where address='%s'"%(all_buyers[0][5])
    # mycursor.execute(address_all)
    # mydata = mycursor.fetchall()
    # print(mydata)
    # print("###########")
    
    
    return render_template('viewallcrop.html',data1=data1,cols=data.columns.values, rows=data.values.tolist())

@app.route("/sendrequest/<int:id>", methods=["POST", "GET"])
def sendrequest(id=0):
    print(id)
    print(session['sellersemail'])
    sql = "select * from cropprice where id='%s'" % (id)
    mycursor.execute(sql)
    data = mycursor.fetchall()
    print(data)
    return render_template('sendcroprequest.html',loanid=data[0][0],data=data)

@app.route('/ordercrop',methods=["POST","GET"])
def ordercrop():
    if request.method == "POST":
        imgfile = request.form['imgfile']
        cropname = request.form['cropname']
        category = request.form['category']
        mincost = int(request.form['mincost'])
        semail =  session['sellersemail']
        bemail = session['buyersemail']
        quantity = int(request.form['quantity'])
        Order = int(request.form['Order'])
        season = request.form['season']
        # myfile = request.files['myfile']
        # myfilename = myfile.filename
        # path=os.path.join("static/profiles/", myfilename)
        # myfile.save(path)
        # profilepath = f"static/profiles/{myfilename}"
        # db,cur = mydb()
        totalquantity =  quantity-Order
        print(totalquantity)

        amount = mincost*Order
        print(amount)

        sql = "INSERT INTO croporder(cropname, category, mincost, quantity, myorder, season,totalquantity, semail,bemail,amount,imgfile) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s,%s,%s)"
        val = (cropname, category, mincost, quantity, Order, season,totalquantity, semail,bemail,amount,imgfile)
        mycursor.execute(sql,val)
        mydb.commit()

        sql="update cropprice set totalquantity='%s' where cropname='%s' and category='%s'"%(totalquantity,cropname, category)
        mycursor.execute(sql)
        

        
        # sql = "UPDATE cropprice SET quantity=%s WHERE id=%s"
        # mycursor.execute(sql, (totaoquantity, id))
        # mydb.commit()

        return redirect(url_for('viewallcrop'))


@app.route("/Viewbuyerrequest")
def Viewbuyerrequest():
    sql = "select * from croporder where semail='" + session['sellersemail'] + "' and status='pending'"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('Viewbuyerrequest.html', cols=data.columns.values, rows=data.values.tolist())

@app.route("/acceptresponse/<id>", methods=["POST", "GET"])
def acceptresponse(id=0):
    print(id)
    sql = "select  * from croporder where id='%s'" % (id)
    mycursor.execute(sql)
    dc = mycursor.fetchall()
    print(dc)
   
    
    sql ="update croporder set status='Accepted' where id='%s'"%(id)
    mycursor.execute(sql)
    mydb.commit() 
    
    return redirect(url_for('Viewbuyerrequest'))

@app.route("/rejectresponse/<id>", methods=["POST", "GET"])
def rejectresponse(id=0):
    print(id)
    sql = "select  * from croporder where id='%s'" % (id)
    mycursor.execute(sql)
    dc = mycursor.fetchall()
    print(dc)
   
    
    sql ="update croporder set status='Rejected' where id='%s'"%(id)
    mycursor.execute(sql)
    mydb.commit() 
    
    return redirect(url_for('Viewbuyerrequest'))

@app.route("/farmeraccepteddata")
def farmeraccepteddata():
    sql = "select * from croporder where status='Accepted' and  semail='" + session['sellersemail'] + "' and status='Accepted'"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template("farmeraccepteddata.html", cols=data.columns.values, rows=data.values.tolist())


@app.route("/accepteddata")
def accepteddata():
    
    
    sql = "select * from croporder where status='Accepted' and  bemail='" + session['buyersemail'] + "' and status='Accepted'"
    data = pd.read_sql_query(sql, mydb)
    

    return render_template('accepteddata.html', cols=data.columns.values, rows=data.values.tolist())

@app.route('/payment/<int:id>', methods=['POST', 'GET'])
def payment(id=0):
    print(id)
    sql = "select * from croporder where id='%s'"%id
    mycursor.execute(sql, mydb)
    data = mycursor.fetchall()
   
    amount = data[0][10]
   
    
    if request.method == 'POST':
        bemail = session['buyersemail']
        Amount = request.form['amount']
        Cardname = request.form['cardname']
        Cardnumber = request.form['cardnumber']
        expmonth = request.form['expmonth']
        cvv = request.form['cvv']
        status = "Completed"
        semail = session['sellersemail']
        sql = "INSERT INTO payment(Email, Amount, Cardname, Cardnumber, expmonth, cvv, semail,status) VALUES (%s, %s,%s, %s, %s, %s, %s,%s)"
        val = (bemail, Amount, Cardname, Cardnumber, expmonth, cvv,semail,status)
        mycursor.execute(sql, val)
        mydb.commit()
        sql = "SELECT * FROM payment"
        mycursor.execute(sql)
        payments = mycursor.fetchall()

        # Create a dictionary to store transactions grouped by user
        transactions_by_user = defaultdict(list)

        for payment_data in payments:
            user_email = payment_data[1]  # Assuming email is the user identifier
            payment_id = payment_data[0]
            timestamp = date.datetime.now()
            data = payment_data[1:]  # Excluding the email field
            transactions_by_user[user_email].append((payment_id, timestamp, data))

        # Generate text files for each user's transactions
        for user_email, transactions in transactions_by_user.items():
            blockchain = Blockchain()
            for transaction in transactions:
                payment_id, timestamp, data = transaction
                block = Block(payment_id, timestamp, data, "")
                blockchain.add_block(block)

            # Generate text file for the user's transactions
            transaction_data = ""
            for block in blockchain.chain:
                transaction_data += f"Block #{block.index}\nTimestamp: {block.timestamp}\nData: {block.data}\nHash: {block.hash}\nPrevious Hash: {block.previous_hash}\n\n"

            file_path = f"static/{bemail}_transactions.txt"
            with open(file_path, "w") as f:
                f.write(transaction_data)


    return render_template("payment.html",id=id,data=data)


@app.route("/viewpayment")
def viewpayment():
    sql = "select * from payment where  semail='" + session['sellersemail'] + "'"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('viewpayment.html', cols=data.columns.values, rows=data.values.tolist())

@app.route("/viewframerpayment")
def viewframerpayment():
    sql = "SELECT id, amount, email, cardname, Cardnumber, expmonth, cvv,status FROM payment"
    data = pd.read_sql_query(sql, mydb)

    print(data)
    return render_template('viewframerpayment.html', cols=data.columns.values, rows=data.values.tolist())

if __name__=="__main__":
    app.run(debug=True)