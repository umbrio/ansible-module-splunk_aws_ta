#!/usr/bin/env python

from ansible.module_utils.basic import *
from ansible.module_utils.urls import fetch_url
from ansible.module_utils._text import to_text
from ansible.module_utils.six.moves.urllib.parse import urlencode

# from ansible.module_utils.six.moves.urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit
from ansible.module_utils.splunk_ta_aws import Splunk_TA_AWS, shared_arguments, as_bool
import json

class SplunkInputCloudwatch(Splunk_TA_AWS):
    def __init__(self, module):
        super(SplunkInputCloudwatch, self).__init__(module)
        self.base_endpoint = "{}/{}".format(self.module.params['url'], 'services/splunk_ta_aws_aws_cloudwatch')
    
    def data(self):
        return dict(
            output_mode='json',
            aws_account=self.module.params['account'], # Do note the name difference here.
            aws_iam_role=self.module.params['aws_iam_role'], 
            index=self.module.params['index'], 
            sourcetype=self.module.params['sourcetype'], 
            aws_region=','.join(self.module.params['region']), # Do note the name difference here.
            polling_interval=self.module.params['polling_interval'],
            period=self.module.params['period'],
            metric_namespace=json.dumps(self.module.params['metric_namespace']),
            metric_names=self.encode_nested_json(self.module.params['metric_names']),
            metric_dimensions=self.encode_nested_json(self.module.params['metric_dimensions']),
            statistics=self.encode_nested_json(self.module.params['statistics']),
        )

    def get_all(self):
        for content in self.get_paginated(self.base_endpoint, headers=self.default_headers()):
            for c in content['entry']:
                yield {
                    'name': c['name'],
                    'aws_iam_role': c['content'].get('aws_iam_role', ''),
                    'account': c['content']['aws_account'], # Do note the name difference here.
                    'index': c['content']['index'],
                    'sourcetype': c['content']['sourcetype'],
                    'region': c['content']['aws_region'].split(','), # Do note the name difference here.
                    'polling_interval': c['content']['polling_interval'],
                    'period': c['content']['period'],
                    'metric_namespace': json.loads(c['content']['metric_namespace']),
                    'metric_names': self.decode_nested_json(c['content']['metric_names']),
                    'metric_dimensions': self.decode_nested_json(c['content']['metric_dimensions']),
                    'statistics': self.decode_nested_json(c['content']['statistics']),
                    'disabled': as_bool(c['content']['disabled']),
                }

    def diff(self):
        default_metrics = self.default_metrics()

        if len(self.module.params['metric_namespace']) == 0:
            self.module.params['metric_namespace'] = default_metrics['metric_namespace']
        if len(self.module.params['metric_names']) == 0:
            self.module.params['metric_names'] = default_metrics['metric_names']
        if len(self.module.params['metric_dimensions']) == 0:  
            self.module.params['metric_dimensions'] = default_metrics['metric_dimensions']
        if len(self.module.params['statistics']) == 0:  
            self.module.params['statistics'] = default_metrics['statistics']

        super(SplunkInputCloudwatch, self).diff()

    def add(self):
        data = self.data()
        data.update(
            name=self.module.params['name'],
        )

        resp, info = fetch_url(self.module, self.base_endpoint, data=urlencode(data), headers=self.default_headers(), method='POST', timeout=300)

        if info['status'] == 201:
            # Adding an already disabled input cannot be done by setting the disabled key in the data above. 
            # If the disabled key is present everything else is ignored (and not added).
            # So we have to do this in two steps.
            if self.should_disable():
                self.disable(True)

            self.module.exit_json(changed=True)

        self.parseErrorResponse(info)

    # Return a json encoded string where all the individual items of the original list
    # are also json encoded before the final list is encoded.
    # Essentially the items in the list end up being double encoded. 
    def encode_nested_json(self, data):
        return json.dumps(list(map(lambda x: json.dumps(x), data)))

    def decode_nested_json(self, data):
        outer = json.loads(data)
        try:
            return list(map(lambda x: json.loads(x), outer))
        except ValueError:
            return outer

    # Get the lists of default metrics (these are also used in the GUI)
    def default_metrics(self):
        default_metric_namespace = []
        default_metric_names = []
        default_metric_dimensions = []
        default_statistics = []

        url = "{}/{}".format(self.module.params['url'], 'services/splunk_ta_aws/splunk_ta_aws_cloudwatch_default_settings?output_mode=json')
        resp, info = fetch_url(self.module, url, headers=self.default_headers(), method='GET', timeout=120)

        if info['status'] != 200:
            self.module.fail_json(msg="Could not get default metrics from API")

        defaults = json.loads(resp.read())['entry'][0]['content']

        namespaces = json.loads(defaults['namespaces'])
        metrics = json.loads(defaults['metrics'])
        dimensions = json.loads(defaults['dimensions'])
        statistics = json.loads(defaults['statistics'])

        for namespace in namespaces:
            for dimension in dimensions[namespace]:
                default_metric_namespace.append(namespace)
                default_metric_dimensions.append([dimension])
                default_metric_names.append('.*')
                default_statistics.append(statistics)

        return dict(
            metric_namespace=default_metric_namespace,
            metric_names=default_metric_names,
            metric_dimensions=default_metric_dimensions,
            statistics=default_statistics,
        )

def main():
    argument_spec = shared_arguments()
    argument_spec.update(
        account=dict(required=True, type='str'),
        aws_iam_role=dict(required=False, type='str', default=''),
        index=dict(required=True, type='str'),
        region=dict(required=True, type='list'),
        sourcetype=dict(required=False, type='str', default='aws:cloudwatch'),
        polling_interval=dict(required=False, type='int', default=3600),
        period=dict(required=False, type='int', default=300),
        metric_namespace=dict(required=False, type='list', default=[]),
        metric_names=dict(required=False, type='list', default=[]),
        metric_dimensions=dict(required=False, type='list', default=[]),
        statistics=dict(required=False, type='list', default=[]),
		state=dict(required=False, type='str', default='present', choises=['present', 'absent', 'disabled'])
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    desc = SplunkInputCloudwatch(module)
    desc.diff()

if __name__ == '__main__':
    main()