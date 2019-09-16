#!/usr/bin/env python3
import requests as req
import time

def p(text: str):
    print(text)
    
base_url = 'http://127.0.0.1:8000/'
#headers = {'content-type': 'application/json'}

src_creds_payload = {
    "user": "src_user",
    "password": "123",
    "domain": "src-dom"
}

dst_creds_payload = {
    "user": "dst_user",
    "password": "321",
    "domain": "dst-dom"
}

p('\nCreate credentials for source and destination')
src_creds = req.post(base_url + 'credentials/', data = src_creds_payload).json()['id']
dst_creds = req.post(base_url + 'credentials/', data = dst_creds_payload).json()['id']
#p(f'{src_creds} {dst_creds}')

mp1_payload = {
    "name": "c",
    "size": 20100
}

mp2_payload = {
    "name": "d",
    "size": 101000
}

p('\nCreate mount points')
mp1 = req.post(base_url + 'mountpoint/', data = mp1_payload).json()['id']
mp2 = req.post(base_url + 'mountpoint/', data = mp2_payload).json()['id']


src_vm_payload = {
    "ip": "1.1.1.1",
    "credentials": src_creds,
    "mount_list": [ mp1, mp2]
}

dst_vm_payload = {
    "ip": "2.2.2.2",
    "credentials": dst_creds,
    "mount_list": []
}

p('\nCreate source and destination workloads')
src_vm = req.post(base_url + 'workload/', data = src_vm_payload).json()['id']
dst_vm = req.post(base_url + 'workload/', data = dst_vm_payload).json()['id']


target_payload = {
    "cloud_type": "azure",
    "credentials": dst_creds,
    "target": dst_vm
}

p('\nCreate migration target')
target = req.post(base_url + 'migrationtarget/', data = target_payload).json()['id']

# Change "mount_list" so it has no "c" ("mp1" variable) in order to fail test
migration_payload = {
    "mount_list": [mp1],
    "target": target,
    "source": src_vm
}

p('\nCreate migration')
migration = req.post(base_url + 'migration/', data = migration_payload).json()['id']


p('\nStart migration')
state = req.post(base_url + f'migration/{migration}/run').json()


p('\nCheck migration status')

status = 'running'
while state == 'running':
    print(state)
    time.sleep(1)
    state = req.get(base_url + f'migration/{migration}/state').json()
print(state)
if state == 'success':
    print(f'Mount points have been copied\nfrom:\n{req.get(base_url + "workload/" + str(src_vm)).json()}\n'
          f'to\n{req.get(base_url + "workload/" + str(dst_vm)).json()}')


# Clear up
p('\nClear all things')
p(req.delete(base_url + f'migration/{migration}'))

p(req.delete(base_url + f'migrationtarget/{target}'))

p(req.delete(base_url + f'workload/{src_vm}'))
p(req.delete(base_url + f'workload/{dst_vm}'))

p(req.delete(base_url + f'mountpoint/{mp1}'))
p(req.delete(base_url + f'mountpoint/{mp2}'))

p(req.delete(base_url + f'credentials/{src_creds}'))
p(req.delete(base_url + f'credentials/{dst_creds}'))
