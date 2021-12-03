from napalm import get_network_driver
import json

driver = get_network_driver('ios')
optional_args = {'secret': 'cisco'}
ios = driver('10.1.1.1', 'admin', 'admin', optional_args=optional_args)
ios.open()
output = ios.ping('10.1.1.1')


dump = json.dumps(output, indent=4)
print(dump)

# f = open('arp.txt', 'w')
# f.write(dump)
ios.close()