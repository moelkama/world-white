from .views import TaskListCreateAPIView, TaskRetrieveUpdateDestroyAPIView
from .views import MatchListCreateAPIView
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
    path('match/', MatchListCreateAPIView.as_view(), name='match-list-create'),
    path('data/', login.data, name='data'),
    path('token/', login.token, name='session'),
    path('update_profile/', login.update_profile, name='update_profile'),
    path('update_username/', login.update_username, name='update_username'),
    path('already_logged/', login.already_logged, name='already_logged'),
    path('registeruser/', views.SignUp, name='registerUser'),
    path('loginuser/', views.SignIn, name='loginUser'),
    path('leaderboard/', login.leadrboard, name='leaderboard'),
    path('history/', login.get_match_history, name='get_match_history'),
]