import yaml

def main():
	"""Test BD extractor"""
	print "Running extract test"

def extract(dts, file, wait=60, key=''):
	"""
	Extract derived data from the given input file's contents via DTS.
	@param dts: The URL to the Data Tilling Service to use.
	@param file: The input file.
	@param wait: The amount of time to wait for the DTS to respond.  Default is 60 seconds.
	@param key: The key for the DTS. Default is ''.
	@return: The filename of the JSON file containing the extracted data.
	"""
	username = ''
	password = ''
	metadata = ''

	#Check for authentication
	if '@' in dts:
		parts = dts.rsplit('@', 1)
		dts = parts[1]
		parts = parts[0].split(':')
		username = parts[0]
		password = parts[1]

	#Upload file
	file_id = ''

	if(file.startswith('http://')):
		data = {}
		data["fileurl"] = file

		if key:
			file_id = requests.post('http://' + dts + ':9000/api/extractions/upload_url?key=' + key, headers={'Content-Type': 'application/json'}, data=json.dumps(data)).json()['id']
		else:
			file_id = requests.post('http://' + dts + ':9000/api/extractions/upload_url?key=' + key, auth=(username, password), headers={'Content-Type': 'application/json'}, data=json.dumps(data)).json()['id']
	else:
		if key:
			file_id = requests.post('http://' + dts + ':9000/api/extractions/upload_file?key=' + key, files={'File' : (os.path.basename(file), open(file))}).json()['id']
		else:
			file_id = requests.post('http://' + dts + ':9000/api/extractions/upload_file?key=' + key, auth=(username, password), files={'File' : (os.path.basename(file), open(file))}).json()['id']

	#Poll until output is ready
	if file_id:
		while wait > 0:
			status = requests.get('http://' + dts + ':9000/api/extractions/' + file_id + '/status').json()
			if status['Status'] == 'Done': break
			time.sleep(1)
			wait -= 1

		#Display extracted content (TODO: needs to be one endpoint!!!)
		metadata = requests.get('http://' + dts + ':9000/api/files/' + file_id + '/tags').json()
		metadata['technicalmetadata'] = requests.get('http://' + dts + ':9000/api/files/' + file_id + '/technicalmetadatajson').json()
		metadata['versusmetadata'] = requests.get('http://' + dts + ':9000/api/files/' + file_id + '/versus_metadata').json()

	return metadata

if __name__ == "__main__":
    main()