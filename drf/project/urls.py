from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from app import views
#from rest_framework_swagger.views import get_swagger_view
from django.views.generic import TemplateView

#schema_view = get_swagger_view(title='API')

router = routers.DefaultRouter()
'''
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
'''

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += [
    path('', include('app.urls')),
]

#urlpatterns += [
#    path(r'swagger/', schema_view),
#]

urlpatterns += [
    path('swagger/', TemplateView.as_view(
        template_name='swagger.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger'),
]
