from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from .forms import AddPostForm
from .forms import AddPostForm2
from adik.models import Adik, Category # adik можно убрать так как в текущем пакете (.#models)
from . forms import ContactForm

# Create your views here.


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        #{'title': "Войти", 'url_name': 'login'}
]

#def index(request):
    #return render(request, 'adik/index.html', {'title': 'Главная страница'})

def index(request):
    posts = Adik.objects.filter(is_published=1)
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
    }
    return render(request, 'adik/index.html', data) # можно и без context просто data 

def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Adik.objects.filter(cat_id=category.pk)
    data = {
        'title': f'Рубрика: {category.name}', # ввеху в названии будет рубика такая та
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
 
    return render(request, 'adik/index.html', context=data)
#Мы здесь вначале проверяем наличие раздела с указанным слагом, если его нет в БД, то #генерируется исключение 404 PageNotFound. Если же рубрика найдена, то выбираются все посты с #помощью менеджера published, у которых категория имеет указанный слаг. Затем формируется #словарь data с передаваемыми данными в шаблон index.html. Причем, в title мы будем отображать #название рубрики. (Список cats_db удалим).  рубрики отображаются с помощью пользовательского #шаблонного тега, прописанного в файле adik_tags.py.    


def show_post(request, post_slug):
    post = get_object_or_404(Adik, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }
 
    return render(request, 'adik/post.html', context=data) 



def about(request):
    posts = Adik.objects.all()
    return render(request, 'adik/about.html', {'posts':posts, 'menu':menu, 'title': 'О сайте'})

# Декоратор login_required-для закрытия страниц от неавторизованных пользователей
# В файле settings.py пропишем параметр LOGIN_URL следующим образом: LOGIN_URL = 'users:login'
@login_required 
def contact(request):
    #return HttpResponse("Обратная связь")
# Теперь, при заходе на страницу нам открывается форма авторизации
    if request.method == 'POST':
        form = ContactForm(request.POST) 
        if form.is_valid():
            form.save() # при успешной валидации сохраняем в базе данных 
        return redirect('home') # при успешной валидации переходим на главную страницу
    
    else:
        form = ContactForm()        
    
    
    return render(request, 'adik/contact.html', {'form': form, 'menu': menu})


def login(request):
    return HttpResponse("Авторизация")

#def addpage(request):
    #return HttpResponse("Добавление статьи") 

def addpage(request):
    # при первом заполнении формы срабатывает GET запрос и корректность заполнения полей
    # формы происходит на уровне браузера если все нормально отправляется уже POST запрос 
    # который проверяется уже на сервере на предмет правильности заполнения при этом 
    # обязательно в самом шаблоне применяется {% csrf_token %}
    if request.method == 'POST':
        form = AddPostForm2(request.POST, request.FILES) # поставили 2 чтоб не было путанницы
        # второй параметр- request.FILES-без него не загружаются фото и картинки
        if form.is_valid():  # в видеоуроке показаны примеры создания различных стандартных
           # пользовательских валидаторов как отдельно по полям так и по форме в целом
            #print(form.cleaned_data)
            
            ## код для класса форм не связанных с моделью
            ##try:
                ##Adik.objects.create(**form.cleaned_data)
                ##return redirect('home')
            ##except:
                ##form.add_error(None, 'Ошибка добавления поста')

             # для связынных с моделью:(одна строчка-form.save())
             # метод save() берет на себя всю проверку корректности записи данных и блок try #except нам уже не нужен. 
            form.save()  # метод для сохранения переданных в БД данных
            return redirect('home') 
    else:
        form = AddPostForm2()
    return render(request, 'adik/addpage.html', {'menu': menu, 'title': 'Добавление статьи', 'form': form}) 
    #Мы здесь используем ORM Django для формирования новой записи в таблице adik и передаем в #метод create() распакованный словарь полученных данных. Так как метод create() может #генерировать исключения, то помещаем его вызов в блок try и при успешном выполнении, #осуществляется перенаправление на главную страницу- статья добавляется.Если же возникли #какие-либо ошибки, то попадаем в блок except и формируем общую ошибку для ее отображения в #форме. метод save() берет на себя всю проверку корректности записи данных и блок try except #нам уже не нужен. В файле settings.py пакета конфигурации в корне проекта указать единую #папку media, в которую будут сохраняться все загружаемые файлы (MEDIA_ROOT = BASE_DIR / #'media'-   в проекте нашемpublic_html/media/photos/год и т.д)            
    
    # КЛАССЫ ПРЕДСТАВЛЕНИЯ:
    # Все классы представлений в Django наследуются от базового класса View. Используем класс #представления с именем AddPage, унаследованный от класса View вместо функции def addpage 
    # (request):

class AddPage(View): #  from django.views import View-импортируем вверху базовый класс View
    # В нем используються два метода:
    #по методу get() мы просто отдаем пустую форму, а по методу post() создаем форму с принятыми #данными, если данные корректны, то сохраняем их в БД и делаем перенаправление на главную #страницу, иначе, возвращаем форму с ранее введенными значениями и списком ошибок ее #заполнения. 
    
    def get(self, request): # не забываем в urls.py отметить путь через класс а не через функцию
        form = AddPostForm2() # форма связанная с моделью
        return render(request, 'adik/addpage.html', {'menu': menu, 'title': 'Добавление статьи', 'form': form})
 
    def post(self, request):
        form = AddPostForm2(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, 'adik/addpage.html', {'menu': menu, 'title': 'Добавление статьи', 'form': form})

        #Выше создавали класс AddPage для отображения формы добавления статей. Но наследовали #его от базового класса View. Так вот, правильнее было бы здесь использовать класс #FormView  еще раз сделаем объявление этого класса изменив немного название на class AddPage2 со следующими атрибутами: 

class AddPage2(FormView): # ЭТИМ КЛАССОМ ЗАМЕНИЛИ ВЕРХНИЙ КЛАС
    form_class = AddPostForm2 # ссылка на класс формы связанной с моделью
    template_name = 'adik/addpage.html' #  маршрут к шаблону для отображения формы
    success_url = reverse_lazy('home') # определяет маршрут перенаправления при успешной #отправке после валидации формы.
    extra_context = { # передаем меню и заголовок как дополнительные парамметры
        'menu': menu,
        'title': 'Добавление статьи',
    }
    def form_valid(self, form): # метод для сохранения в БД
        form.save()
        return super().form_valid(form)
    #Этот метод вызывается только после успешной проверки всех переданных данных формы. Параметр #form – это ссылка на заполненную форму. Поэтому нам остается только вызвать метод save() и #сохранить данные в БД. В конце обязательно нужно записать оператор return с вызовом этого #же метода из базового класса.
    #Здесь только нужно учитывать, что объект формы в шаблон addpage.html передается через #параметр form. Мы именно его использовали. Если указать любое другое имя, то форма, конечно #же, отображаться не будет.  
        
    #Для добавления (то есть, создания) новой статьи мы могли бы вместо FormView использовать #класс CreateView. Давайте это сделаем.
class AddPage3(LoginRequiredMixin, CreateView): # LoginRequiredMixin-для закрытия страниц
    #  будет выполнено перенаправление на форму авторизации. 
    form_class = AddPostForm2
    template_name = 'adik/addpage.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'menu': menu,
        'title': 'Добавление статьи',
    }   # метод def form_valid()   убираем -класс CreateView-берет на себя сохранение в БД
        # Когда мы имеем дело с классами представлений, то здесь вместо декоратора для закытия страниц login_required используется класс минксинов LoginRequiredMixin.
    login_url = '/admin/' # При обращении к закрытой странице выполнится перенаправление на #админ-панель. Если убать то будет выполнено перенаправление на форму авторизации.
        
       
       
        #вместо функции index можно использовать класс представления например AdikHome, который #наследуется от класса TemplateView. Однако можно сделать еще лучше и использовать #другой базовый класс ListView созданный специально для отображения произвольных #списков. Вначале импортируем класс ListView. Пагинация у нас на основе того класса

