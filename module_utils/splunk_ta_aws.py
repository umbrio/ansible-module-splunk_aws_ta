#!/usr/bin/env python
from ansible.module_utils.urls import fetch_url
from ansible.module_utils.six.moves.urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit

import json

def shared_arguments():
	return dict(
		name=dict(required=True, type='str'),
		url=dict(required=True, type='str'),
		token=dict(required=True, type='str'),
		validate_certs=dict(required=False, type='bool'),
		state=dict(required=False, type="str", default='present', choises=['present', 'absent'])
	)

def as_bool(v):
	if type(v) == bool:
		return v
	if type(v) == int:
		return v > 0

	return v.lower() in ("yes", "y", "true", "t", "1")

class Splunk_TA_AWS(object):
	def __init__(self, module):
		self.module = module	

	def default_headers(self):
		token = self.module.params['token']
		headers = {
			"Authorization": "Splunk {}" . format(token),
		}
		return headers

	def get_paginated(self, url, headers=None):
		self.module.log(url)
		while True:
			resp, info = fetch_url(self.module, url, headers=headers, method="GET", data=urlencode({'output_mode':'json'}))

			if info["status"] != 200:
				self.parseErrorResponse(info)
	
			content = json.loads(resp.read())
			yield content

			if not self.hasmorepages(content['paging']):
				break
			
			s = urlsplit(url)
			qs = parse_qs(s.query)
			offset = int(qs.get('offset', [0])[0])
			offset += 1
			qs["offset"] = [ offset ]
			query = urlencode(dict((k, v[0]) for k, v in qs.items()))
			s = list(s)
			s[3] = query
			url = urlunsplit(s)
			# self.module.log("Going to get: %s" % (url))
			
	def hasmorepages(self, paging):
		perpage = paging.get('perPage', 1)
		total = paging.get('total', 1)
		offset = paging.get('offset', 1)
		# self.module.log("Has more pages?: %d, %d, %d" % (perpage, total, offset))
		return total/perpage > offset

	def parseErrorResponse(self, resp):
		try:
			r = json.loads(resp.get('body', None))
		except:
			self.module.fail_json(msg="Received error response but was unable to parse it")
		
		# messages _could_ contain multiple entries. I have not seen that happen so I'll just parse the first message only. 
		err = r['messages'][0]
		self.module.fail_json(msg="{}: {}".format(err['type'], err['text']))		

	def get_all(self):
		return None

	def should_disable(self):
		return self.module.params.get('state', '') == 'disabled'

	def should_delete(self):
		return self.module.params.get('state', '') == 'absent'	

	def diff(self):
		update = False

		should_delete = self.should_delete()
		a = self.get_single()
		if a is None:
			if should_delete:
				self.module.exit_json(changed=False)
			else:
				self.add()
		else:
			if should_delete:
				self.delete()
		
		should_disable = self.should_disable()
		is_disabled = a.get('disabled', False)

		if is_disabled != should_disable:
			self.disable(should_disable)

		for k, v in a.iteritems():
			if k == 'disabled':
				continue
			
			self.module.log("{} = {} ({})" . format(k, v, self.module.params.get(k, "")))
			if type(v) == list:
				cur = self.module.params.get(k, [])

				if len(v) != len(cur):
					update = True
				# item is in v but not in cur
				elif bool([item for item in v if item not in cur]):
					update = True
				# item is in cur but not in v
				elif bool([item for item in cur if item not in v]):
					update = True
				
			elif str(self.module.params.get(k, '')) != str(v):
				update = True
		
			self.module.log(str(update))

		if update:
			self.update()

		self.module.exit_json(changed=False)

	def get_single(self):
		for i in self.get_all():
			if i['name'] == self.module.params['name']:
				return i
		return None

	def add(self):
		data = self.data()
		data.update(
			name=self.module.params['name'],
			disabled='1' if self.should_disable() else '0',
		)
		resp, info = fetch_url(self.module, self.base_endpoint, data=urlencode(data), headers=self.default_headers(), method='POST', timeout=300)

		if info['status'] == 201:
			self.module.exit_json(changed=True)

		self.parseErrorResponse(info)

	def update(self):
		url = "{}/{}" . format(self.base_endpoint, self.module.params['name'])
		resp, info = fetch_url(self.module, url, data=urlencode(self.data()), headers=self.default_headers(), method='POST', timeout=300)

		if info['status'] == 200:
			self.module.exit_json(changed=True)

		self.parseErrorResponse(info)

	def delete(self):
		url = "{}/{}" . format(self.base_endpoint, self.module.params['name'])
		resp, info = fetch_url(self.module, url, headers=self.default_headers(), method='DELETE', timeout=300)

		if info['status'] == 200:
			self.module.exit_json(changed=True)

		self.parseErrorResponse(info)

	def disable(self, disable):
		# self.module.log("Going to {} \"{}\"".format('disable' if disable else 'enable', self.module.params['name']))

		url = "{}/{}" . format(self.base_endpoint, self.module.params['name'])
		data = {
			'output_mode': 'json',
			'disabled': '1' if disable else '0',
		}

		resp, info = fetch_url(self.module, url, data=urlencode(data), headers=self.default_headers(), method='POST', timeout=300)

		if info['status'] == 200:
			self.module.exit_json(changed=True)

		self.parseErrorResponse(info)