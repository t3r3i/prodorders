from app import db
from flask import request,jsonify
from modules import product,order, orderschema,productschema
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from marshmallow import ValidationError

reportschemas=productschema(many=True)
def reports():
    if request.method == 'GET':
        if request.authorization:
            if request.authorization.username=='admin' and request.authorization.password=='Password' :
                    currentdate=datetime.now()
                    #currentdate=datetime.now().replace(day=1)  # Starting date of previous three months
                    three_months = currentdate - relativedelta(months=3)
                    three_months_order=db.session.query(product).join(order).filter(order.created_date >=three_months).all()
                    if not three_months_order:
                        return {'statusCode':'000','Data':'No order placed in last three months'}
                    res=reportschemas.dump(three_months_order,many=True)
                    return jsonify(data=res)
            return {'statusCode':'E002','data':'Invalid Credentials'}
        else :
            return {'statusCode':'E001','data':'Missing auhoriziation headers'}