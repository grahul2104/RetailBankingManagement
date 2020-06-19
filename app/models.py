from datetime import datetime
from app import db


class Userstore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128), nullable=False)
    emp_type = db.Column(db.String(5), nullable=False)
    last_login = db.Column(db.DateTime)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Customer(db.Model):

    def generate_id(self):
        last_id = db.session.query(db.func.max(Customer.cust_id)).scalar()
        if last_id is not None:
            return last_id + 1
        return 102030001

    cust_id = db.Column(db.Integer, primary_key=True, default=generate_id)
    ssn_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(128))
    age = db.Column(db.Integer)
    address = db.Column(db.String(128))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    # status = db.relationship('CustomerStatus', lazy='select', backref=db.backref('customer', lazy='joined'), foreign_keys=[cust_id, ssn_id])


class Account(db.Model):

    def generate_id(self):
        last_id = db.session.query(db.func.max(Account.acc_id)).scalar()
        if last_id is not None:
            return last_id + 1
        return 112233001

    acc_id = db.Column(db.Integer, primary_key=True, default=generate_id)
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.cust_id'))
    amount = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(20))
    customer = db.relationship('Customer', lazy='select', backref=db.backref('account', lazy='joined'))


class CustomerStatus(db.Model):
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.cust_id'), primary_key=True)
    ssn_id = db.Column(db.Integer, unique=True, nullable=False)
    status = db.Column(db.String(128))
    message = db.Column(db.String(128))
    customer = db.relationship('Customer', lazy='select', backref=db.backref('customer_status', lazy='joined', uselist=False))
    last_updated = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class AccountStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.cust_id'), nullable=False)
    acc_id = db.Column(db.Integer, db.ForeignKey('account.acc_id'), nullable=False)
    status = db.Column(db.String(128))
    message = db.Column(db.String(128))
    customer = db.relationship('Customer', lazy='select', backref=db.backref('account_status', lazy='joined'))
    account = db.relationship('Account', lazy='select', backref=db.backref('account_status', lazy='joined'))
    last_updated = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class Transactions(db.Model):

    def generate_id(self):
        last_id = db.session.query(db.func.max(Transactions.trans_id)).scalar()
        if last_id is not None:
            return last_id + 1
        return 12300001

    trans_id = db.Column(db.Integer, primary_key=True, default=generate_id)
    acc_id = db.Column(db.Integer, db.ForeignKey('account.acc_id'), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    debit = db.Column(db.Integer, nullable=False)
    credit = db.Column(db.Integer, nullable=False)
    balance = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    account = db.relationship('Account', lazy='select', backref=db.backref('transactions', lazy='joined'))

