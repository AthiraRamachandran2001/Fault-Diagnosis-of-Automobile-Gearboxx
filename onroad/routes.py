from msilib.schema import File
from flask import Flask, render_template, request, redirect,send_file,  flash, abort, url_for
from onroad import app,db,mail
from onroad import app,db,mail
from onroad import app
from onroad.models import *
from onroad.forms import *
from flask_login import login_user, current_user, logout_user, login_required
from random import randint
import os
from PIL import Image
from flask_mail import Message
from io import BytesIO
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
# from datetime import datetime as dt
from datetime import datetime,date
# from datetime import timedelta
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = 'C:/Users/FAB 1/Desktop/CARPAD-AN ONROAD WEBSITE/onroad/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from datetime import datetime, timedelta


from tensorflow import keras
import pandas as pd
# from collections.abc import Iterable


@app.route('/prediction',methods=['GET', 'POST'])
def prediction():
    
    if request.method == "POST":
        
        a1 = request.form['a1']
        a2 = request.form['a2']
        a3 = request.form['a3']
        a4 = request.form['a4']
        load = request.form['load']
           
        model_1 = keras.models.load_model('onroad/model')
        
        fault_labels = {
            0 :'healthy',
            1 : 'faulty'}

        input_dict = {"a1": [float(a1)], "a2": [float(a2)], "a3":[float(a3)], "a4":[float(a4)], "load": [float(load)]}

        input_df = pd.DataFrame.from_dict(input_dict)
        y_pred= model_1.predict(input_df)
        prediction = y_pred[0][0]

        if prediction >0.5: 
            prediction_class = 1
        else:
            prediction_class = 0
        prediction_label = fault_labels[prediction_class]
        output=prediction_label
        print(prediction_label)
        return render_template("output.html",output=output)
    return render_template("prediction.html")








@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/admin_index')
def admin_index():
    return render_template("admin_index.html")





@app.route('/user_index/<id>')
def user_index(id):
    return render_template("user_index.html")



@app.route('/mechanics_index/<id>')
def mechanics_index(id):
    return render_template("mechanics_index.html")



@app.route('/mechanic_index/<id>')
def mechanic_index(id):
    return render_template("mechanic_index.html")





@app.route('/')
def index():
   
    return render_template("index.html")




@app.route('/login', methods=["GET","POST"])
def login():


   
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        admin = Login.query.filter_by(username=username, password=password,usertype= 'admin').first()
        mechanic=Login.query.filter_by(username=username,password=password, usertype= 'workshop',approve='Approved').first()
        mechanics=Login.query.filter_by(username=username,password=password, usertype= 'mechanic').first()
         
        user=Login.query.filter_by(username=username,password=password, usertype= 'user').first()
           
        if admin:
            login_user(admin)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/admin_index') 
        
             
        elif mechanic:
            login_user(mechanic)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/mechanic_index/'+str(mechanic.id))

        elif mechanics:
            login_user(mechanics)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/mechanics_index/'+str(mechanics.id))


         
        elif user:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/user_index/'+str(user.id)) 
        else:
            d="Invalid Username or Password!"
            return render_template("login.html",d=d)


    
    return render_template("login.html")

          
     
    








