from flask import Flask, request, render_template, flash, redirect
from forms import RegistrationForm, AdditionalInformation, MultiStepForm, SomethingElse
from wtforms import Form


app = Flask(__name__)
app.secret_key = 'super secret key'


def flash_errors(form: Form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')


@app.route('/register_success', methods=['GET', 'POST'])
def register_done():
    return render_template('register_done.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    multi_form = MultiStepForm(forms=[RegistrationForm, AdditionalInformation, SomethingElse],
                               final_action=redirect('/register_success'),
                               form_template='register.html')
    thing = request
    return multi_form.advance(request)


if __name__ == '__main__':
    app.run(debug=True)
