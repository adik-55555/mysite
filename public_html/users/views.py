from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import LoginUserForm, RegisterUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse, reverse_lazy
# Create your views here.

#def login_user(request): <!-- просто как заглушка -->
    #return HttpResponse("login")
   
def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        # вначале создаем форму LoginUserForm с набором принятых данных request.POST
        #Затем, проверяем форму на корректность (валидность) и если проверка проходит, то #создаем временную переменную cd, которая ссылается на очищенные принятые данные формы
        #На основе полей username и password мы пытаемся с помощью функции authenticate() #аутентифицировать пользователя по таблице user БД. Если пользователь с указанной парой #логин/пароль находится в БД и является активным (не забанен, например), то вызывается #ключевая функция login(), которая создает запись в сессии, авторизуя текущего #пользователя на сайте. После этого делается перенаправление на главную страницу. В #случае каких-либо ошибок снова форма отображается в браузере пользователя, предлагая #ему еще раз попробовать ввести логин и пароль. 
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
    else:
        form = LoginUserForm()
    return render(request, 'users/login.html', {'form': form})

    # класс представления для авторизации пользователей (заменим функцию login_user())
    # не забываем изменить маршрут с функции на класс в users/urls.py
class LoginUser(LoginView): 
    form_class = AuthenticationForm  #атрибуту form_class мы присваиваем стандартный класс формы #AuthenticationForm фреймворка Django
    template_name = 'users/login.html'
    extra_context = {'title': "Авторизация"}
    # Изменим адрес перенаправления, переопределив метод get_success_url():
    #def get_success_url(self):
        #return reverse_lazy('home') # на домашнюю страницу
        # Второй вариант(применен) добавить константу в файле settings.py пакета конфигурации
         # mysite:
        # LOGIN_REDIRECT_URL = 'home'  - задает URL-адрес, на который следует перенаправлять 
        # пользователя после успешной авторизации; home-имя маршрута


 
#def logout_user(request):
    #return HttpResponse("logout")
def logout_user(request):  # функция для выхода
    logout(request)
    return HttpResponseRedirect(reverse('users:login')) # используем пространство имен users
    #  если записать (reverse('login'))- то попадем на Login.html приложения adik
 # Класс LogoutView - отдельно не объявляется
 # Класс LogoutView. С его помощью можно заменить функцию представления logout_user(). Если нам #достаточно стандартного поведения, то класс LogoutView можно сразу связать с нужным маршрутом
 #(в файле users/urls.py): path('logout/', LogoutView.as_view(), name='logout'),
 #Переходим на сайт, нажимаем «Выйти» и попадаем на несуществующую страницу.
 #Как нам задать другой адрес для выхода? Для этого можно воспользоваться константой #LOGOUT_REDIRECT_URL, прописав ее в файле settings.py, например, так: 
 #LOGOUT_REDIRECT_URL = 'home'- Теперь мы будем выходить на главную страницу сайта. 

#def register(request):  # функция для регистрации - заменили нижней функцией для улучшения
    #form = RegisterUserForm()
    #return render(request, 'users/register.html', {'form': form})

def register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # создание объекта без сохранения в БД
            #параметром commit=False, который запрещает запись данных непосредственно в БД (хэш)
            user.set_password(form.cleaned_data['password']) # теперь записываем в базу(новый 
            # хэш который джанго  захэширует- переданный пароль)
            user.save() #  формирование объекта пользователя с помощью метода save() формы
            return render(request, 'users/register_done.html') # определяем еще один шаблон
    else:
        form = RegisterUserForm()
    return render(request, 'users/register.html', {'form': form})

# Теперь также заменим функцию представления регистрации на класс в Джанго-CreateView:
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"} # свяжем этот класс с маршрутом register в файле #users/urls.py
    success_url = reverse_lazy('users:login') # перенаправление на страницу авторизации