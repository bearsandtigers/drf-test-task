from app.models import ( Credentials, MountPoint, Workload, MigrationTarget,
                         Migration )
from app.serializers import ( CredentialsSerializer, MountPointSerializer,
                            WorkloadSerializer, MigrationTargetSerializer,
                            MigrationSerializer )

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework import ( status,
                           mixins,
                           generics )
from rest_framework import viewsets
  

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'credentials': reverse('credentials-list', request=request, format=format),
        'mountpoint': reverse('mountpoint-list', request=request, format=format),
        'workload': reverse('workload-list', request=request, format=format)
    })


class CredentialsViewSet(viewsets.ModelViewSet):
    queryset = Credentials.objects.all()
    serializer_class = CredentialsSerializer

class MountPointViewSet(viewsets.ModelViewSet):
    queryset = MountPoint.objects.all()
    serializer_class = MountPointSerializer

class WorkloadViewSet(viewsets.ModelViewSet):
    queryset = Workload.objects.all()
    serializer_class = WorkloadSerializer

class MigrationTargetViewSet(viewsets.ModelViewSet):
    queryset = MigrationTarget.objects.all()
    serializer_class = MigrationTargetSerializer

class MigrationViewSet(viewsets.ModelViewSet):
    queryset = Migration.objects.all()
    serializer_class = MigrationSerializer
    
    def state(self, request, *args, **kwargs):
        migration = self.get_object()
        migration.check_state()
        return Response(migration.state, status=status.HTTP_200_OK)
        
    def run(self, request, *args, **kwargs):
        migration = self.get_object()
        migration.run()
        return Response(migration.state, status=status.HTTP_200_OK)
