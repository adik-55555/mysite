from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
 
class LoginUserForm(forms.Form):
    # форма не связанная с моделью с двумя полями для ввода логина и пароля:
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class RegisterUserForm(UserCreationForm): #класс формы регистрации связанной с моделью
    #  переопределили базовый класс и немногго добавили см. форму ниже закомментир.
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
 
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }
 
    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email



#class RegisterUserForm(forms.ModelForm): # класс формы регистрации связанной с моделью
    #username = forms.CharField(label="Логин")
    #password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    #password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput)
 
    #class Meta:  # связываем с моделью
        #model = get_user_model()
        #fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
        #labels = {
            #'email': 'E-mail',
            #'first_name': 'Имя',
            #'last_name': 'Фамилия',
        #}
    #def clean_password2(self): # метод для проверки совпадения паролей
        #все методы формы, которые начинаются с префикса clean_ и продолжаются именем поля, #автоматически вызываются при проверке корректности переданных данных. 
        #cd = self.cleaned_data
        #if cd['password'] != cd['password2']:
            #raise forms.ValidationError("Пароли не совпадают!")
        #return cd['password2']

    #def clean_email(self): # проверка на уникальность email
        #email = self.cleaned_data['email']
        #if User.objects.filter(email=email).exists():
            #raise forms.ValidationError("Такой E-mail уже существует!")
        #return email       