class AdikHome(ListView):
    model = Adik  # строчка model = Women выбирает все записи из таблицы women и попытается #отобразить их в виде списка, 
    template_name = 'adik/index.html' #  атрибут template_name, которому присваиваем путь к #нужному шаблону
    # По умолчанию, данные из модели Adik, указанной в классе представлений, помещаются в #коллекцию object_list. Мы же в шаблоне обращаемся к переменным со своими именами, которые определили в функции представления index. Например, post содержал список всех записей
    #Если мы ее запишем вместо post, то должно все заработать. Если в шаблоне вместо object_list #мы хотим использовать другое обозначение (имя), то в классе AdiknHome следует прописать #атрибут context_object_name с указанием другого имени переменной: 
    context_object_name = 'posts'
    paginate_by = 3 # пагинация (предусмотрена в классе ListView но если есть базовый то в нем)
    #Если данные зависят от параметров GET-запроса, то для этого следует переопределять метод get_context_data() для педачи в шаблон данных(в других случаях можно метод-extra_context)
    #Здесь дополнительно определен параметр object_list
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['menu'] = menu
        context['cat_selected'] = 0
        return context
    # В файле urls.py закомментиуем путь через функцию и укажем через функцию представления

    # Создаем класс представлений для категорий:

class AdikCategory(ListView):
    template_name = 'adik/index.html'
    context_object_name = 'posts'
    allow_empty = False # при несуществующем слаге выдаст исключение 404
    paginate_by = 3 # пагинация (предусмотрена в классе ListView)
    def get_queryset(self): # функция для выборки записей  
        return Adik.objects.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['title'] = 'Категория - ' + cat.name
        context['menu'] = menu
        context['cat_selected'] = cat.pk
        return context

        #Выборка записей: Здесь первым параметром указано имя cat__slug – это способ обращения к #слагу таблицы category через объект cat модели Adik. Далее, указываем, что поле slug у #категории должно быть равно параметру cat_slug, который мы берем из словаря kwargs #объекта класса AdikCategory. Ключ cat_slug автоматически формируется по шаблону #маршрута (файл adik/urls.py), в котором мы должны вместо функции указать класс #представления

        #Класс для отображения отдельных постов (заменим функцию представления show_post()):
class ShowPost(DetailView):
    model = Adik # такая запись выбирает все записи с таблицы
    template_name = 'adik/post.html'
    slug_url_kwarg = 'post_slug' # чтобы не было исключения так как у нас формируется маршрут с параметром post_slug в файле urls.py
    #по умолчанию класс DetailView в шаблон передает переменную с именем object и переменную с #именем модели (малыми буквами). В нашем примере – это adik. Чтобы указать другое имя #переменной для шаблона, мы в классе ShowPost должны прописать атрибут: 
    context_object_name = 'post' #( иначе пустой пост выдаст)
    #Осталось передать в шаблон заголовок title и пункты главного меню:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        context['menu'] = menu
        return context 

        # ПРИМЕЧАНИЕ: В Джанго есть еще классы UpdateView-для изменения существующих записей
        # DeleteView - для удаления и DataMixin-базовый класс (их не рассматривал так как 
        # изменять и удалять можно и в БД, а базовый класс оставил на потом) 
      
