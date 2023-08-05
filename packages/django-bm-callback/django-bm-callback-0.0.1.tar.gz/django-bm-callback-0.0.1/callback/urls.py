from django.urls import path

from apps.callback import views


app_name = 'callback'


urlpatterns = [

    path('add/', views.add_callback, name='add'),

    path('list/', views.CallbackListView.as_view(), name='list')

]