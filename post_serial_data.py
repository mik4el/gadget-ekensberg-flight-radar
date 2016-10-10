import os
import subprocess
import serial
from time import strftime
import requests
from datetime import datetime, timedelta
import threading
import queue
import time
import json

class DataAuther:

	def __init__(self, username, password, base_url):
		self.login_url = base_url + '/backend/api-token-auth/'
		self.username = username
		self.password = password
		self.token = None

	def auth_and_get_token(self):
		credentials = {'username':self.username, 'password':self.password}
		r = requests.post(self.login_url, json=credentials)
		self.token=r.json()['token']
		return self.token


class DataPosterWorker(threading.Thread):

	def __init__(self, token, base_url, data_string, status_queue):
		threading.Thread.__init__(self)
		gadget_slug = "ekensberg-flight-radar" 
		self.post_url = base_url+'/backend/api/v1/gadgets/'+gadget_slug+'/data/'
		self.headers = {'Authorization': 'Bearer '+ token}
		self.data_string = data_string
		self.status_queue = status_queue

	def run(self):
		self.post_data_from_string(self.data_string)

	def update_status(self, message):
		self.status_queue.put(message)

	def post_data(self, data):
		now = datetime.now() - timedelta(hours=2)  # convert to Z timezone
		payload = {
			'data':data,
			'timestamp': now.isoformat()
		}
		try:
			r = requests.post(self.post_url, json=payload, headers=self.headers)
		except:
			self.update_status("Error when posting.")
			return
		if r.status_code != 201:
			self.update_status(r.status_code)
			self.update_status(r.json())
			self.update_status("Request not ok when posting.")
		else:
			self.update_status("Posted: '{}'".format(data))

	def data_from_string(self, data_string):
		# validate data or update status
		data = json.loads(data_string)
		assert(len(data)>0)
		return data

	def post_data_from_string(self, data_string):
		self.post_data(self.data_from_string(data_string))


if __name__ == '__main__':
	username = os.environ.get('GADGET_DATA_POSTER_USERNAME', None)
	password = os.environ.get('GADGET_DATA_POSTER_PASSWORD', None)
	base_url = os.environ.get('GADGET_DATA_POSTER_URL', '')
	dump1090_cmd = os.environ.get('DUMP1090_COMMAND', '')
	
	# start dump1090 in background
	subprocess.Popen(dump1090_cmd, shell=True)

	status_queue = queue.Queue()
	data_auther = DataAuther(username, password, base_url)
	token = data_auther.auth_and_get_token()
	time_since_get = time.time()-1000  # initialize timer for first iteration
	try:
		while True:
			while not status_queue.empty():
				try:
					message = status_queue.get()
				except queue.Empty:
					pass
				else:
					print("{:%Y-%m-%d %H:%M} {}" .format(datetime.now(),message))
					if message == "Request not ok when posting.":
						# reauth
						token = data_auther.auth_and_get_token()
						print("Token updated.")
						with status_queue.mutex:
							status_queue.queue.clear()


			# Get data
			if (time.time()-time_since_get>60.0):
				time_since_get = time.time()
				get_url = "http://localhost:8080/data.json"
				r = requests.get(get_url)
				data = r.text
				
				if data is not None:
					# Upload if data ok
					data_poster = DataPosterWorker(token, base_url, data, status_queue)
					data_poster.start()
				log_message = "{:%Y-%m-%d %H:%M} {}" .format(datetime.now(),data)
				with open('gadget-ekensberg-flight-radar.log','a') as logfile:
					print(log_message, file=logfile)
				print(log_message)

			
	except KeyboardInterrupt:
		print("\ndone")
