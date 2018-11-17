from wtforms import Form, StringField, PasswordField, validators, HiddenField
from wtforms.form import FormMeta
from wtforms import ValidationError
from werkzeug.local import LocalProxy

import phonenumbers
from flask import flash, render_template


def flash_errors(form: Form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')


class MultiStepForm:
    MULTI_STEP_KEY = 'multi_part_step'

    def __init__(self, forms, final_action=None, form_template=None, validate_error=flash_errors):
        self.form_steps = {}
        self.current_form = None
        self.final_action = final_action
        self.form_template = form_template
        self.validate_error = validate_error

        if not isinstance(forms, list) or not all(isinstance(x, FormMeta) for x in forms):
            raise TypeError('Input for "forms" must be of type List[Form]')

        for index, form in enumerate(forms):
            self.form_steps[index] = self.build_form(form, index, self.MULTI_STEP_KEY)

    def advance(self, request: LocalProxy):

        if not isinstance(request, LocalProxy):
            raise TypeError('value for request is not of type "LocalProxy"')

        if request.method == 'POST':
            current_form: Form = self.increment(request.form)

            if current_form.validate():
                try:
                    next_form = self.increment(request.form, next_val=1)
                except KeyError:
                    return self.final_action

                return render_template(self.form_template, form=next_form)
            else:
                self.validate_error(current_form)
                return render_template(self.form_template, form=current_form)

        return render_template(self.form_template, form=self.increment(request.form))

    def increment(self, form_data, next_val=0):
        if not form_data:
            return self.first()
        form_step = form_data.get(self.MULTI_STEP_KEY, type=int)
        selected_form = self.form_steps[form_step + next_val]
        return selected_form(form_data)

    def first(self):
        return self.form_steps[0]()

    def build_form(self, input_form, input_step: int, step_key: str):
        class SubForm(input_form):
            multi_part_step = HiddenField(step_key, default=input_step)

            def __iter__(self):
                return iter(self._fields[k] for k in self._fields if k is not step_key)

        return SubForm


class RegistrationForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    phone = StringField('Phone', validators=[validators.DataRequired()])

    def validate_phone(form, field):
        if len(field.data) > 16:
            raise ValidationError('Invalid phone number.')
        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            try:
                input_number = phonenumbers.parse("+1" + field.data)
                if not (phonenumbers.is_valid_number(input_number)):
                    raise ValidationError('Invalid phone number.')
            except phonenumbers.phonenumberutil.NumberParseException:
                raise ValidationError('Invalid phone number.')


class AdditionalInformation(Form):
    first_name = StringField('First Name', [validators.Length(min=4, max=25)])
    last_name = StringField('Last Name', [validators.Length(min=6, max=35)])


class SomethingElse(Form):
    mike = StringField('First Name', [validators.Length(min=4, max=25)])
    wilson = StringField('Last Name', [validators.Length(min=6, max=35)])
    first_name = StringField('First Name', [validators.Length(min=4, max=25)])
    last_name = StringField('Last Name', [validators.Length(min=6, max=35)])