@app.route('/user_register',methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        address = request.form['address']
        password = request.form['password']
        cardno = request.form['cardno']
        cvv = request.form['cvv']
        month = request.form['month']
        year = request.form['year']
        amount = request.form['amount']
        my_data = User(name=name,email=email,address=address,contact=contact,password=password,cardno=cardno,cvv=cvv,month=month,year=year,amount=amount)
        my_data1 = Login(name=name,username=email,address=address,contact=contact,password=password,usertype="user")
        db.session.add(my_data) 
        db.session.add(my_data1) 
        db.session.commit()
        flash("Registered successfully! Please Login..")
        return redirect('/login')
        
    else :
        return render_template("user_register.html")




@app.route('/mech_register',methods=['GET', 'POST'])
def mech_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        location = request.form['location']
        password = request.form['password']
        cardno = request.form['cardno']
        cvv = request.form['cvv']
        month = request.form['month']
        year = request.form['year']
        amount = request.form['amount']
        area = request.form['area']
        my_data = Mechanic(name=name,email=email,location=location,contact=contact,password=password,cardno=cardno,cvv=cvv,month=month,year=year,amount=amount,status="workshop")
        my_data1 = Login(name=name,username=email,location=location,contact=contact,password=password,usertype="workshop",approve="Approve",reject="Reject",status="workshop",area=area)
        db.session.add(my_data) 
        db.session.add(my_data1) 
        db.session.commit()
        # m_sendmail(email)    
        d="Your Registeration will be confirmed soon.."
        return render_template("mech_register.html",d=d)
        
    else :
        return render_template("mech_register.html")






@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')



@app.route('/approve/<int:id>')
def approve(id):
    c= Login.query.get_or_404(id)
    c.approve = "Approved"
    c.reject="Reject"
    db.session.commit()
    # a_sendmail(c.username)
    return redirect('/admin_view_mechanics')





@app.route('/reject/<int:id>')
def reject(id):
    c= Login.query.get_or_404(id)
    c.reject = 'Rejected'
    c.approve="Approve"
    db.session.commit()
    # r_sendmail(c.username)
    return redirect('/admin_view_mechanics')





@login_required
@app.route('/admin_view_mechanics',methods=["GET","POST"])
def admin_view_mechanics():
    obj = Login.query.filter_by(usertype="workshop",status="workshop").all()
    return render_template("admin_view_mechanics.html",obj=obj)








@login_required
@app.route('/user_view_mechanics',methods=["GET","POST"])
def user_view_mechanics():
    search = request.args.get('search')
    if search:
        obj=Login.query.filter((Login.location.contains(search)| Login.area.contains(search))  & Login.usertype.contains("workshop") )
    else:
        obj = Login.query.filter_by(usertype="workshop",approve="Approved").all()
    return render_template("user_view_mechanics.html",obj=obj)






@login_required
@app.route('/admin_view_users',methods=["GET","POST"])
def admin_view_users():
    obj = User.query.all()
    return render_template("admin_view_users.html",obj=obj)



@app.route('/admin_add_mechanics',methods=['GET', 'POST'])
def admin_add_mechanics():
    if request.method == 'POST':
        a=current_user.id
        print(a)
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        location = request.form['location']
        password = request.form['password']
        area = request.form['area']
        my_data = Mechanic(name=name,email=email,location=location,contact=contact,password=password,status="admin")
        my_data1 = Login(name=name,username=email,location=location,contact=contact,password=password,usertype="mechanic",approve="Approved",status="admin",uid=a,area=area)
        db.session.add(my_data) 
        db.session.add(my_data1) 
        db.session.commit()
        # ad_sendmail(email,password)
        # flash("Registered successfully! Please Login..")
        return redirect('/admin_mechanics')
        
    else :
        return render_template("admin_add_mechanics.html")






@login_required
@app.route('/admin_mechanics',methods=["GET","POST"])
def admin_mechanics():
    obj = Login.query.filter_by(usertype="mechanic",status="admin",approve="Approved",uid=current_user.id).all()
    return render_template("admin_mechanics.html",obj=obj)





@app.route('/delete_mechanic/<int:id>')
@login_required
def delete_mechanic(id):
    delet = Login.query.get_or_404(id)
    # d=Mechanic.query.get_or_404(delet.id)
    try:
        db.session.delete(delet)
        # db.session.delete(d)
        db.session.commit()
        return redirect('/admin_mechanics')
    except:
        return 'There was a problem deleting that task'



@app.route('/contact', methods = ['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        my_data = Contact(name=name, email=email,message=message)
        db.session.add(my_data) 
        db.session.commit()
        return redirect('/')
    else :
        return render_template("contact.html")




@login_required
@app.route('/user_contact/<id>', methods = ['GET','POST'])
def user_contact(id):
    d=Login.query.filter_by(id=id).first()
 
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        contact = request.form['contact']
        my_data = Contact(name=name, email=email,message=message,contact=contact)
        db.session.add(my_data) 
        db.session.commit()
   
        return redirect('/user_index/'+str(current_user.id))
    else :
        return render_template("user_contact.html",d=d)




@login_required
@app.route('/mech_contact/<id>', methods = ['GET','POST'])
def mech_contact(id):
    d=Login.query.filter_by(id=id).first()
 
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        my_data = Contact(name=name, email=email,message=message)
        db.session.add(my_data) 
        db.session.commit()
        return redirect('/mechanic_index/'+str(current_user.id))
    else :
        return render_template("mechanic_contact.html",d=d)









@login_required
@app.route('/admin_view_feedbacks',methods=["GET","POST"])
def admin_view_feedbacks():
    obj = Contact.query.all()
    return render_template("admin_view_feedbacks.html",obj=obj)





@app.route('/user_profile/<int:id>',methods=["GET","POST"])
@login_required
def user_profile(id):
    d = Login.query.get_or_404(id)
    return render_template("user_profile.html",d=d)






@app.route('/edit_profile/<int:id>',methods=["GET","POST"])
@login_required
def edit_profile(id):
    d = Login.query.get_or_404(id)
    if request.method == 'POST':
        
        d.name = request.form['name']
        d.address = request.form['address']
        d.username = request.form['username']
        d.contact = request.form['contact']
        db.session.commit()
        return redirect('/user_profile/'+str(d.id))
    return render_template("edit_profile.html",d=d)





@app.route('/change_password/<int:id>',methods=["GET","POST"])
@login_required
def change_password(id):
    d = Login.query.get_or_404(id)
    if request.method == 'POST':
        
        d.password = request.form['password']
        db.session.commit()
        return redirect('/pswd_success')
    return render_template("change_password.html",d=d)



@app.route('/add_msg/<id>',methods=['GET', 'POST'])
def add_msg(id):
    w=Login.query.filter_by(id=id).first()
    f=Login.query.filter_by(id=current_user.id).first()
    if request.method == 'POST':
        today = date.today()
        now=datetime.now()
        current_time=now.strftime("%H:%M:%S")
        msg = request.form['msg']
        my_data = Problems(msg=msg,uid=[f],wid=w.id,date=today,time=current_time)
        db.session.add(my_data) 
        db.session.commit()
        return redirect('/user_index/'+str(id))

    return render_template("add_msg.html")



@login_required
@app.route('/vw_msg',methods=["GET","POST"])
def vw_msg():
    
    obj = Problems.query.filter_by(wid=current_user.id,status="NULL").all()
    return render_template("vw_msg.html",obj=obj)



@app.route('/add_assign/<id>',methods=['GET', 'POST'])
def add_assign(id):
    msg=Problems.query.filter_by(id=id).first()
    a=Login.query.filter_by(usertype="mechanic",uid=current_user.id).all()
    if request.method == 'POST':
        
        msg.m_id=request.form['mid']
      
        msg.status = "assigned"
        
        db.session.commit()
        return redirect('/mechanic_index/'+str(id))

    return render_template("add_assign.html",msg=msg,a=a)



@app.route('/add_email/<id>',methods=['GET', 'POST'])
def add_email(id):
    e=Login.query.filter_by(id=id).first()
    if request.method == 'POST':
        message=request.form['message']
        cnt_mail(message,e.username)
    return render_template("add_email.html")



def cnt_mail(message,username):

    msg = Message('Notification from Mechanics',
                  recipients=[username])
    msg.body = f'''{message} '''

    mail.send(msg)

    



@app.route('/vw_messages',methods=["GET","POST"])
@login_required
def vw_messages():
    d = Problems.query.filter_by(m_id=current_user.id).all()
    return render_template("view_messages.html",d=d)




@app.route('/add_response/<id>',methods=['GET', 'POST'])
def add_response(id):
    
    if request.method == 'POST':

        res=Problems.query.filter_by(id=id).first()


        response = request.form['response']
        result = request.form['result']
        issue = request.form['issue']

        my_data = Response(response=response,result=result,issue=issue,prblm_id=res.id)
     
        db.session.add(my_data)
     
        db.session.commit()
        
        return render_template('add_response.html',res=res)
    else :
        return render_template("add_response.html")



@app.route('/vw_complaints/<id>',methods=["GET","POST"])
@login_required
def vw_complaints(id):

    d = Login.query.filter_by(id=id).first()
    
    c = Problems.query.filter_by(wid=d.id).all()

    return render_template("vw_complaints.html",d=d,c=c)

@app.route('/vw_response/<id>',methods=["GET","POST"])
@login_required
def vw_response(id):

    c = Response.query.filter_by(prblm_id=id).all()

    return render_template("vw_response.html",c=c)


@app.route('/vw_feedback',methods=["GET","POST"])
@login_required
def vw_feedback():

    obj = Contact.query.all()

    return render_template("vw_feedback.html",obj=obj)