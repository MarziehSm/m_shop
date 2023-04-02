from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.order_create_view, name='order_create'),
    path('get_all_data/', views.GetAllData.as_view()),
    path('all_data/', views.all_data),
    path('get_ispaid_data/', views.GetIsPaidData.as_view()),
    path('update_data/<int:pk>/', views.UpdateData.as_view()),
    path('post_model/', views.PostModelData.as_view()),
    path('set_data/', views.set_data),
    path('search/', views.SearchData.as_view()),
    path('delete/<int:pk>/', views.DeleteData.as_view()),
]
