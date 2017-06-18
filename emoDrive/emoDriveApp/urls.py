from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^home/', views.index, name='index'),
    url(r'^upload/$', views.data_input, name='data_input'),
    url(r'^analyze/(?P<path>.*)/$', views.get_image_analysis),
]
