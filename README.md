## Splunk TA AWS ansible module ##

This collection of ansible modules can be used to manage various settings and inputs of the [splunk AWS TA](https://splunkbase.splunk.com/app/1876/)
These modules use the splunk API for this TA to manage the settings and inputs.

### How to use ###

Copy the library and module_utils directories in the root of your playbook (or role) to use them.
See [this](https://docs.ansible.com/ansible/latest/dev_guide/developing_locally.html) page for more information.

An example playbook ca be found at the end of this document.

# Modules #

### splunk_aws_account ###

Manage aws accounts in the Splunk AWS TA

|parameter |choises |default|comment   |
|---       |---     |---    |---       |
|name      |        |       |The name of the account (mandatory) |
|secret_key|        |       |mandatory |
|key_id    |        |       |mandatory |
|category  |choises:<br>* 1<br>* 2<br>* 3|1      |          |
|state     |choises:<br>* present<br>* absent|present||

### splunk_aws_iam_role ###

Manage iam roles in the Splunk AWS TA

|parameter |choises |default|comment   |
|---       |---     |---    |---       |
|name      |        |       |The name of the role (mandatory) |
|arn       |        |       |The arn of the role (mandatory) |
|state     |choises:<br>* present<br>* absent|present||

### splunk_aws_input_cloudwatch ###

Manage cloudwatch inputs in the Splunk AWS TA

|parameter|choises|default|comment|
|---|---|---|---|
|name|||The name of the input (mandatory)|
|account|||AWS account (mandatory)|
|aws_iam_role|||Assume role|
|region|||A list of AWS regions|
|index|||The index to use (mandatory)|
|sourcetype||aws:cloudwatch|The sourcetype to use|
|polling_interval||3600|The polling interval to use|
|period||300|The period to use|
|metric_namespace||||
|metric_names||||
|metric_dimensions||||
|statistics||||
|state|choises:<br>* present<br>* absent<br>* disabled|present||

if you leave the metric_name, metric_namespaces, metric_dimensions and statistics parameters emtpy the input will be created with the following default set of metrics:

```yaml
  metric_dimensions:
  - - ApiName:
      - .*
  - - ApiName:
      - .*
      Stage:
      - .*
  - - ApiName:
      - .*
      Method:
      - .*
      Resource:
      - .*
      Stage:
      - .*
  - - LoadBalancer:
      - .*
  - - AvailabilityZone:
      - .*
      LoadBalancer:
      - .*
  - - AvailabilityZone:
      - .*
      LoadBalancer:
      - .*
      TargetGroup:
      - .*
  - - Currency:
      - .*
  - - Currency:
      - .*
      ServiceName:
      - .*
  - - Currency:
      - .*
      LinkedAccount:
      - .*
      ServiceName:
      - .*
  - - VolumeId:
      - .*
  - - AutoScalingGroupName:
      - .*
  - - ImageId:
      - .*
  - - InstanceId:
      - .*
  - - InstanceType:
      - .*
  - - AvailabilityZone:
      - .*
      LoadBalancerName:
      - .*
  - - AvailabilityZone:
      - .*
  - - LoadBalancerName:
      - .*
  - - FunctionName:
      - .*
      Resource:
      - .*
  - - FunctionName:
      - .*
  - - DBClusterIdentifier:
      - .*
  - - DBInstanceIdentifier:
      - .*
  - - DatabaseClass:
      - .*
  - - EngineName:
      - .*
  - - BucketName:
      - .*
      StorageType:
      - .*
  - - BucketName:
      - .*
      FilterId:
      - .*
  metric_names:
  - .*
  - .*
  - .*
  - .*
  - .*
  - .*
  - .*
  - .*
  - .*
  - .*
  - .*
  - .*
  - .*
  - .*
  - .*
  - .*
  - .*
  - .*
  - .*
  - .*
  - .*
  - .*
  - .*
  - .*
  - .*
  metric_namespace:
  - AWS/ApiGateway
  - AWS/ApiGateway
  - AWS/ApiGateway
  - AWS/ApplicationELB
  - AWS/ApplicationELB
  - AWS/ApplicationELB
  - AWS/Billing
  - AWS/Billing
  - AWS/Billing
  - AWS/EBS
  - AWS/EC2
  - AWS/EC2
  - AWS/EC2
  - AWS/EC2
  - AWS/ELB
  - AWS/ELB
  - AWS/ELB
  - AWS/Lambda
  - AWS/Lambda
  - AWS/RDS
  - AWS/RDS
  - AWS/RDS
  - AWS/RDS
  - AWS/S3
  - AWS/S3
  statistics:
  - - Average
    - Sum
    - SampleCount
    - Maximum
    - Minimum
  - - Average
    - Sum
    - SampleCount
    - Maximum
    - Minimum
  - - Average
    - Sum
    - SampleCount
    - Maximum
    - Minimum
  - - Average
    - Sum
    - SampleCount
    - Maximum
    - Minimum
  - - Average
    - Sum
    - SampleCount
    - Maximum
    - Minimum
  - - Average
    - Sum
    - SampleCount
    - Maximum
    - Minimum
  - - Average
    - Sum
    - SampleCount
    - Maximum
    - Minimum
  - - Average
    - Sum
    - SampleCount
    - Maximum
    - Minimum
  - - Average
    - Sum
    - SampleCount
    - Maximum
    - Minimum
  - - Average
    - Sum
    - SampleCount
    - Maximum
    - Minimum
  - - Average
    - Sum
    - SampleCount
    - Maximum
    - Minimum
  - - Average
    - Sum
    - SampleCount
    - Maximum
    - Minimum
  - - Average
    - Sum
    - SampleCount
    - Maximum
    - Minimum
  - - Average
    - Sum
    - SampleCount
    - Maximum
    - Minimum
  - - Average
    - Sum
    - SampleCount
    - Maximum
    - Minimum
  - - Average
    - Sum
    - SampleCount
    - Maximum
    - Minimum
  - - Average
    - Sum
    - SampleCount
    - Maximum
    - Minimum
  - - Average
    - Sum
    - SampleCount
    - Maximum
    - Minimum
  - - Average
    - Sum
    - SampleCount
    - Maximum
    - Minimum
  - - Average
    - Sum
    - SampleCount
    - Maximum
    - Minimum
  - - Average
    - Sum
    - SampleCount
    - Maximum
    - Minimum
  - - Average
    - Sum
    - SampleCount
    - Maximum
    - Minimum
  - - Average
    - Sum
    - SampleCount
    - Maximum
    - Minimum
  - - Average
    - Sum
    - SampleCount
    - Maximum
    - Minimum
  - - Average
    - Sum
    - SampleCount
    - Maximum
    - Minimum
  ```

### splunk_aws_input_configrule ###

Manage configrule inputs in the Splunk AWS TA

|parameter|choises|default|comment|
|---|---|---|---|
|name|||The name of the input (mandatory)|
|account|||AWS account (mandatory)|
|aws_iam_role|||Assume role|
|index|||The index to use (mandatory)|
|sourcetype||aws:config:rule|The sourcetype to use|
|polling_interval||3600|The polling interval to use|
|region|||A list of AWS regions|
|rule_names|||The config rules per region<br>The number of rules specified here should match the number of regions|
|state|choises:<br>* present<br>* absent<br>* disabled|present||

### splunk_aws_input_description ###

Manage description inputs in the Splunk AWS TA

|parameter|choises|default|comment|
|---|---|---|---|
|name|||The name of the input (mandatory)|
|account|||AWS account (mandatory)|
|aws_iam_role|||Assume role|
|index|||The index to use (mandatory)|
|sourcetype||aws:description|The sourcetype to use|
|region|||A list of AWS regions|
|apis|||A list of apis to use<br>Should be in the form apiname/interval|
|state|choises:<br>* present<br>* absent<br>* disabled|present||

If apis is left empty the following default apis will be used:
```yaml
apis:
- ec2_volumes/3600
- ec2_instances/3600
- ec2_reserved_instances/3600
- ebs_snapshots/3600
- classic_load_balancers/3600
- application_load_balancers/3600
- vpcs/3600
- vpc_network_acls/3600
- cloudfront_distributions/3600
- vpc_subnets/3600
- rds_instances/3600
- ec2_key_pairs/3600
- ec2_security_groups/3600
- ec2_images/3600
- ec2_addresses/3600
- lambda_functions/3600
- s3_buckets/3600
- iam_users/360
```

### Shared parameters ###

All modules accept the following parameters.

|parameter |choises |default|comment   |
|---       |---     |---    |---       |
|url|||The url of the API endpoint to use (mandatory)|
|token|||The authentication token to usewith the api (mandatory)|
|validate_certs|choises:<br>* True<br>* False|True|Validate the SSL certificate of the endpoint|

An example on how you can get the token:

```yaml
- name: log in
  uri:
    url: https://<url>/services/auth/login?output_mode=json
    validate_certs: no
    method: POST
    body:
      username: admin
      password: adminpass
    status_code: 200
    body_format: form-urlencoded
    return_content: yes
  no_log: true
  register: login_result
```
You can then pass "{{ login_result.json.sessionKey }}" to the token parameter.

### Example playbook ###

```yaml
- hosts: localhost
  gather_facts: no
  vars:
  - url: https://127.0.0.1:8089
  tasks:
  - name: log in
    uri:
      url: "{{ url }}/services/auth/login?output_mode=json"
      validate_certs: no
      method: POST
      body:
        username: admin
        password: adminpassword
      status_code: 200
      body_format: form-urlencoded
      return_content: yes
    no_log: true
    register: login_result
  - name: my_aws_account
    splunk_aws_account:
      name: my_aws_account
      key_id: XYZXUZYQWEDWQEFW
      secret_key: QWCQWRCWQRVQERVQER
      url: "{{ url }}"
      token: "{{ login_result.json.sessionKey }}"
      validate_certs: no
  - name: my_iam_role
    splunk_aws_iam_role:
      name: my_iam_role
      arn: "arn:copied:from:aws"
      url: "{{ url }}"
      token: "{{ login_result.json.sessionKey }}"
      validate_certs: no
  - name: input configrule
    splunk_aws_input_configrule:
      name: my_inpu_configrule
      account: my_aws_account
      index: main
      polling_interval: 600
      region:
      - eu-west-1
      rule_names:
      - ""
      url: "{{ url }}"
      token: "{{ login_result.json.sessionKey }}"
      validate_certs: no
  - name: input description cli_added
    splunk_aws_input_description:
      name: my_description_input
      account: my_aws_account
      index: docker
      region:
      - eu-west-1
      apis:
      - lambda_functions/3600
      - ec2_volumes/3600
      url: "{{ url }}"
      token: "{{ login_result.json.sessionKey }}"
      validate_certs: no
  - name: input description ansible_description
    splunk_aws_input_description:
      name: input_description_wdefaults
      account: my_aws_account
      index: docker
      region:
      - eu-west-1
      url: "{{ url }}"
      token: "{{ login_result.json.sessionKey }}"
      validate_certs: no
  - name: input cloudwatch with defaults
    splunk_aws_input_cloudwatch:
      name: CloudwatchDefaults
      account: my_aws_account
      index: splunklogger
      region:
      - eu-west-1
      url: "{{ url }}"
      token: "{{ login_result.json.sessionKey }}"
      validate_certs: no
```