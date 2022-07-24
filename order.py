
from sqlalchemy import func
from app import db
from flask import request
from modules import product,order
import modules


def orders():
    if request.method=='POST':
        if request.is_json:
            data=request.json
            payload =data['orders']
            ordcounter=db.session.query(func.max(order.order_id)).first() 
            nextorder = ordcounter[0]+1 if ordcounter[0] is not None else 1
            for ord in payload:
                prodid,quant    =ord.get("productid"),ord.get("quantity")
                prod=db.session.query(product).filter(product.productid==prodid).first()
                #prod=db.session.query(product).filter(product.productid==prodid).first_or_404(description=f" productid  {prodid} doesnot exists")
                if not prod :
                    return {'statusCode':'E006','Data':f"Product id {prodid} is not avaialble"}
                neword=order(order_id=nextorder, productid=prodid,quantity=quant,price=prod.price*quant)
                db.session.add(neword)
            db.session.commit()
            return {'statusCode':'000','Data': f" Orderid {nextorder}  placed successfully "}
           
        else :
            return "",415