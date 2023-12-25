from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField, DateField
from wtforms.validators import DataRequired, ValidationError, NumberRange

class UserInputForm(FlaskForm):
    type = SelectField('Type',validators=[DataRequired()],
                          choices=[('income','income'),
                                    ('expense','expense')])
    date = DateField('Date', validators=[DataRequired()])
    
    category = SelectField('Category',validators=[DataRequired()],
                          choices=[('rent','rent'),
                                    ('salary','salary'),
                                    ('investment','investment'),
                                    ('side_hustle','side_hustle')])
    
    amount = IntegerField('Amount',validators=[DataRequired(), NumberRange(min=None, max=None, message="Invalid amount")])


    submit= SubmitField("Submit Report")

    # def validate_amount(self,field):
    #     if self.type.data == 'income' and field.data<0:
    #         raise ValidationError('Amount has to be postive for the income type.')
    #     elif self.type.data == 'expense' and field.data>0:
    #         raise ValidationError('Amount has to be negative for the expense type.')
    