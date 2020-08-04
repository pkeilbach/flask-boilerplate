from flask import Flask, Markup
from flask import render_template, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime


app = Flask(__name__)
# for wtf forms
app.config['SECRET_KEY'] = 'PK17'
# use local bootstrap files
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
bootstrap = Bootstrap(app)
moment = Moment(app)


class SimpleForm(FlaskForm):
    search_text = StringField('Enter your search term', validators=[DataRequired()])
    submit = SubmitField('Search')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SimpleForm()
    # a simple post/redirect/get pattern
    if form.validate_on_submit():
        session['search_term'] = form.search_text.data
        # we can flash alerts simply like that, see templates/base.html for the html rendering
        message = Markup(f"This form does pretty much nothing but displays your search term: <strong>{form.search_text.data}</strong>")
        flash(message, category='warning')
        # redirect when coming with a post request
        return redirect(url_for('index'))
    return render_template(
        'index.html',
        form=form,
        search_term=session.get('search_term'),  # returns None in case it is not set yet
        current_time=datetime.utcnow()
    )


if __name__ == '__main__':
    app.run(debug=True)
