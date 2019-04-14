from django import forms
from .models import Product
from django.db.models import Q
from .currencies import get_currency_choices
from commons.validation_messages import (FORM_URL_INVALID, FORM_PRICE_INVALID_DECIMALS,
                                         FORM_PRICE_INVALID_DIGITS_AMOUNT, FORM_CURRENCY_INVALID,
                                         FORM_UNIQUE_USER_AND_PRODUCT_NAME_CONSTRAINT_VIOLATION, FORM_DATE_INVALID)
from django.utils.translation import gettext_lazy as _

class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.action_type = kwargs.pop('action_type', None)
        self.orig_name = kwargs.pop('orig_name', None)
        super(ProductForm, self).__init__(*args, **kwargs)

    name = forms.CharField(max_length=200, label=_('Product Name'))
    description = forms.CharField(label=_('Product Description'),
                              widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "5", }))
    url = forms.URLField(required=False, label=_('Link to your product\'s website'),
                         error_messages={'invalid': FORM_URL_INVALID})
    price = forms.DecimalField(label=_('Product\'s price (if it does not require any purchase, please set the value as 0).'),
                                       min_value=0,
                                       error_messages={'max_decimal_places': FORM_PRICE_INVALID_DECIMALS,
                                                       'max_digits': FORM_PRICE_INVALID_DIGITS_AMOUNT})
    currency = forms.ChoiceField(choices=get_currency_choices(), label=_('Currency'))
    work_start_date = forms.DateField(required=False, widget=forms.SelectDateWidget,
                                      error_messages={'invalid': FORM_DATE_INVALID},
                                      label=_('Work start date'))
    launch_date = forms.DateField(required=False, widget=forms.SelectDateWidget,
                                  error_messages={'invalid': FORM_DATE_INVALID},
                                  label=_('Launch date'))

    class Meta:
        model = Product
        fields = ['name', 'description', 'url', 'price', 'currency', 'work_start_date', 'launch_date' ]

    def clean(self):
        cd = self.cleaned_data
        name_and_user_not_unique = Product.objects.filter(name=cd['name'], owner_id=self.request.user.pk).exists()


        # handle ADD
        if self.action_type == 'ADD' and name_and_user_not_unique:
            self.errors['name'] = [FORM_UNIQUE_USER_AND_PRODUCT_NAME_CONSTRAINT_VIOLATION]

        # handle EDIT
        if self.action_type == 'EDIT' and name_and_user_not_unique and self.orig_name != cd['name']:
            self.errors['name'] = [FORM_UNIQUE_USER_AND_PRODUCT_NAME_CONSTRAINT_VIOLATION]

        # make sure if there's valid currency selected when price > 0
        if cd['price'] > 0 and cd['currency'] == '-':
            self.errors['currency'] = [FORM_CURRENCY_INVALID]
        return cd
