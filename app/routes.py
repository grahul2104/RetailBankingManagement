
from flask import request, flash, redirect, url_for, render_template, session, Blueprint
from functools import wraps

from app import db
from app.models import Userstore, Customer, CustomerStatus, Account, AccountStatus, Transactions

main = Blueprint('main', __name__)


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user' in session:
            return func(*args, **kwargs)
        else:
            flash("Login Required", 'error')
            return redirect(url_for('main.login', next=request.path))
    return wrapper


def exec_login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user' in session:
            user = session['user']
            if user['emp_type'] == 'executive':
                return func(*args, **kwargs)
            else:
                flash("Executive Login Required", 'error')
                return redirect(url_for('main.login'))
        else:
            flash("Login Required", 'error')
            return redirect(url_for('main.login', next=request.path))
    return wrapper


def teller_login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user' in session:
            user = session['user']
            if user['emp_type'] == 'teller':
                return func(*args, **kwargs)
            else:
                flash("Cashier/Teller Login Required", 'error')
                return redirect(url_for('main.login'))
        else:
            flash("Login Required", 'error')
            return redirect(url_for('main.login', next=request.path))
    return wrapper


@main.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Userstore.query.filter_by(username=username, password=password).first()
        if user is None:
            flash("Invalid Credentials", 'error')
            return redirect(url_for('main.login'))
        else:
            data = {'id': user.id, 'emp_type': user.emp_type}
            session['user'] = data
            flash("Login Successful", 'success')
            return redirect(url_for('main.home'))

    if 'user' in session:
        return redirect(url_for('main.home'))
    return render_template("login.html")


@main.route('/home')
@login_required
def home():
    return render_template("home.html")


@main.route('/create_customer', methods=['GET', 'POST'])
@exec_login_required
def create_customer():
    if request.method == 'POST':
        ssn_id = request.form.get('ssn_id')
        name = request.form.get('name')
        age = request.form.get('age')
        address = request.form.get('address')
        state = request.form.get('state')
        city = request.form.get('city')
        try:
            customer = Customer(ssn_id=ssn_id, name=name, age=age, address=address, state=state, city=city)
            status = CustomerStatus(ssn_id=ssn_id, status="Active", message="customer created successfully", customer=customer)
            db.session.add(customer)
            db.session.add(status)
            db.session.commit()
            flash("Customer creation initiated successfully", 'success')
        except Exception as e:
            print(e)
            flash("Something Went Wrong", 'error')

    return render_template("create_customer.html")


@main.route('/update_customer', methods=['GET', 'POST'])
@exec_login_required
def update_customer():
    if request.method == 'POST':
        cust_id = request.form.get('cust_id')
        name = request.form.get('name')
        age = request.form.get('age')
        address = request.form.get('address')
        print(cust_id, age, address, name)
        try:
            customer = Customer.query.filter_by(cust_id=cust_id).first()
            customer.name = name
            customer.age = age
            customer.address = address
            customer.customer_status.message = "customer update complete"
            db.session.commit()
            flash("Customer update initiated successfully", 'success')
        except Exception as e:
            print(e)
            flash("Something Went Wrong", 'error')

    user = None
    ssn_id = request.args.get('ssn_id')
    cust_id = request.args.get('cust_id')
    if ssn_id is not None:
        user = Customer.query.filter_by(ssn_id=ssn_id).first()
    if cust_id is not None:
        user = Customer.query.filter_by(cust_id=cust_id).first()
    if (ssn_id or cust_id) and not user:
        flash("User does not exist", 'error')
    return render_template("update_customer.html", user=user)


