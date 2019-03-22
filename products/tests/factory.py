import factory
import factory.fuzzy as fz
from users.tests.factory import UsersFactory
from products.currencies import CURRENCIES

class ProductsFactory(factory.django.DjangoModelFactory):
    owner = factory.SubFactory(UsersFactory)
    name = fz.FuzzyText()
    description = fz.FuzzyText()
    price = 25
    currency = 'USD' # TODO: refactor

    class Meta:
        model = 'products.Product'
