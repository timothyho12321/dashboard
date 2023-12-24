from application import app, db
from flask import render_template, flash, redirect, url_for, get_flashed_messages
from application.form import UserInputForm
from application.models import IncomeExpense
import json

@app.route("/", methods=["GET"])
def index():
    entries = IncomeExpense.query.order_by(IncomeExpense.date.desc()).all()
    return render_template('index.html', title ='index',entries=entries)

@app.route("/dashboard")
def dashboard():
    
    income_vs_expense = db.session.query(db.func.sum(IncomeExpense.amount), IncomeExpense.type).group_by(IncomeExpense.type).order_by(IncomeExpense.type).all()

    income_expense = []
    for total_amount, _ in income_vs_expense:
        income_expense.append(total_amount)
   
    return render_template('dashboard.html',
                           income_vs_expenses=json.dumps(income_expense))

@app.route("/add", methods =["GET", "POST"])
def add_expense():

    form= UserInputForm()
    if form.validate_on_submit():
        entry = IncomeExpense(type=form.type.data, amount= form.amount.data,
                              category=form.category.data)
        db.session.add(entry)
        db.session.commit()
        flash("Successfully added",'success')
        return redirect(url_for('index'))
    
    return render_template("add.html",title='add', form=form)

@app.route("/delete/<int:entry_id>")
def delete(entry_id):
    entry = IncomeExpense.query.get_or_404(int(entry_id))
    db.session.delete(entry)
    db.session.commit()
    flash("Deleted successfully", 'success')
    return redirect(url_for("index"))