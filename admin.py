from flask import Flask, render_template, request,redirect,session
from ayurvedic_data import ayurvedic_db  # Import the data from separate file
'''from sqlalchemy import SQLAlchemy'''
import sqlite3 
connection=sqlite3.connect("custemer_log.db",check_same_thread=False)
cur=connection.cursor()
cur.execute("create table if not exists Admin(Full_Name varchar(50),Age int,Email varchar(50),Phone_number int,Username varchar(50),Password varchar(50),Confirm_Password varchar(50))")
app = Flask(__name__)
from flask_mail import Mail,Message
app.config["MAIL_SERVER"]="smtp.gmail.com"
app.config["MAIL_USERNAME"]="usmam510@gmail.com"
app.config["MAIL_PASSWORD"]="ywoe hame khej yxuk"
app.config["MAIL_PORT"]=587
app.config["MAIL_USE_TLS"]=True
mail=Mail(app)
@app.route("/")
def cu_lo():
    return render_template("login_selection.html")
@app.route("/admin_login",methods=["POST","GET"])
def login():
    if request.method=="POST":
        adname=request.form["Username"]
        adpassword=request.form["Password"]
        print(adname,adpassword)
        cur.execute("select * from Admin where Username=?",(adname,) )
        
        patience=cur.fetchone()
        print(patience)
        # password=cur.execute("select Password from Custmer where Username=?",(uname,) )
        # umail=cur.execute("select Email from Custmer where Username=?",(uname,) )
        # print(username,password,umail)
        if ( adname in patience )and (adpassword in patience):
            try:
                '''data=Message(subject="Your Login Sucess Fully",sender="usmam510@gmail.com",recipients=[patience[2],])
                data.body="Welcome to the portel"
                mail.send(data)'''
                return redirect("/admin_dashboard")
            except:
                return "Mail Not Send"
    return render_template("admin_login.html")
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        Fname=request.form["Full Name"]
        age=request.form["Age"]
        email=request.form["Email Address"]
        pnumber=request.form["Phone Number"]
        uname=request.form["Username"]
        passw=request.form["Password"]
        cpass=request.form["Confirm Password"]
        cur.execute("insert into Admin(Full_Name,Age,Email,Phone_number,Username,Password,Confirm_Password)values(?,?,?,?,?,?,?)",(Fname,age,email,pnumber,uname,passw,cpass,))
        connection.commit()
        data=Message(subject="Your REGISTER Sucess Fully",sender="usmam510@gmail.com",recipients=[email,])
        data.body="Welcome to the portel"
        mail.send(data)
        return redirect("/admin_login")
    
    return render_template("register.html")

@app.route('/admin_login')
def index():
    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def dash():
    cur.execute("select * from Custemer")
    data=cur.fetchall()
    return render_template('admin_dashboard.html',cdata=data)
@app.route('/delete',methods=["POST"])
def delt():
    if request.method=="POST":
        uname=request.form["username"]
        cur.execute("delete from Custemer where Username=?",(uname,))
        connection.commit()
        return render_template('admin_dashboard.html')
    

if __name__ == '__main__':
    app.run(debug=True)
