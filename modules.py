from dataclasses import fields
from app import db,ma
import datetime
from marshmallow import fields
from typing import List


class product(db.Model):
    __tablename__='products'
    sno=db.Column(db.Integer,primary_key=True)
    productid=db.Column(db.Integer,unique=True)
    productdesc=db.Column(db.String)
    price=db.Column(db.Float)
    prd_orders = db.relationship('order', backref='orders', lazy=True)


class order(db.Model):
    __tablename__='orders'
    order_sno=db.Column(db.Integer,primary_key=True)
    order_id=db.Column(db.Integer)
    productid=db.Column(db.Integer,db.ForeignKey('products.productid'))
    quantity=db.Column(db.Integer)
    price=db.Column(db.Float)
    created_date=db.Column(db.DateTime, default=datetime.datetime.now())


class orderschema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=order
        fields=('order_id','quantity','price','created_date')
    price=fields.Decimal(places=2)
    created_date=fields.DateTime(format='%d-%m-%Y %H:%M:%S')

class productschema(ma.SQLAlchemyAutoSchema):  
    class Meta:
        model=product
        fields=('productid','productdesc','prd_orders')
        ordered=True
    
    prd_orders=ma.Nested(orderschema,many=True)


    
