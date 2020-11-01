from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('csv-upload',views.csv_upload,name='csv-upload'),
    path('select-class/',views.select_class,name='select-class_'),
    path('calculate',views.calculator,name='calculator'),
]