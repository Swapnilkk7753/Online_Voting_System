from flask import Flask,render_template,url_for,redirect,request,session,flash
import sqlite3 as sq
from werkzeug.security import generate_password_hash,check_password_hash
import os


app=Flask(__name__)
app.secret_key="supersecret"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


#Database creation for userinfo
def init_db():
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute('''create table if not exists UserData(id integer primary key autoincrement,Name text not null,UserId integer not null ,Email text not null unique,Password text not null unique,login_type text not null, Registered_Time DATETIME DEFAULT Current_timestamp,filename text,Role text check(Role in ('admin','user')) default 'user') 
                ''')
    conn.commit()
    conn.close()

#Database creation for candidateinfo
def init_db_can():
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute('''create table if not exists CandidateData(id integer primary key autoincrement,C_Name text not null ,Email text not null unique,Registered_Time DATETIME DEFAULT Current_timestamp,Active_status integer default 1,Role text not null,Imagefile text not null, Candidate_Type text,Total_Votes integer default 0 )
                ''')
    conn.commit()
    conn.close()

#Database creation for eventinfo
def init_db_eve():
    conn=sq.connect("EventInfo.db")
    cur=conn.cursor()
    cur.execute('''create table if not exists EventData(id integer primary key autoincrement,E_Title text not null ,E_Type text not null ,E_Date text,S_Time text,E_Time text,Active_status integer default 1,E_Dis text not null )
                ''')
    conn.commit()
    conn.close()

#voterlist
def init_db_votlist():
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute('''create table if not exists VoterData(id integer primary key autoincrement,C_Name text not null ,Email text not null ,Active_status integer default 1,Role text not null)
                ''')
    conn.commit()
    conn.close()


@app.route("/")
def inde():
    init_db_votlist()
    init_db_can()
    init_db()
    init_db_eve()
    return render_template('index.html')
@app.route("/index")
def index():
    return render_template('index.html')
@app.route("/A_result")
def A_result():
    return render_template('A_result.html')
@app.route("/candidate")
def candidate():
    rw=getcandiinfo()
    return render_template('candidate.html',rw=rw)
