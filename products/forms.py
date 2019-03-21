from django import forms
from .models import Product
from django.db.models import Q
from .currencies import get_currency_choices
from commons.validation_messages import (FORM_URL_INVALID, FORM_PRICE_INVALID_DECIMALS,
                                         FORM_PRICE_INVALID_DIGITS_AMOUNT, FORM_CURRENCY_INVALID,
                                         FORM_UNIQUE_USER_AND_PRODUCT_NAME_CONSTRAINT_VIOLATION, FORM_DATE_INVALID)


class AddProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AddProductForm, self).__init__(*args, **kwargs)

    name = forms.CharField(max_length=200, label='Product Name')
    description = forms.CharField(label='Product Description',
                              widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "5", }))
    url = forms.URLField(required=False, label='Link to your product\'s website',
                         error_messages={'invalid': FORM_URL_INVALID})
    price = forms.DecimalField(label='Product\'s price (if it does not require any purchase, please set the value as 0).',
                                       min_value=0,
                                       error_messages={'max_decimal_places': FORM_PRICE_INVALID_DECIMALS,
                                                       'max_digits': FORM_PRICE_INVALID_DIGITS_AMOUNT})
    currency = forms.ChoiceField(choices=get_currency_choices())
    work_start_date = forms.DateField(required=False, widget=forms.SelectDateWidget,
                                      error_messages={'invalid': FORM_DATE_INVALID})
    launch_date = forms.DateField(required=False, widget=forms.SelectDateWidget,
                                  error_messages={'invalid': FORM_DATE_INVALID})

    class Meta:
        model = Product
        fields = ['name', 'description', 'url', 'price', 'currency', 'work_start_date', 'launch_date' ]

    def clean(self):
        cd = self.cleaned_data
        # check if there's no duplicated product name under request's user
        if Product.objects.filter(Q(name=cd['name']) &
                                  Q(owner_id=self.request.user.pk)).exists():
            self.errors['name'] = [FORM_UNIQUE_USER_AND_PRODUCT_NAME_CONSTRAINT_VIOLATION]

        # make sure if there's valid currency selected when price > 0
        if cd['price'] > 0 and cd['currency'] == '-':
            self.errors['currency'] = [FORM_CURRENCY_INVALID]
        return cd
