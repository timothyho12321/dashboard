from application import db
from datetime import datetime

class IncomeExpense(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    type=db.Column(db.String(30),default='income',nullable=False)
    category=db.Column(db.String(30), default='rent',nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    amount=db.Column(db.Integer,nullable=False)

    def __str__(self):
        return self.id