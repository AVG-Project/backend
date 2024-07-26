from datetime import datetime
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

phone_regex = RegexValidator(
        regex=r'^\+?1?\d{10,12}$',
        message="Телефон должен быть указан в формате: +7ХХХХХХХХХХ (12 символов).")

def years_range():
    current_year = int(datetime.now().year)
    YEARS = [(current_year - 90) + x for x in range(1, 80)]
    return YEARS



def no_number_in_name(value):
    is_digit_present = any(character.isdigit() for character in value)
    if is_digit_present:
        raise ValidationError(
            'В вашем имени, фамилии или отчестве не должно быть цифр.',
            params={"value": value},
        )

# def mobile_number_min_len(value):
#     if len(value) != 12:
#         raise ValidationError(
#             'Телефон должен быть указан в формате: +7ХХХХХХХХХХ (12 символов).',
#             params={"value": value},
#         )
