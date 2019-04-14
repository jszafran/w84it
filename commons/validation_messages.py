from django.utils.translation import gettext_lazy as _

FORM_URL_INVALID = _('Enter a valid URL.')
FORM_PRICE_INVALID_DECIMALS = _('Ensure that there are no more than 2 decimal places.')
FORM_PRICE_INVALID_DIGITS_AMOUNT = _('Ensure that there are no more than 11 digits in total.')
FORM_CURRENCY_INVALID = _('Product has price but no currency. Please either set price to 0 or pick currency.')
FORM_UNIQUE_USER_AND_PRODUCT_NAME_CONSTRAINT_VIOLATION = _('You already have product registered under such name. Pick another one!')
FORM_DATE_INVALID = _('Enter a valid date.')

