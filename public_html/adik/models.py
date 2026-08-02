from django.db import models
# В видеоуроке № 5 подробно описано как в строеннной в django ORM работать с базой данных
from django.urls import reverse
from django.contrib.auth import get_user_model

class Adik(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    #slug = models.SlugField(max_length=255, db_index=True, blank=True, default='') временная
    slug = models.SlugField(max_length=255, db_index=True, unique=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    #photo = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None, blank=True, #null=True, verbose_name="Фото")
    photo = models.ImageField(upload_to="photos/%Y/$m/%d/", verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категории")
    #author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, #related_name='posts', null=True, default=None)
    #Добавление авторства статей. Mы обращаемся к модели User с помощью функции get_user_model
    #(). Это считается предпочтительной практикой для фреймворка Django. Далее, прописываем #параметр on_delete с флагом SET_NULL, то есть, при удалении пользователя поле author будет #содержать значение NULL. Однако не получилось создать миграцию для измененимя -нужно сразу
    #при создании таблицы создать это поле поэтому закомментируем
    ##author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, ##related_name='posts', null=True, default=None)
    #Так как модель изменилась, то нам нужно не забыть создать и применить миграции.

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Программирование' # изменили название в админпанеле   
        verbose_name_plural = 'Программирование' # убрали s в конце(множеств.число)
        ordering = ['time_create'] # если знак спереди минус то очередность на сайте по дате
        indexes = [
            models.Index(fields=['time_create'])  # то же если минус будет
        ] 

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug}) # метод удобен тем что если
        # надо перейти снова на post_id меняем только в этой функции(и в маршрутах) кроме того #стандартная #админ-панель обращается к этому методу для построения ссылок на каждую #запись -появляется кнопка-смотреть на сайте если перейти то будет этот фрагмент #записи     

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True,  verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Категория' # меняем названия на русские
        verbose_name_plural = 'Категории'
 
    def get_absolute_url(self): # self -объект класса модели (запись)
        return reverse('category', kwargs={'cat_slug': self.slug})
 
    def __str__(self):
        return self.name 
            



##class Adikson(models.Model): # Women- произвольное название класса базы данных и таблицы в ней
    # этот класс мы наследуем от базового класса Model (поле id уже  автоматически прописаноо #согласно этого класса)
    ##title = models.CharField(max_length=255, verbose_name="Заголовок") # прописываем остальные #поля models- модуль(файл с кодом который
    # можно использовать   CharField- класс по созданию текстового поля)
    # перечень классов и их характеристики в учебнике по djanco)
    # verbose_name="Заголовок"- для изменения в админпанеле названия на нужное (было title)
    ##slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    # slug добавили в 12 уроке для того чтоб использовать слаги в строке запроса
    # unique=True- означает уникальность поля, db_index=True - поле будет индексировано
    ##content = models.TextField(blank=True, verbose_name="Текст статьи") # класс по созданию #контекста, blank=True- параметр для необязательного заполнения
    ##photo = models.ImageField(upload_to="photos/%Y/$m/%d/", verbose_name="Фото")  # "photos/%Y/#$m/%d/"- путь к каталогу куда будут загружаться фото(
    # каталлоги и подкаталлоги    /%Y/$m/%d/- шаблон сортировки типа год месяц и дата #распределения)
    ##time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания") # #поле- время создания статьи (создается автоматич) auto_now_add=True-при коректировке не #фиксирует
    ##time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")   # поле #-время последнего редактирования статьи(автоматич) auto_now=True-фиксирует изменения
    ##is_published = models.BooleanField(default=True, verbose_name="Публикация")    # создается автоматически так как и здесь значение True
    # cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, #verbose_name="Категории")  # добавленный ключ cat.id(.id-добавляется автоматически)
    ##cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категории")  # #заменили верхнюю
    # PROTECT - запрещается удалять категории на которые есть ссылки в таблице women (class #Women)
    # 'Category'-класс(таблица) ввиде строки так как этот класс определен ниже класса Women ( #если разместить выше то
    # можно писать без ковычек(не как строку), без null=True джанго не добавит ключ так как  #таблица Категории пустая -не создана
    #def __str__(self):
        #return self.title

    #def get_absolute_url(self): # метод для обращения к конкретной записи в базе данных
        #return reverse('post', kwargs={'post_slug': self.slug})   # id и pk поменяли на slug  в #12 уроке

    #class Meta:
        #verbose_name = 'Известные женщины'
        #verbose_name_plural = 'Известные женщины'
        #  ordering = ['-time_create', 'title']  заменили в 18 уроке на:
        #ordering = ['id']  # сортируем записи по id


##class Category(models.Model):  # создаем вторую таблицу Category с двумя полями id (создается #автоматически) и name
    #name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")   #  #db_index=True- означает индексацию поля(поиск будет быстрее)
    ##slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    #def __str__(self):  # метод который возвращает имя категории(name)
        #return self.name

    #def get_absolute_url(self):
        #return reverse('category', kwargs={'cat_slug': self.slug})

    #class Meta:
        #verbose_name = 'Категорию'
        #verbose_name_plural = 'Категории'
        #ordering = ['id']


class Contact(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    message = models.TextField(max_length=1000)

    def __str__(self):
        # Будет отображаться следующее поле в панели администрирования
        return f'Вам письмо от {self.email}'
