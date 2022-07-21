from django.contrib import admin
from django.urls import path, include

from django_db_logger.views import __gen_500_errors

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__gen_500/', __gen_500_errors),
    path('', include('django_db_logger.urls'))
]

handler404 = 'django_db_logger.views.error_404_view'