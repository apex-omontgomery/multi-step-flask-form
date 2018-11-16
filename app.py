from flask import Flask, request, render_template, flash, redirect
from forms import RegistrationForm, AdditionalInformation, MultiStepForm
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
    multi_form = MultiStepForm(forms=[RegistrationForm, AdditionalInformation])

    if request.method == 'POST':
        current_form: Form = multi_form[request.form]

        if current_form.validate():
            try:
                next_form = multi_form.step(request.form)

            except KeyError:
                return redirect('/register_success')

            return render_template('register.html', form=next_form)
        else:
            flash_errors(current_form)
            return render_template('register.html', form=current_form)

    first_form = multi_form.first()

    return render_template('register.html', form=first_form)


if __name__ == '__main__':
    app.run(debug=True)
