from django.urls import reverse_lazy
from django.views.generic import UpdateView
from users.models import User
from .forms import UserCreationForm, UserChangeForm
from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.core.mail import send_mail

# class SignUpView(CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'signup.html'
#     # fields = ('username', 'email', 'password',)

class EditUserDataView(UpdateView):
    model = User
    #form_class = UserChangeForm
    fields = ('first_name','last_name','username',)
    success_url = reverse_lazy('home')
    template_name = 'edit_user_data.html'

    def get_queryset(self):
        return User.objects.filter(email=self.request.user.email)

class SignupView(TemplateView):
    def signup(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                token = account_activation_token.make_token(user)
                send_mail(
                    'w84it - Activate your account',
                    f'''Please activate your account with below link:
                    http://localhost:8000/users/activate/{user.pk}/{token}.''',
                    'w84it@w84it.com',
                    [form.cleaned_data['email']],
                    fail_silently=False
                )
                return render(request, 'user_confirmation_message.html', {'email': form.cleaned_data['email']})
        else:
            form = UserCreationForm()

        return render(request, 'signup.html', {'form': form})

    def activate(request, pk, token):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            user = None
        if user:
            if not user.is_active and account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                return render(request, 'user_account_confirmed.html')
            else:
                print(get_current_site(request))
                return render(request, 'home.html')
        else:
            return render(request, 'user_confirmation_invalid_token.html')