@main.route('/delete_customer', methods=['GET', 'POST'])
@exec_login_required
def delete_customer():
    if request.method == 'POST':
        cust_id = request.form.get('cust_id')
        try:
            Account.query.filter_by(cust_id=cust_id).delete()
            AccountStatus.query.filter_by(cust_id=cust_id).delete()
            Customer.query.filter_by(cust_id=cust_id).delete()
            CustomerStatus.query.filter_by(cust_id=cust_id).delete()
            db.session.commit()
            flash('Customer deletion initiated successfully', 'success')
        except Exception as e:
            print(e)
            flash("Something Went Wrong", 'error')

    user = None
    ssn_id = request.args.get('ssn_id')
    cust_id = request.args.get('cust_id')
    if ssn_id is not None:
        user = Customer.query.filter_by(ssn_id=ssn_id).first()
    if cust_id is not None:
        user = Customer.query.filter_by(cust_id=cust_id).first()
    if (ssn_id or cust_id) and not user:
        flash("User does not exist", 'error')
    return render_template("delete_customer.html", user=user)


@main.route('/create_account', methods=['GET', 'POST'])
@exec_login_required
def create_account():
    if request.method == 'POST':
        cust_id = request.form.get('cust_id')
        account_type = request.form.get('type')
        amount = request.form.get('amount')
        customer = Customer.query.filter_by(cust_id=cust_id).first()
        if customer is None:
            flash("User does not exist", 'error')
            return redirect(url_for('main.create_account'))
        try:
            account = Account(amount=amount, type=account_type, customer=customer)
            status = AccountStatus(status="Active", message="account creation complete", customer=customer, account=account)
            db.session.add(account)
            db.session.add(status)
            db.session.commit()
            flash("Account creation initiated successfully", 'success')
        except Exception as e:
            print(e)
            flash("Something Went Wrong", 'error')

    return render_template("create_account.html")


@main.route('/delete_account', methods=['GET', 'POST'])
@exec_login_required
def delete_account():
    if request.method == 'POST':
        acc_id = request.form.get('acc_id')
        try:
            AccountStatus.query.filter_by(acc_id=acc_id).delete()
            Account.query.filter_by(acc_id=acc_id).delete()
            db.session.commit()
            flash('Account deletion initiated successfully', 'success')
        except Exception as e:
            print(e)
            flash("Something Went Wrong", 'error')

    accounts = None
    ssn_id = request.args.get('ssn_id')
    cust_id = request.args.get('cust_id')
    if ssn_id is not None:
        customer = Customer.query.filter_by(ssn_id=ssn_id).first()
        if customer:
            cust_id = customer.cust_id
    if cust_id is not None:
        accounts = Account.query.filter_by(cust_id=cust_id).all()
    if (ssn_id or cust_id) and not accounts:
        flash("User does not exist", 'error')
    return render_template("delete_account.html", accounts=accounts)


@main.route('/customer_status')
@exec_login_required
def customer_status():
    rows = CustomerStatus.query.all()
    return render_template("customer_status.html", rows=rows)


@main.route('/account_status')
@exec_login_required
def account_status():
    rows = AccountStatus.query.all()
    return render_template("account_status.html", rows=rows)


