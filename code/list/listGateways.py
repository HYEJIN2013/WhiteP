##################################################################################
# List gateways
# ©Copyright IBM Corporation 2014.
# LICENSE: MIT (http://opensource.org/licenses/MIT)    
# libraries used:
#        SoftLayer,pprint
##################################################################################

import SoftLayer.API
from pprint import pprint as pp
 
api_username = 'xxxx'
api_key = 'xxxx'
 
client = SoftLayer.Client(
    username=api_username,
    api_key=api_key,
)

gateways = client['Account'].getNetworkGateways()
 
pp (gateways)
