#!/usr/bin/env python

from ansible.module_utils.basic import *
from ansible.module_utils.urls import fetch_url
from ansible.module_utils._text import to_text
from ansible.module_utils.six.moves.urllib.parse import urlencode

# from ansible.module_utils.six.moves.urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit
from ansible.module_utils.splunk_ta_aws import Splunk_TA_AWS, shared_arguments, as_bool
import json

class SplunkInputDescription(Splunk_TA_AWS):
    def __init__(self, module):
        super(SplunkInputDescription, self).__init__(module)
        self.base_endpoint = "{}/{}".format(self.module.params['url'], 'services/splunk_ta_aws_aws_description')
        self._default_apis = (
            'ec2_volumes/3600',
            'ec2_instances/3600',
            'ec2_reserved_instances/3600',
            'ebs_snapshots/3600',
            'classic_load_balancers/3600',
            'application_load_balancers/3600',
            'vpcs/3600',
            'vpc_network_acls/3600',
            'cloudfront_distributions/3600',
            'vpc_subnets/3600',
            'rds_instances/3600',
            'ec2_key_pairs/3600',
            'ec2_security_groups/3600',
            'ec2_images/3600',
            'ec2_addresses/3600',
            'lambda_functions/3600',
            's3_buckets/3600',
            'iam_users/3600'
        )

    def parse_response(self, response):
        return dict(
            name=response['name'],
            aws_iam_role=response['content'].get('aws_iam_role', ''),
            account=response['content']['account'],
            index=response['content']['index'],
            sourcetype=response['content']['sourcetype'],
            region=response['content']['regions'].split(','),
            apis=list(map(lambda x:x.strip(), response['content']['apis'].split(","))),
            disabled=as_bool(response['content']['disabled']),
        )

    def uri_data(self):
        return dict(
            output_mode='json',
            account=self.module.params['account'],
            aws_iam_role=self.module.params['aws_iam_role'], 
            index=self.module.params['index'], 
            sourcetype=self.module.params['sourcetype'], 
            regions=','.join(self.module.params['region']), # Do note the name difference here..regions(s)
            apis=','.join(self.module.params['apis']),
        )

    def run_module(self):
        if len(self.module.params['apis']) == 0:
            self.module.params['apis'] = self._default_apis

        super(SplunkInputDescription, self).run_module()

def main():
    argument_spec = shared_arguments()
    argument_spec.update(
        account=dict(required=True, type='str'),
        aws_iam_role=dict(required=False, type='str', default=''),
        index=dict(required=True, type='str'),
        region=dict(required=True, type='list'),
        apis=dict(required=False, type='list', default=[]),
        sourcetype=dict(required=False, type='str', default='aws:description'),
		state=dict(required=False, type='str', default='present', choises=['present', 'absent', 'disabled'])
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    desc = SplunkInputDescription(module)
    desc.run_module()

if __name__ == '__main__':
    main()