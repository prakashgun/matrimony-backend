from django.urls import path

from .views import UserList, UserDetail, GroupList

app_name = 'user_management'

urlpatterns = [
    path('users/', UserList.as_view(), name='users'),
    path('users/<pk>/', UserDetail.as_view(), name='user_detail'),
    path('groups/', GroupList.as_view(), name='groups'),
]
