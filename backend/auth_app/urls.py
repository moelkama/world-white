from .views import TaskListCreateAPIView, TaskRetrieveUpdateDestroyAPIView
from django.urls import path
from django.urls import path
from . import views 
from . import login


urlpatterns = [
    path('csrf-token/', login.csrf_token),
    path('redirect/', views.redirect_to_42, name='redirect_to_42'),
    path('auth/callback/', views.callback, name='callback'),
    path('logout/',login.logout,name='logout'),
    path('exit/',login.exit,name='exit'),
    path('tasks/', TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-retrieve-update-destroy'),
    path('get_session/', login.get_session, name='get_session'),
]