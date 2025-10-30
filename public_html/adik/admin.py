from django.contrib import admin
from .models import Adik
from .models import Category
from .models import Contact

# Register your models here.

#admin.site.register(Adik) # регистрируем нашу модель в админ-панеле заменили на декоратор

@admin.register(Adik) # регистрация нижнего класса с помощью функции register:
#добавим в список записей дополнительные поля: id, title, время создания и флаг публикации. Для #этого нужно открыть файл women/admin.py и объявить класс, унаследованный от ModelAdmin: 
class AdikAdmin(admin.ModelAdmin):  # заголовки по колонкам
    list_display = ('id', 'title', 'time_create', 'is_published', 'cat', 'brief_info')
    # в атрибуте list_display указываем список отображаемых полей
    # brief_info- заголовок нового пользовательского поля в админке которого нет в БД
    list_display_links = ('id', 'title') # поля ссылки на переход к таблице изменений 
#Далее добавим сортировку записей по дате их создания и по заголовку с помощью еще одного #атрибута ordering в классе WomenAdmin: 
    ordering = ['time_create', 'title']  # действие расспространяется только на админку
    list_per_page = 5 # пагинация списка изменений в админке
    search_fields = ['title'] # - добавляем поле поиска по заголовкам
    list_filter = ['cat__name', 'is_published']

    @admin.display(description="Краткое описание", ordering='content') # поменяли brief_info
    def brief_info(self, adik: Adik):#для создания нового поля в админке которого нет в БД
        return f"Описание {len(adik.content)} символов." # adik-объект класса Adik и
        # представляет собой конкретную запись из этой модели

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass