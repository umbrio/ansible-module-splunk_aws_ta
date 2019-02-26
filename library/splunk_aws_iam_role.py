#!/usr/bin/env python

from ansible.module_utils.basic import *
from ansible.module_utils.urls import fetch_url
from ansible.module_utils._text import to_text
from ansible.module_utils.six.moves.urllib.parse import urlencode

# from ansible.module_utils.six.moves.urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit
from ansible.module_utils.splunk_ta_aws import Splunk_TA_AWS, shared_arguments
import json

class SplunkIAMRole(Splunk_TA_AWS):
	def __init__(self, module):
		super(SplunkIAMRole, self).__init__(module)
		self.base_endpoint = "{}/{}".format(self.module.params['url'], 'services/splunk_ta_aws/settings/splunk_ta_aws_iam_role')

	def data(self):
		return dict(
			output_mode='json',
			arn=self.module.params['arn'],
		)

	def get_all(self):
		for content in self.get_paginated(self.base_endpoint, headers=self.default_headers()):
			for a in content['entry']:
				yield { 
					'name': a['name'],
					'arn': a['content']['arn'],
				}

	def add(self):
		data = self.data()
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
		arn=dict(required=True, type='str'),
	)

	module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
	role = SplunkIAMRole(module)
	role.diff()

if __name__ == '__main__':
    main()