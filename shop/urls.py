from django.conf.urls import url
from django.urls import path
from .views import *

app_name = 'shop'
urlpatterns = [
    # /
    # /반찬/
    # /2/고추장-소스-진미채
    path('', product_list, name='product_list'),
    path('<category_slug>/', product_list, name='product_list_by_category'),
    path('<id>/<slug>/', product_detail, name='product_detail'),
]
