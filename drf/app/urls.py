from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from app import views

from app.views import ( api_root, CredentialsViewSet, MountPointViewSet,
                      WorkloadViewSet, MigrationTargetViewSet, 
                      MigrationViewSet )
from rest_framework import renderers

credentials_list = CredentialsViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
credentials_detail = CredentialsViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

mountpoint_list = MountPointViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
mountpoint_detail = MountPointViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})

workload_list = WorkloadViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
workload_detail = WorkloadViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

migrationtarget_list = MigrationTargetViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
migrationtarget_detail = MigrationTargetViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})

migration_list = MigrationViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
migration_detail = MigrationViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})


urlpatterns = [
    path('', api_root),
    path('credentials/', credentials_list, name='credentials-list'),
    path('credentials/<int:pk>/', credentials_detail, name='credentials-detail'),
    path('mountpoint/', mountpoint_list, name='mountpoint-list'),
    path('mountpoint/<int:pk>/', mountpoint_detail, name='mountpoint-detail'),
    path('workload/', workload_list, name='workload-list'),
    path('workload/<int:pk>/', workload_detail, name='workload-detail'),
    path('migrationtarget/', migrationtarget_list, name='migrationtarget-list'),
    path('migrationtarget/<int:pk>/', migrationtarget_detail,
         name='migrationtarget-detail'),
    path('migration/', migration_list, name='migration-list'),
    path('migration/<int:pk>/', migration_detail, name='migration-detail'),
    path('migration/<int:pk>/state',
         views.MigrationViewSet.as_view({'get': 'state'}),
         name='migration-state'),
    path('migration/<int:pk>/run',
         views.MigrationViewSet.as_view({'post': 'run'}),
         name='migration-run'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
