from napalm import get_network_driver
import json

driver = get_network_driver('ios')
optional_args = {'secret': 'cisco'}
ios = driver('10.1.1.10', 'admin', 'admin', optional_args=optional_args)
ios.open()
ios.load_replace_candidate(filename='r10-config.txt')
diff = ios.compare_config()
print(diff)

ios.close()