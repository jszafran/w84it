import factory
import factory.fuzzy as fz


class UsersFactory(factory.django.DjangoModelFactory):
    email = fz.FuzzyText(suffix="@w84it.com")
    username = fz.FuzzyText()

    class Meta:
        model = 'users.User'
