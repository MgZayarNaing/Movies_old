from django.urls import path
from .views.category_views import category_list, category_create, category_detail, category_update, category_delete

urlpatterns = [

    path('categories/', category_list, name='category-list'),
    path('categories/create/', category_create, name='category-create'),
    path('categories/<int:pk>/', category_detail, name='category-detail'),
    path('categories/<int:pk>/update/', category_update, name='category-update'),
    path('categories/<int:pk>/delete/', category_delete, name='category-delete'),

    
]
