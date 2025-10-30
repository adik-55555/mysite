from django import template
import adik.views as views
from adik.models import Category

# Simple Tags-простой пользовательский тег, который будет возвращать список категорий и #использоваться непосредственно в шаблоне. Согласно документации теги должны располагаться в #подкаталоге templatetags каталога приложения adik и являться пакетом, то есть, содержать файл #__init__.py. при этом обязательно перезагрузить сервер так как новый пакет

#Inclusion Tags-второй тип пользовательских тегов – включающий тег, позволяет дополнительно #формировать свой собственный шаблон на основе некоторых данных и возвращать фрагмент #HTML-страницы.

#  создаем экземпляр класса Library, через который происходит регистрация собственных шаблонных #  тегов: 
register = template.Library()

#@register.simple_tag(name='getcats')  # используется этот декоратор, доступный через переменную register чтобы связать функцию get_categories с тегом (превратить ее в в шаблоне в тег 
 #  -get_categories) 
#def get_categories():
    #return views.cats_db (cats_db список категорий)

#в функции show_categories() вместо коллекции cats_db будем читать данные из таблицы category и #передавать в шаблон list_categories.html: 
@register.inclusion_tag('adik/list_categories.html')
#Здесь в функции how_categories() происходит формирование и возврат словаря с необходимыми #данными для шаблона list_categories.html который создаем где все шаблоны приложения
#def show_categories():
    #cats = views.cats_db
    #return {"cats": cats} 

#в функции show_categories() вместо коллекции cats_db будем читать данные из таблицы category и #передавать в шаблон list_categories.html:       
def show_categories(cat_selected_id=0):
    cats = Category.objects.all()
    return {"cats": cats, "cat_selected": cat_selected_id}