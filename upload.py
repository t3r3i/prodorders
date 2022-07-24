from app import db
from flask import request
import pandas as pd
from werkzeug.utils import secure_filename
from modules import product
import modules


ALLOWED_EXTENSIONS = {'csv'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload():
    if request.method == 'POST':
        if request.authorization:
                if request.authorization.username=='admin' and request.authorization.password=='Password' :
                    if 'file' not in request.files:
                        return {'statusCode':'E003','data':'Missing File Parameter'}
                    file = request.files['file']
                    if file.filename == '':
                        return {'statusCode':'E004','data':'File not found'}
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        df = pd.read_csv(request.files.get('file'))
                        df.columns = [c.lower() for c in df.columns]
                        for i in range(len(df)):
                            print(df.loc[i,'productid'])
                            #prod=product.query.filter(product.productid==df.loc[0,'productid']).first_or_404(description=f"There is no product with {df.loc[0,'productid']}")
                            prod=db.session.query(modules.product).filter(modules.product.productid==df.loc[i,'productid']).first()
                            prodid,prodname,price=df.loc[i]
                            if not prod : 
                                prodrec=modules.product(productid=int(prodid),productdesc=prodname,price=price)
                                db.session.add(prodrec)
                                db.session.commit()
                            else :
                                prod.price=price
                                prod.productdesc=prodname
                                db.session.add(prod)
                                db.session.commit()
                        return {'statusCode':'000','data':f'uploaded {i+1} products information successfully'}  
                    return {'statusCode':'E005','data':'Invalid file format'}
                return {'statusCode':'E002','data':'Invalid Credentials'}
        else :
            return {'statusCode':'E001','data':'Missing auhoriziation headers'}