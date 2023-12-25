from application import app, db
from flask import render_template, flash, redirect, url_for, get_flashed_messages
from application.form import UserInputForm
from application.models import IncomeExpense
import json

import plotly
import plotly.express as px
import pandas as pd


@app.route("/", methods=["GET"])
def index():
    entries = IncomeExpense.query.order_by(IncomeExpense.date.desc()).all()
    return render_template('index.html', title ='index',entries=entries)

@app.route("/dashboard")
def dashboard():
    
    income_vs_expense = db.session.query(db.func.sum(IncomeExpense.amount), IncomeExpense.type).group_by(IncomeExpense.type).order_by(IncomeExpense.type).all()

    dates = db.session.query(db.func.sum(IncomeExpense.amount),IncomeExpense.date).group_by(IncomeExpense.date).order_by(IncomeExpense.date).all()
    
    category_comparison = db.session.query(db.func.sum(IncomeExpense.amount),IncomeExpense.category).group_by(IncomeExpense.category).order_by(IncomeExpense.category).all()

    income_category = []
    for amounts, _ in category_comparison:
        income_category.append(amounts)

    income_expense = []
    for total_amount, _ in income_vs_expense:
        income_expense.append(total_amount)

    over_time_expenditure = []
    dates_labels = []
    for amount, date in dates:
        over_time_expenditure.append(amount)
        dates_labels.append(date.strftime("%m-%d-%Y"))


    category_comparison = db.session.query(db.func.sum(IncomeExpense.amount), IncomeExpense.category).group_by(IncomeExpense.category).order_by(IncomeExpense.category).all()

    # Extract data for the radar chart
    categories = []
    total_amounts = []

    for amount, category in category_comparison:
        categories.append(category)
        total_amounts.append(amount)


   
    return render_template('dashboard.html',
                           income_vs_expenses=json.dumps(income_expense),
                           over_time_expenditure=json.dumps(over_time_expenditure),
                           dates_labels=json.dumps(dates_labels),
                           category_spend = json.dumps(income_category),
                           categories=json.dumps(categories),
                           totalAmounts=json.dumps(total_amounts))


@app.route("/dashboard_plotly")
def dashboard_plotly():
    
    income_vs_expense = db.session.query(db.func.sum(IncomeExpense.amount), IncomeExpense.type).group_by(IncomeExpense.type).order_by(IncomeExpense.type).all()

    # Extract data for the pie chart
    labels = [type for _, type in income_vs_expense]
    values = [total_amount for total_amount, _ in income_vs_expense]

    # Create a pie chart using Plotly Express
    fig = px.pie(names=labels, values=values, title="Income vs Expense Pie Chart")

    #Treemap
     # Query to get total income and expense for each category
    category_comparison = db.session.query(db.func.sum(IncomeExpense.amount), IncomeExpense.category, IncomeExpense.type).group_by(IncomeExpense.category, IncomeExpense.type).all()

    # Extract data for the treemap chart
    df = pd.DataFrame(category_comparison, columns=['amount', 'category', 'type'])


    
    # Chart 2: Line chart showing cumulative income and expense over time
    line_chart = px.line(x=[entry.date for entry in IncomeExpense.query.order_by(IncomeExpense.date)], 
                         y=[entry.amount if entry.type == 'income' else -entry.amount for entry in IncomeExpense.query.order_by(IncomeExpense.date)],
                         labels={'x': 'Date', 'y': 'Cumulative Amount'}, title="Cumulative Income and Expense Over Time")



    # Create a Treemap chart
    treemap_chart = px.treemap(df, path=['type', 'category'], values='amount', title='Income and Expense by Category')

    # Create a Bar Chart with two sub-sections
    bar_chart = px.bar(df, x='category', y='amount', color='type', barmode='group', title='Income and Expense by Category')

    # Convert the Plotly figure to JSON
    pieChartJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    lineChartJSON = json.dumps(line_chart, cls=plotly.utils.PlotlyJSONEncoder)
    treemapChartJSON = json.dumps(treemap_chart, cls=plotly.utils.PlotlyJSONEncoder)
    barChartJSON = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard_plotly.html', pieChartJSON=pieChartJSON, lineChartJSON=lineChartJSON , 
                           treemapChartJSON=treemapChartJSON, barChartJSON=barChartJSON)


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


@app.route("/edit/<int:entry_id>", methods = ["GET", "POST"])
def edit(entry_id):
    entry = IncomeExpense.query.get_or_404(int(entry_id))
    form= UserInputForm(obj=entry)
    if form.validate_on_submit():

        entry.date = form.date.data
        entry.type = form.type.data
        entry.category = form.category.data
        entry.amount = form.amount.data

        db.session.commit()
        flash("Successfully edited",'success')
        return redirect(url_for('index'))
    
    return render_template("edit.html",title='add', form=form)

@app.route("/delete/<int:entry_id>")
def delete(entry_id):
    entry = IncomeExpense.query.get_or_404(int(entry_id))
    db.session.delete(entry)
    db.session.commit()
    flash("Deleted successfully", 'success')
    return redirect(url_for("index"))