from django import forms
from .models import Category
from .models import Adik
from django.forms import ModelForm
from .models import Contact
from django.forms import Textarea

# создают в приложении отдельный файл forms.py.
#  в Django существует специальный класс Form, на базе которого удобно создавать формы, не
# связанные с моделями
# Следующий шаг – объявить класс AddPostForm:
# Для улучшения вида объявляем класс AddPostForm(готовую форму из django), описывающий форму 
# добавления статьи (без привязки к БД)
# здесь тоже желательно атрибут формы  назвать так же, как называются поля в таблице . 
# В последствии нам это облегчит написание кода,  поля модели time_create или time_update нигде # не фигурируют, так как заполняются автоматически. required=False-делает поля не обязательными
# для заполнения(некоторые поля django обязывает заполнять )

#class AddPostForm(forms.Form):
    #title = forms.CharField(max_length=255)
    #slug = forms.SlugField(max_length=255)
    #content = forms.CharField(widget=forms.Textarea(), required=False)
    #is_published = forms.BooleanField(required=False)
    #cat = forms.ModelChoiceField(queryset=Category.objects.all())

# Улучшим форму для восприятия:

# применим атрибут label, который позволяет задавать свои имена(русские)
class AddPostForm(forms.Form): 
    # формируем виджет через класс TextInput и указываем у него стиль оформления form-input
    # initial=True- делает поле is_published с установленной галочкой(статья будет автоматически # опубликованна)
    # (attrs={'cols': 50, 'rows': 5})-если вставить то будут заданы размеоы текстового поля
    # с помощью словаря attrs можно назначать любые атрибуты HTML для соответствующих 
    # тегов.      
    title = forms.CharField(max_length=255, label="Заголовок", widget=forms.TextInput(attrs=
    {'class': 'form-input'}))
    slug = forms.SlugField(max_length=255, label="URL")
    content = forms.CharField(widget=forms.Textarea(), required=False, label="Контент")
    is_published = forms.BooleanField(required=False, initial=True, label="Статус")
    cat = forms.ModelChoiceField(queryset=Category.objects.all(),  empty_label="Категория не выбрана", label="Категории")
    # empty_label-вместо черточек отображались по умолчанию в списке эти фразы

    #Верхний класс-пример использования формы не связанной с моделью. В результате, нам пришлось #в классе AddPostForm дублировать поля, описанные в модели  и, кроме того, вручную #выполнять сохранение данных в таблицу adik. Все это можно автоматизировать, используя #форму в связке с моделью.

    # После того, как форма определена, ее можно использовать в функции представления addpage(). 
    # и отобразить в шаблоне addpage.html

    #когда форма предполагает тесное взаимодействие с какой-либо моделью, то лучше ее напрямую с #ней и связать. ФОРМЫ СВЯЗАННЫЕ С МОДЕЛЬЮ:

    #Перейдем в файл adik/forms.py и класс AddPostForm унаследуем от другого базового класса #ModelForm. А внутри дочернего класса объявим вложенный класс Meta с атрибутами model и #fields: 

    ##class AddPostForm(forms.ModelForm):  # унаследуем от другого базового класса ModelForm
    ##class Meta: # обьявим  вложенный класс Meta с атрибутами model и fields:
       ## model = Adikson # трибут model устанавливает связь формы с моделью
        ##fields = '__all__' # Значение __all__ указывает показывать все поля(fields), кроме #тех, #что заполняются автоматически( без полей time_create и time_update, так как они #наполняются без участия пользователя. ) Однако на практике рекомендуется явно #прописывать список полей, необходимых для отображения в форме, а также у списков #установить свойства empty_label. Затем, чтобы описать стили оформления для каждого #поля, используется атрибут widgets класса Meta В нашем случае это будет выглядеть так:

class AddPostForm2(forms.ModelForm): # class AddPostForm2- чтоб не было путанницы ставим 2
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категории")
    
    class Meta: 
        model = Adik  # импортируем модель (связь с моделью)
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat'] # точно в соответствии с
        #полями в модели иначе ошибка-500
        #fields = '__all__'  # можно и так
        labels = {'slug': 'URL'} # меняем название slug на URL
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }


class ContactForm(forms.ModelForm):

    class Meta:
        # Определяем модель, на основе которой создаем форму
        model = Contact
        # Поля, которые будем использовать для заполнения
        fields = ['first_name', 'last_name', 'email', 'message']
        widgets = {
            'message': Textarea(
                attrs={
                    'placeholder': 'Напишите тут ваше сообщение'
                }
            )
        }
    def __init__(self, *args, **kwargs): # добавил 4.01.2025 ничего не поменялось

        """

        Обновление стилей формы

        """

        super().__init__(*args, **kwargs)

        for field in self.fields:

            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})