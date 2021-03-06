from django.urls import path
from .views import DatasetListCreate, RowListView, LogListView, LogList
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('v1/dataset', DatasetListCreate.as_view(), name = 'dataset-list-create'),
    path('v1/rows', RowListView.as_view(), name = 'row-list'),
    path('v1/logs', LogListView.as_view(), name = 'log-list'),
    path('logs', LogList, name = 'log-list-site'),
    path('token', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
