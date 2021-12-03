from napalm import get_network_driver
import json

driver = get_network_driver('ios')
optional_args = {'secret': 'cisco'}
ios = driver('10.1.1.10', 'u1', 'cisco', optional_args=optional_args)
ios.open()
ios.load_replace_candidate(filename='r10-config.txt')
diff = ios.compare_config()
print(diff)
if len(diff):
    print('applying changes')
    ios.commit_config()
else:
    print('no change')
    ios.discard_config()

ios.close()