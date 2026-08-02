from django.urls import path # функцию path, которая и связывает URL c функциями представления
from adik import views


#urlpatterns = [
    #path('', views.index), # функция index будет соответствовать адресу:
      #  http://домен/

    #path('cats/', views.categories),  #  http://домен/cats/
    #path('cats/<int:cat_id>/', views.categories),  #  http://домен/cats/1...5....
    # маршрут для доступа к категориям через слаг (slug):
    #path('cats/<slug:cat_slug>/', views.categories_by_slug), #  цифры один из видов слагов
    
#]

#urlpatterns = [ # добавляем имена каждому шаблону пути
    #path('', views.index, name='home'),
    #path('cats/<slug:cat_slug>/', views.categories_by_slug, name='cats'),
    #path('cats/<int:cat_id>/', views.categories, name='cats_id'),
    #path('about/', views.about, name='about'),
    
#]


urlpatterns = [
    #path('', views.index, name='home'),
    path('', views.AdikHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    #path('addpage/', views.addpage, name='add_page'), #заменили функцию на класс представления
    #path('addpage/', views.AddPage.as_view(), name='add_page'), # ЗАМЕНИЛИ НА НИЖНЕЕ
    #path('addpage/', views.AddPage2.as_view(), name='add_page'),
    path('addpage/', views.AddPage3.as_view(), name='add_page'), 
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    #path('post/<int:post_id>/', views.show_post, name='post'), -поменяли на слаги
    #path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('category/<slug:cat_slug>/', views.AdikCategory.as_view(), name='category'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    #path('category/<slug:cat_slug>/', views.show_category, name='category'),
    #path('category/<int:cat_id>/', views.show_category, name='category'), #поменяли на #slug:cat_slug
    
    
]