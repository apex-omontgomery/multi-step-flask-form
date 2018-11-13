from flask import Flask, request, render_template, flash
from forms import RegistrationForm, AdditionalInformation
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


def select_form(step: int):
    if step == 1:
        return RegistrationForm
    if step == 2:
        return AdditionalInformation


@app.route('/register/<int:step>', methods=['GET', 'POST'])
def register(step: int):
    if request.method == 'POST':
        current_form: Form = select_form(step - 1)(request.form)
        if (current_form.validate()):
            multi_dict = request.args
            for key in multi_dict:
                print(multi_dict.get(key))
                print(multi_dict.getlist(key))
            SelectedForm = select_form(step)
            form = SelectedForm(request.form)

            return render_template('register.html', form=form, next_form=f'/register/{step+1}')
        else:
            flash_errors(current_form)
            return render_template('register.html', form=current_form, next_form=f'/register/{step}')

    SelectedForm = select_form(step)
    first_form = SelectedForm(request.form)

    return render_template('register.html', form=first_form, next_form=f'/register/{step+1}')


if __name__ == '__main__':
    app.run()
