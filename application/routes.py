from application import app, db
from flask import render_template, flash, redirect, url_for, get_flashed_messages
from application.form import UserInputForm
from application.models import IncomeExpense

@app.route("/", methods=["GET"])
def index():
    entries = IncomeExpense.query.order_by(IncomeExpense.date.desc()).all()
    return render_template('index.html', title ='index',entries=entries)

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

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