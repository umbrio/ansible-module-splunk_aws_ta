#!/usr/bin/env python

from ansible.module_utils.basic import *
from ansible.module_utils.urls import fetch_url
from ansible.module_utils._text import to_text
from ansible.module_utils.six.moves.urllib.parse import urlencode

# from ansible.module_utils.six.moves.urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit
from ansible.module_utils.splunk_ta_aws import Splunk_TA_AWS, shared_arguments
import json

class SplunkAWSAccount(Splunk_TA_AWS):
	def __init__(self, module):
		super(SplunkAWSAccount, self).__init__(module)
		self.base_endpoint = "{}/{}".format(self.module.params['url'], 'services/splunk_ta_aws/settings/account')

	def uri_data(self):
		return dict(
			output_mode='json',
			key_id=self.module.params['key_id'],
			secret_key=self.module.params['secret_key'],
			category=self.module.params.get('category', 1),
		)

	def parse_response(self, response):
		return dict( 
			name=response['name'],
			secret_key=response['content']['secret_key'],
			key_id=response['content']['key_id'],
			category=response['content']['category'],
		)

	def get_single(self):
		url = "{}/{}?output_mode=json".format(self.base_endpoint, self.module.params['name'])
		resp, info = fetch_url(self.module, url, headers=self.default_headers(), method='GET', timeout=120)
		if info['status'] == 200:
			content = json.loads(resp.read())
			return self.parse_response(content['entry'][0])		
		else:
			return None

	def add(self):
		data = self.uri_data()
		data.update(
			name=self.module.params['name'],
		)
		resp, info = fetch_url(self.module, self.base_endpoint, data=urlencode(data), headers=self.default_headers(), method='POST', timeout=120)

		if info['status'] == 201:
			self.module.exit_json(changed=True)

		self.parseErrorResponse(info)

def main():
	argument_spec = shared_arguments()
	argument_spec.update(
		secret_key=dict(required=True, type='str'),
		key_id=dict(required=True, type='str'),
		category=dict(required=False, type='int', default=1, choises=[1,2,3]),
	)

	module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
	account = SplunkAWSAccount(module)
	account.run_module()

if __name__ == '__main__':
    main()