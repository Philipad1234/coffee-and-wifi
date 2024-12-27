from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe Name', validators=[DataRequired()])
    location = StringField('Cafe location on Google Maps(URL)', validators=[DataRequired()])
    open_time = StringField('Opening time e.g. 9AM', validators=[DataRequired()])
    closing_time = StringField('Closing time e.g. 5:30PM', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee rating',
                                choices=[('✘'), ('☕️'), ('☕️☕️'), ('☕️☕️☕️'), ('☕️☕️☕️☕️'), ('☕️☕️☕️☕️☕️')],
                                validators=[DataRequired()])
    wifi_rating = SelectField('Wifi strength rating', choices=[('✘'), ('💪'), ('💪💪'), ('💪💪💪'), ('💪💪💪💪'), ('💪💪💪💪💪')],
                              validators=[DataRequired()])
    power_outlet_rating = SelectField('Power outlet rating',
                                      choices=[('✘'), ('🔌'), ('🔌🔌'), ('🔌🔌🔌'), ('🔌🔌🔌🔌'), ('🔌🔌🔌🔌🔌')],
                                      validators=[DataRequired()])
    submit = SubmitField('Submit')



# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['POST', 'GET'])
def add_cafe():
    form = CafeForm()
    new_row = []
    if form.validate_on_submit():
        print("True")
        with open('cafe-data.csv', 'a', newline='', encoding='utf-8') as csv_file:
            for data in form.data.values():
                new_row.append(data)
            final_list = new_row[:-2]
            csv_data = csv.writer(csv_file, delimiter=',')
            csv_data.writerow(final_list)
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
