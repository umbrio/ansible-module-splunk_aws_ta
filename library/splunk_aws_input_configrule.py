#!/usr/bin/env python

from ansible.module_utils.basic import *
from ansible.module_utils.urls import fetch_url
from ansible.module_utils._text import to_text
from ansible.module_utils.six.moves.urllib.parse import urlencode

# from ansible.module_utils.six.moves.urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit
from ansible.module_utils.splunk_ta_aws import Splunk_TA_AWS, shared_arguments, as_bool
import json

class SplunkInputConfigrule(Splunk_TA_AWS):
    def __init__(self, module):
        super(SplunkInputConfigrule, self).__init__(module)
        self.base_endpoint = "{}/{}" . format(self.module.params['url'], 'services/splunk_ta_aws_aws_config_rule')

    def data(self):
        return dict(
            output_mode='json',
            account=self.module.params['account'],
            aws_iam_role=self.module.params['aws_iam_role'], 
            polling_interval=self.module.params['polling_interval'], 
            index=self.module.params['index'], 
            sourcetype=self.module.params['sourcetype'], 
            region=json.dumps(self.module.params['region']),
            rule_names=json.dumps(self.module.params['rule_names']),
        )

    def get_all(self):
        # url = self.module.params['url']

        # url = "{}/{}" . format(url, 'services/splunk_ta_aws_aws_config_rule?output_mode=json')
        for content in self.get_paginated(self.base_endpoint, headers=self.default_headers()):
            for a in content['entry']:
                yield { 
                    'name': a['name'],
                    'aws_iam_role': a['content'].get('aws_iam_role', ''),
                    'polling_interval': a['content'].get('polling_interval', 300),
                    'account': a['content']['account'],
                    'index': a['content']['index'],
                    'sourcetype': a['content']['sourcetype'],
                    'region': json.loads(a['content']['region']),
                    'rule_names': json.loads(a['content']['rule_names']),
                    'disabled': as_bool(a['content']['disabled']),
                }


def main():
    argument_spec = shared_arguments()
    argument_spec.update(
        account=dict(required=True, type='str'),
        aws_iam_role=dict(required=False, type='str', default=''),
        index=dict(required=True, type='str'),
        polling_interval=dict(required=False, type='int', default=300),
        region=dict(required=True, type='list'),
        sourcetype=dict(required=False, type='str', default='aws:config:rule'),
        rule_names=dict(required=True, type='list'),
		state=dict(required=False, type='str', default='present', choises=['present', 'absent', 'disabled'])
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    rule = SplunkInputConfigrule(module)
    rule.diff()

if __name__ == '__main__':
    main()