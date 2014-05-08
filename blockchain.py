#!/usr/bin/env python
# title          : blockchain.py
#description     : BlockChain.info API library
#author          : p4u <p4u@dabax.net>
#based work on   : Justin Allen
#date            : 20140510
#version         : 0.1.0
#notes           :
#license         : GNU GPLv3 http://www.gnu.org/licenses/
#python_version  : 3  
#==============================================================================

import requests
import urllib
import json


class Wallet: 
	guid		= ''
	isAccount 	= 0
	isKey 		= 0
	password1 	= ''
	password2 	= ''
	url 		= ''
	verbose = True

	def __init__(self, guid = '', password1 = '', password2 = ''):

		if guid.count('-') > 0:
			self.isAccount = 1
			if password1 == '': # wallet guid's contain - 
				raise ValueError('No password with guid.')
		else:
			self.isKey = 1

		self.guid = guid
		self.url = 'https://blockchain.info/merchant/' + guid + '/'

		self.password1 = password1
		self.password2 = password2


	def call(self, method, data = {}):
		if self.password1 != '':
			data["password"] = self.password1
		if self.password2 != '':
			data['second_password'] = self.password2
		if self.verbose:
			print("Url:%s\nMethod:%s\nData:%s" %(self.url,method,data))
		response = requests.post(self.url + method, params=data)
		json = response.json
		if 'error' in json:
			raise RuntimeError('ERROR: ' + json['error'])

		return json


	def getBalance(self):
		response = self.call('balance')
		return response['balance']


	def getAddressBalance(self,addr = '', confirm = 4):
		data = {"address": addr , "confirmations": confirm }

		response = self.call('address_balance', data)
		return response['balance']


	def getAddresses(self, confirm = 4):
		data = {"confirmations": confirm }
		response = self.call('list', data)
		return response['addresses']


	def newAddress(self, label = ''):
		if self.isKey:
			raise ValueError('Key\'s cannot generate addresses?') 

		response = ''

		if label != '':
			response = self.call('new_address', {"label": label})
		else:
			response = self.call('new_address')

		return response['address']


	def sendPayment(self, toaddr, amount , fromaddr = False, shared = False, fee = 0.0005, note = False):
		data = {}
		data['to'] = toaddr
		data['amount'] = amount
		data['fee'] = fee

		if fromaddr:
			data['from'] = fromaddr
		if shared:
			data['shared'] = 'true'
		if note:
			data['note'] = note
		response = self.call('payment',data)

		return response


	def sendManyPayment(self, recipients = {} , fromaddr = False, shared = False, fee = 0.0005, note = False):
		data = {}
		data['recipients'] = urllib.parse.urlencode(recipients)
		data['fee'] = fee
		if fromaddr:
			data['from'] = fromaddr
		if shared:
			data['shared'] = 'true'
		else:
			data['shared'] = 'false'
		if note:
			data['note'] = note

		response = self.call('sendmany',data)
		return response
