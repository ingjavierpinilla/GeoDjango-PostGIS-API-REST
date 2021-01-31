from django.urls import path
from .views import Upload_csv, RowListView

urlpatterns = [
    path('v1/datasets', Upload_csv.as_view()),
    path('v1/rows', RowListView.as_view()),
]
