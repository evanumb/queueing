from django.contrib import admin
from django.urls import path, include
from queue_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
    path('take-ticket/', views.take_ticket, name='take_ticket'),
    path('my-ticket/', views.my_ticket, name='my_ticket'),
    path('status/', views.status_view, name='status'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/call-next/', views.call_next, name='call_next'),
    path('admin/mark-served/<int:ticket_id>/', views.mark_served, name='mark_served'),
    path('admin/skip/<int:ticket_id>/', views.skip_ticket, name='skip_ticket'),
    path('admin/reset-today/', views.reset_today, name='reset_today'),
]
