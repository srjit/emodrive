from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^home/', views.index, name='index'),
    url(r'^upload/$', views.upload_to_dropbox, name='upload_to_dropbox'),
    url(r'^analyze/(?P<path>.*)/$', views.get_image_analysis),
]
