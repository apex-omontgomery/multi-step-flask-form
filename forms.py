from wtforms import Form, StringField, PasswordField, validators, HiddenField
from wtforms import ValidationError
import phonenumbers


class MultiStepForm:
    form_steps = {}

    def __init__(self, forms):
        self.current_form = None
        if not isinstance(forms, list) and not all(isinstance(x, Form) for x in forms):
            raise TypeError('Input for "forms" must be of type List[Form]')

        for index, form in enumerate(forms):
            self.form_steps[index] = self.build_form(form, index)

    def __getitem__(self, form_data):
        form_step = form_data.get('multi_part_step', type=int)
        selected_form = self.form_steps[form_step]
        form_built = selected_form(form_data)
        return form_built

    def step(self, form_data):
        form_step = form_data.get('multi_part_step', type=int)
        selected_form = self.form_steps[form_step + 1]
        form_built = selected_form()
        return form_built

    def first(self):
        return self.form_steps[0]()

    def build_form(self, input_form, input_step: int):
        class SubForm(input_form):
            multi_part_step = HiddenField('multi_part_step', default=input_step)

            def __iter__(self):
                return iter(self._fields[k] for k in self._fields if k is not 'multi_part_step')

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
