import random
import time

from django.db import models


class Credentials(models.Model):
    user = models.CharField(max_length=20, null=False)
    password = models.CharField(max_length=50, null=False)
    domain = models.CharField(max_length=20, null=False)
    
    class Meta:
        unique_together = ('user', 'domain', )

class MountPoint(models.Model):
    # this is always like 'C' or 'D', right ?
    # as it seems it's about Windows systems ?
    # (I intentially use just 'C', not 'C:\' - as 
    # no any reason here for such redundancy)
    name = models.CharField(max_length=1)
    size = models.BigIntegerField()

class Workload(models.Model):
    ip = models.GenericIPAddressField(protocol='IPv4')
    credentials = models.ForeignKey(Credentials, 
                                    on_delete=models.SET_NULL, null=True)
    mount_list = models.ManyToManyField(MountPoint, blank=True)
    
class MigrationTarget(models.Model):
    CLOUD_TYPES = (
        ( 'aws', 'aws' ),
        ( 'azure', 'azure' ),
        ( 'vcloud', 'vcloude' ),
        ( 'vsphere', 'vsphere' )
    )
    cloud_type = models.CharField(max_length=10, choices=CLOUD_TYPES,
                                  null=False)
    credentials = models.ForeignKey(Credentials, 
                                    on_delete=models.SET_NULL, null=True)
    target = models.ForeignKey(Workload, on_delete=models.SET_NULL, null=True)
    
class Migration(models.Model):
    MIGRATION_STATES = (
        ( 'not_started', 'not_started' ),
        ( 'running', 'running' ),
        ( 'error', 'error' ),
        ( 'success', 'success' )
    )

    mount_list = models.ManyToManyField(MountPoint)
    state = models.CharField(max_length=10, choices=MIGRATION_STATES,
                             default='not_started')
    source = models.ForeignKey(Workload, 
                               on_delete=models.SET_NULL, null=True)
    target = models.ForeignKey(MigrationTarget, 
                               on_delete=models.SET_NULL, null=True)
    timer = models.FloatField(null=True)
    
    def run(self):
        # Make sure 'C' is selected
        mount_points = self.mount_list.all().values_list('name')
        mount_point_names = ' '.join(str(m) for m in mount_points)
        print(f'Mount point names: {mount_point_names}')
        if not 'c' in list(mount_point_names):
            self.state = 'error'
            self.timer = None
            print('No "C" mount point among selected')
            return
        self.state = 'running'
        self.target.target.mount_list.set(self.mount_list.all())
        
        print(f'target list: {self.target.target.mount_list}')
        
        random.seed()
        interval = random.randint(3,7)
        self.timer = time.time() + interval
        self.save()
        print('Migration started')

    def check_state(self):
        print('Check process')
        if self.timer and \
            time.time() > self.timer:
            self.state = 'success'
            self.timer = None
            
            self.save()
            print('Migration finished!')
