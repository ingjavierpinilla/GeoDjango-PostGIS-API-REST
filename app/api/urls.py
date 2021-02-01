from django.urls import path
from .views import Upload_csv, RowListView, LoggListView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('v1/datasets', Upload_csv.as_view()),
    path('v1/rows', RowListView.as_view()),
    path('v1/loggs', LoggListView.as_view()),
    path('token', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
