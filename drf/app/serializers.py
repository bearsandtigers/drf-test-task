from rest_framework import serializers
from django.core.validators import validate_ipv4_address

from app.models import Workload, Credentials, MountPoint, MigrationTarget, \
                       Migration

class WorkloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workload
        fields = ['id', 'ip', 'credentials', 'mount_list']
        ip = serializers.CharField(validators=[validate_ipv4_address])
    def update(self, instance, validated_data):
        if 'ip' in validated_data and \
           validated_data['ip'] != instance.ip:
            raise serializers.ValidationError({
                'ip': 'You may not change this field.',
            })
        return super().update(instance, validated_data)
        
class CredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credentials
        #id = serializers.ReadOnlyField()
        fields = ['id', 'user', 'password', 'domain']
        write_only_fields = ['password',]
        
class MountPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = MountPoint
        fields = ['id', 'name', 'size']

class MigrationTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MigrationTarget
        fields = ['id', 'cloud_type', 'credentials', 'target']

class MigrationSerializer(serializers.ModelSerializer):
    
    #mount_list = serializers.MultipleChoiceField(choices='source.mount_list.all()')
    class Meta:
        model = Migration
        fields = ['id', 'mount_list', 'state', 'target', 'source']
        read_only_fields = ['state',]
        #print('CHECK:', data)
    def __init__(self, *args, **kwargs):
        super(MigrationSerializer, self).__init__(*args, **kwargs)
        print('S:', self)
        print('ARGS: ', *args)
        #self.BaselineDefault = BaselineModel.objects.get(pk=<your pk>)
        
    #state = serializers.SerializerMethodField()
    #def get_state(self, obj):
    #   return obj.state
        
    def create(self, validated_data):
        selected_mount_list = validated_data['mount_list']
        
        source_mount_list = validated_data['source'].mount_list.all()
        print('Selected:', repr(selected_mount_list))
        print('Source:', repr(source_mount_list))
        for m in selected_mount_list:
            if m not in source_mount_list:
                raise serializers.ValidationError({
                    'mount_list': 'Mount point doesn\'t belong to source VM',
                })
        return super().create(validated_data)
        
    #mount_list = serializers.PrimaryKeyRelatedField(
    #    many=True, queryset=source.objects.all())
    
