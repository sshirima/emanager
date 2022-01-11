
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.IncomeListView.as_view(), name='incomes'),
    path('search', csrf_exempt(views.incomes_search), name='expenses-search'),
    path('income/add', views.IncomeCreateView.as_view(), name='income-add'),
    path('income/<pk>/update', views.IncomeEditView.as_view(), name='income-edit'),
    path('income/<pk>/delete', views.IncomeDeleteView.as_view(), name='income-delete'),
]