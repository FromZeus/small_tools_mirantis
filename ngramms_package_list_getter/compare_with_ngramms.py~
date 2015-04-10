import require_utils
import json

req = open("filtered_requirements", 'r')
u_req = open("filtered_requirements_ubuntu", 'r')

u_req_d = dict()
req_d = dict()
res_comp = dict()

for i in u_req:
	u_req_d.setdefault(i.rstrip(), "")

for i in req:
	res_comp.setdefault(i.rstrip(), require_utils.Require.correlate(u_req_d, i))

with open("comp-list.json", 'w') as comp_list:
	json.dump(res_comp, comp_list, indent=4, sort_keys=True, separators=(',', ':'))