@app.route("/Image_upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        C_Name=request.form.get("CName")
        C_Type=request.form.get("cantype")
        role=request.form.get("Role")
        email=request.form.get("Email")
        file = request.files["photo"]
        if file:
            filename = file.filename
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        candiinfo(C_Name,role,email,filename,C_Type)
    return redirect(url_for("candidate"))
def candiinfo(n,r,e,i,ty):
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute('insert into CandidateData(C_Name,Role,Email,Imagefile,Candidate_Type) values(?,?,?,?,?)' ,(n,r,e,i,ty) )
    conn.commit()
    conn.close()
def getcandiinfo():
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute('select * from CandidateData')
    return cur.fetchall()
def getcandiinfoby(id):
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute('select * from CandidateData where id=?',(id,))
    return cur.fetchall()
@app.route("/CanDelete",methods=["POST","GET"])
def Candelete():
 if request.method=="POST":
    id=request.form.get("id")
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute('delete from CandidateData where id=?',(id,))
    conn.commit()
    conn.close()
    return redirect(url_for("candidate"))
@app.route("/CanUp/<int:id>",methods=["POST","GET"])
def Canup(id):
    le=getcandiinfoby(id)
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute('update CandidateData set Total_Votes=? where id=?',(le[0][8]+1,id))
    conn.commit()
    conn.close()
    return "success"



@app.route("/contact")
def contact():
    return render_template('contact.html')
@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')
@app.route("/E_results")
def E_results():
    return render_template('E_results.html')
@app.route("/employee")
def employee():
    
    return render_template('employee.html')
#Event creation
@app.route("/event")
def event():
    rw=eveinfodis()
    return render_template("event.html",rw=rw)
@app.route("/SaveEvent",methods=["POST"])
def sevent():
    if request.method=="POST":
        ti=request.form.get("title")
        ty=request.form.get("type")
        dt=request.form.get("date")
        st=request.form.get("stime")
        et=request.form.get("etime")
        di=request.form.get("edis")
        eveinfoins(ti,ty,dt,st,et,di)
        rw=eveinfodis()
    return render_template("event.html",rw=rw)
def eveinfoins(ti,ty,dt,st,et,di):
    conn=sq.connect("EventInfo.db")
    cur=conn.cursor()
    cur.execute('insert into EventData(E_Title,E_Type,E_Date,S_Time,E_Time,E_Dis) values(?,?,?,?,?,?)' ,(ti,ty,dt,st,et,di) )
    conn.commit()
    conn.close()
def eveinfodis():
    conn=sq.connect("EventInfo.db")
    cur=conn.cursor()
    cur.execute('select * from EventData') 
    return cur.fetchall()
@app.route("/EventDelete",methods=["POST","GET"])
def evedelete():
 if request.method=="POST":
    id=request.form.get("id")
    conn=sq.connect("EventInfo.db")
    cur=conn.cursor()
    cur.execute('delete from EventData where id=?',(id,))
    conn.commit()
    conn.close
    return redirect(url_for("event"))

@app.route("/login_A")
def login_A():
    return render_template('login_A.html')
@app.route("/login")
def login():
    return render_template('login.html')
@app.route("/logout_A")
def logout_A():
    return render_template('logout_A.html')
@app.route("/logout")
def logout():
    return render_template('logout.html')
@app.route("/report")
def report():
    return render_template('report.html')
@app.route("/S_results")
def S_results():
    return render_template('S_results.html')
@app.route("/student")
def student():
    return render_template('student.html')
@app.route("/team")
def team():
    return render_template('team.html')
@app.route("/vote")
def vote():
    return render_template('login.html')

#register user
@app.route("/RegisterUser",methods=["POST","GET"])
def RegisterUser():
    if request.method=="POST":
        Name=request.form.get("Name")
        logintype=request.form.get("loginTyper")
        id=request.form.get("UserId")
        Email=request.form.get("Email")
        Password=request.form.get("pass")
        CPassword=request.form.get("cpass")
        file = request.files["photo"]
        if file:
            filename = file.filename
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
       
        if Password==CPassword:
            Hash_pass=generate_password_hash(Password,method='pbkdf2:sha256',salt_length=16)
            conn=sq.connect("UserInfo.db")
            cur=conn.cursor()
            try:
              cur.execute('insert into UserData(Name,Userid,Email,Password,login_type,filename) values(?,?,?,?,?,?)',
                        (Name,id,Email,Hash_pass,logintype,filename))
              conn.commit()
            except sq.IntegrityError:
                return ''' <h1>User already exists<h1>'''
            finally:
              conn.close()
            return redirect(url_for('login'))
        
#login user
@app.route("/LoginUser",methods=["GET","POST"])
def LoginUser():
    if request.method=="POST": 
       id=request.form.get("UserId")
       Password=request.form.get("pass")
       logintype=request.form.get("loginType")
       conn=sq.connect("UserInfo.db")
       cur=conn.cursor()
       conn.commit()
       cond='''select Name,Email,Password , UserId,login_type , filename from UserData where UserId=?'''
       cur.execute(cond,(id,))
       rw=cur.fetchone()
       rwu=getcandiinfo()
       if rw is None:
           return redirect(url_for('login'))
       else:
           if check_password_hash(rw[2],Password):
             session["user"]=rw[0]
             session["Email"]=rw[1]
             session["id"]=rw[3]
             session["logty"]=rw[4]
             vl=voterlistdis(session["user"],session["Email"])
             if logintype==rw[4]:
               if logintype=="student":
                  return render_template("student.html",rw=rw,rwu=rwu,vl=vl,l=len(vl),le=len(voterlistdisall()))
               elif logintype=="employee":
                  return render_template("employee.html",rw=rw,rwu=rwu,vl=vl,l=len(vl),le=len(voterlistdisall()))
    return redirect(url_for('login'))

@app.route("/Voter_List",methods=["POST"])
def voterlist():
  if request.method=="POST":
    r=request.form.get("role")
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute("insert into VoterData(C_Name,Email,Role,Active_status)values(?,?,?,?)",(session["user"],session["Email"],r,0))
    conn.commit()
    conn.close()
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    conn.commit()
    cond='''select Name,Email,Password , UserId,login_type , filename from UserData where UserId=?'''
    cur.execute(cond,(session["id"],))
    rw=cur.fetchone()
    rwu=getcandiinfo()
    vl=voterlistdis(session["user"],session["Email"])
    if session["logty"]=="student":
        return render_template("student.html",rw=rw,rwu=rwu,vl=vl,l=len(vl),le=len(voterlistdisall()))
    return render_template("employee.html",rw=rw,rwu=rwu,vl=vl,l=len(vl),le=len(voterlistdisall()))

def voterlistdis(n,e):
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute("select * from VoterData where C_Name=? and Email=?",(n,e))
    return cur.fetchall()
def voterlistdisall():
    conn=sq.connect("UserInfo.db")
    cur=conn.cursor()
    cur.execute("select * from VoterData")
    return cur.fetchall()

