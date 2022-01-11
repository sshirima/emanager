
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('expenses', views.ExpenseListView.as_view(), name='expenses'),
    path('expenses/search', csrf_exempt(views.expenses_search), name='expenses-search'),
    path('expense/add', views.ExpenseCreateView.as_view(), name='expense-add'),
    path('expense/<pk>/update', views.ExpenseEditView.as_view(), name='expense-edit'),
    path('expense/<pk>/delete', views.ExpenseDeleteView.as_view(), name='expense-delete'),
    path('expense-category-summary', views.expense_category_summary, name='expense-category-summary'),
    path('expense-stats', views.expense_stats, name='expense-stats'),
]