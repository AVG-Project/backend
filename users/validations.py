from datetime import datetime
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import string


# uc_letters = [chr(i) for i in range(sys.maxunicode) if chr(i).isupper()]
# print(uc_letters)

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

def code_validation(code):
    min_5 = (len(code) == 5)
    check_str = string.ascii_uppercase + '0123456789'
    if not min_5:
        raise ValidationError(
            'Код лояльности должен содержать 5 символов\т'
            'Формат: FS6B2',
            params={"code": code},
        )

    for symbol in code:
        if symbol not in check_str:
            raise ValidationError(
                'Код лояльности должен быть указан в формате: FS6B2\n'
                'Цифры и заглавные латински буквы.',
                params={"code": code})