@main.route('/account_statement')
@teller_login_required
def account_statement():
    transactions = None
    no_of_transactions = request.args.get('no_of_transactions')
    acc_id = request.args.get('acc_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    print(no_of_transactions, acc_id, start_date, start_date)
    if acc_id and no_of_transactions:
        transactions = Transactions.query.filter_by(acc_id=acc_id).order_by(Transactions.date).limit(no_of_transactions).all()
    if acc_id and start_date and end_date:
        transactions = Transactions.query.filter(Transactions.date >= start_date).filter(Transactions.date <= end_date).filter_by(acc_id=acc_id).order_by(Transactions.date).all()
    return render_template("account_statement.html", transactions=transactions)


@main.route('/withdraw', methods=['GET', 'POST'])
@teller_login_required
def withdraw():
    if request.method == 'POST':
        acc_id = request.form.get('acc_id')
        amount = request.form.get('amount')
        account = Account.query.filter_by(acc_id=acc_id).first()
        if int(account.amount) < int(amount):
            flash("Withdraw not allowed, please choose smaller amount", 'error')
            return redirect(url_for('main.withdraw'))
        try:
            account.amount = int(account.amount) - int(amount)
            transaction = Transactions(debit=amount, credit=" ", balance=account.amount, description="Cash Withdraw", account=account)
            db.session.add(transaction)
            db.session.commit()
            flash("Amount withdrawn successfully", 'success')
        except Exception as e:
            print(e)
            flash("Something Went Wrong", 'error')

    accounts = None
    ssn_id = request.args.get('ssn_id')
    cust_id = request.args.get('cust_id')
    acc_id = request.args.get('acc_id')
    if ssn_id is not None:
        customer = Customer.query.filter_by(ssn_id=ssn_id).first()
        if customer:
            cust_id = customer.cust_id
    if cust_id is not None:
        accounts = Account.query.filter_by(cust_id=cust_id).all()
    if acc_id is not None:
        accounts = Account.query.filter_by(acc_id=acc_id).all()
    if (ssn_id or cust_id or acc_id) and not accounts:
        flash("User does not exist", 'error')
    return render_template("withdraw.html", accounts=accounts)


@main.route('/deposit', methods=['GET', 'POST'])
@teller_login_required
def deposit():
    if request.method == 'POST':
        acc_id = request.form.get('acc_id')
        amount = request.form.get('amount')
        account = Account.query.filter_by(acc_id=acc_id).first()
        try:
            account.amount = int(account.amount) + int(amount)
            transaction = Transactions(debit=" ", credit=amount, balance=account.amount, description="Cash Deposit", account=account)
            db.session.add(transaction)
            db.session.commit()
            flash("Amount deposited successfully", 'success')
        except Exception as e:
            print(e)
            flash("Something Went Wrong", 'error')

    accounts = None
    ssn_id = request.args.get('ssn_id')
    cust_id = request.args.get('cust_id')
    acc_id = request.args.get('acc_id')
    if ssn_id is not None:
        customer = Customer.query.filter_by(ssn_id=ssn_id).first()
        if customer:
            cust_id = customer.cust_id
    if cust_id is not None:
        accounts = Account.query.filter_by(cust_id=cust_id).all()
    if acc_id is not None:
        accounts = Account.query.filter_by(acc_id=acc_id).all()
    if (ssn_id or cust_id or acc_id) and not accounts:
        flash("User does not exist", 'error')
    return render_template("deposit.html", accounts=accounts)


@main.route('/transfer', methods=['GET', 'POST'])
@teller_login_required
def transfer():
    if request.method == 'POST':
        amount = request.form.get('amount')
        source_acc_id = request.form.get('source_acc_id')
        target_acc_id = request.form.get('target_acc_id')
        source_account = Account.query.filter_by(acc_id=source_acc_id).first()
        target_account = Account.query.filter_by(acc_id=target_acc_id).first()
        try:
            if int(source_account.amount) < int(amount):
                flash('Transfer not allowed, please choose smaller amount', 'error')
                return redirect(url_for('main.transfer'))
            source_account.amount = int(source_account.amount) - int(amount)
            target_account.amount = int(target_account.amount) + int(amount)
            transaction1 = Transactions(debit=amount, credit=" ", balance=source_account.amount, description="Transfer to "+target_acc_id, account=source_account)
            transaction2 = Transactions(debit=" ", credit=amount, balance=target_account.amount, description="Transfer from "+source_acc_id, account=target_account)
            db.session.add(transaction1)
            db.session.add(transaction2)
            db.session.add(source_account)
            db.session.add(target_account)
            db.session.commit()
            flash('Amount transfer completed successfully', 'success')
        except Exception as e:
            print(e)
            flash("Something Went Wrong", 'error')

    return render_template("transfer.html")


@main.route('/logout')
@login_required
def logout():
    session.pop('user', None)
    flash('Logout Successful', 'success')
    return redirect(url_for('main.login'))
