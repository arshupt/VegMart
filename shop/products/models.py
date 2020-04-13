from shop import db

from datetime import datetime


class Addproduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2),nullable=False)
    discount = db.Column(db.Integer,default=0)
    stock = db.Column(db.Integer,nullable=False)
    desc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    image_1=db.Column(db.String(150), nullable=False, default='image.jpg')
    image_2=db.Column(db.String(150), nullable=False, default='image.jpg')
    image_3=db.Column(db.String(150), nullable=False, default='image.jpg')

    def __repr__(self):
        return '<Addproduct {}>'.format(self.name)

db.create_all()