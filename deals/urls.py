
from django.urls import path
from . import views

app_name = 'deals'

urlpatterns = [
    path('last-deals/', views.last_deals, name='last_deals'),
    path('add-deal/', views.add_deal, name='add_deal'),
]
