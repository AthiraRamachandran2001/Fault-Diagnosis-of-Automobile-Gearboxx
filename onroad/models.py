from enum import unique
from ssl import _create_unverified_context
from onroad import db,app,login_manager
from flask_login import UserMixin
from flask_table import Table, Col, LinkCol
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(id):
    return Login.query.get(int(id))


user_request=db.Table('user_request',
                      db.Column('uid',db.Integer,db.ForeignKey('login.id')),
                      db.Column('us_id',db.Integer,db.ForeignKey('problems.id')))




class Login(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80), nullable=False)
    usertype = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(200))
    address=db.Column(db.String(200))
    contact = db.Column(db.String(200))
    approve = db.Column(db.String(200))
    reject = db.Column(db.String(200))
    status = db.Column(db.String(200))
    location = db.Column(db.String(200),default='')
    last_service = db.Column(db.String(50),default='')
    next_service = db.Column(db.String(50),default='')
    last_pollution = db.Column(db.String(50),default='')
    next_pollution = db.Column(db.String(50),default='')
    vehicle = db.Column(db.String(50),default='')
    vehicle_no = db.Column(db.String(50),default='')
    service = db.Column(db.String(50),default='')
    st = db.Column(db.String(50),default='')
    uid = db.Column(db.String(50),default='')
    area = db.Column(db.String(50),default='')
  


class Mechanic(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),unique=True)
    email = db.Column(db.String(200),unique=True)
    contact = db.Column(db.String(200))
    location = db.Column(db.String(200))
    password = db.Column(db.String(200))
    cardno = db.Column(db.String(200),unique=True)
    amount =db.Column(db.String(200))
    cvv=db.Column(db.String(200))
    month=db.Column(db.String(200))
    year=db.Column(db.String(200))
    status = db.Column(db.String(200))
   



class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    contact = db.Column(db.String(200))
    address=db.Column(db.String(200))
    password = db.Column(db.String(200))
    cardno = db.Column(db.String(200),unique=True)
    amount =db.Column(db.String(200))
    cvv=db.Column(db.String(200))
    month=db.Column(db.String(200))
    year=db.Column(db.String(200))


class Contact(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))
    email= db.Column(db.VARCHAR)
    message= db.Column(db.String(200))
    contact= db.Column(db.String(200))
    response= db.Column(db.String(200))
    status= db.Column(db.String(200))

 

class Problems(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    msg=db.Column(db.String(200))
    uid=db.relationship("Login",secondary='user_request',backref='test1')
    wid = db.Column(db.String(200))
    m_id = db.Column(db.String(200))
    date = db.Column(db.String(200))
    time = db.Column(db.String(200))
    status = db.Column(db.String(200),default="NULL")


class Response(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    message=db.Column(db.String(200))
    response=db.Column(db.String(200))
    result=db.Column(db.String(200))
    issue=db.Column(db.String(200))
    prblm_id=db.Column(db.String(200))
    status = db.Column(db.String(200),default="NULL")

   



    
    


