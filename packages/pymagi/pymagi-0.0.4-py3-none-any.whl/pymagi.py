import json
import requests

#----------------------------------[+]Connection Check-----------------------------------

def connectioncheck():
	try:
		requests.get("http://localhost:3000")
	except:
		print("[+]CyberChef Server Down")
		quit()

#----------------------------------[+]Base64-----------------------------------


def base64decode(payload):
	connectioncheck()

	data = json.dumps({"input": payload,"recipe":{"op":"From Base64","args":["A-Za-z0-9+/=",True]},"outputType":"string"})
	API_ENDPOINT = "http://localhost:3000/bake"
	headers_dict = {"Content-Type":"application/json"}

	# #sending post request and saving response as response object
	r = requests.post(url = API_ENDPOINT, headers=headers_dict,data = data)
  
	# # # # extracting response text 
	value_received = json.loads(r.text)

	value = value_received['value']

	return value



def base64encode(payload):
	connectioncheck()

	data = json.dumps({"input": payload,"recipe":{"op":"To Base64","args":["A-Za-z0-9+/="]},"outputType":"string"})
	API_ENDPOINT = "http://localhost:3000/bake"
	headers_dict = {"Content-Type":"application/json"}

	# #sending post request and saving response as response object
	r = requests.post(url = API_ENDPOINT, headers=headers_dict,data = data)
  
	# # # # extracting response text 
	value_received = json.loads(r.text)

	value = value_received['value']

	return value

#----------------------------------[+]Morse-----------------------------------


def morseencode(payload):
	connectioncheck()

	data = json.dumps({"input": payload,"recipe":{"op":"To Morse Code","args":["-/.","Space","Line feed"]},"outputType":"string"})
	API_ENDPOINT = "http://localhost:3000/bake"
	headers_dict = {"Content-Type":"application/json"}

	# #sending post request and saving response as response object
	r = requests.post(url = API_ENDPOINT, headers=headers_dict,data = data)
  
	# # # # extracting response text 
	value_received = json.loads(r.text)

	value = value_received['value']

	return value

def morsedecode(payload):
	connectioncheck()

	data = json.dumps({"input": payload,"recipe":{"op":"From Morse Code","args":["Space","Line feed"]},"outputType":"string"})
	API_ENDPOINT = "http://localhost:3000/bake"
	headers_dict = {"Content-Type":"application/json"}

	# #sending post request and saving response as response object
	r = requests.post(url = API_ENDPOINT, headers=headers_dict,data = data)
  
	# # # # extracting response text 
	value_received = json.loads(r.text)

	value = value_received['value']

	return value

#----------------------------------[+]Base85-----------------------------------


def base85encode(payload):
	connectioncheck()

	data = json.dumps({"input": payload,"recipe":{"op":"To Base85","args":["!-u",False]},"outputType":"string"})
	API_ENDPOINT = "http://localhost:3000/bake"
	headers_dict = {"Content-Type":"application/json"}

	# #sending post request and saving response as response object
	r = requests.post(url = API_ENDPOINT, headers=headers_dict,data = data)
  
	# # # # extracting response text 
	value_received = json.loads(r.text)

	value = value_received['value']

	return value

def base85decode(payload):
	connectioncheck()

	data = json.dumps({"input": payload,"recipe":{"op":"From Base85","args":["!-u"]},"outputType":"string"})
	API_ENDPOINT = "http://localhost:3000/bake"
	headers_dict = {"Content-Type":"application/json"}

	# #sending post request and saving response as response object
	r = requests.post(url = API_ENDPOINT, headers=headers_dict,data = data)
  
	# # # # extracting response text 
	value_received = json.loads(r.text)

	value = value_received['value']

	return value

#----------------------------------[+]atbash-----------------------------------


def atbash(payload):
	connectioncheck()


	data = json.dumps({"input": payload,"recipe":{"op":"Atbash Cipher","args":[]},"outputType":"string"})
	API_ENDPOINT = "http://localhost:3000/bake"
	headers_dict = {"Content-Type":"application/json"}

	# #sending post request and saving response as response object
	r = requests.post(url = API_ENDPOINT, headers=headers_dict,data = data)
  
	# # # # extracting response text 
	value_received = json.loads(r.text)

	value = value_received['value']

	return value

#----------------------------------[+]braille-----------------------------------


def brailleencode(payload):
	connectioncheck()


	data = json.dumps({"input": payload,"recipe":{"op":"To Braille","args":[]},"outputType":"string"})
	API_ENDPOINT = "http://localhost:3000/bake"
	headers_dict = {"Content-Type":"application/json"}

	# #sending post request and saving response as response object
	r = requests.post(url = API_ENDPOINT, headers=headers_dict,data = data)
  
	# # # # extracting response text 
	value_received = json.loads(r.text)

	value = value_received['value']

	return value

def brailledecode(payload):
	connectioncheck()


	data = json.dumps({"input": payload,"recipe":{"op":"From Braille","args":[]},"outputType":"string"})
	API_ENDPOINT = "http://localhost:3000/bake"
	headers_dict = {"Content-Type":"application/json"}

	# #sending post request and saving response as response object
	r = requests.post(url = API_ENDPOINT, headers=headers_dict,data = data)
  
	# # # # extracting response text 
	value_received = json.loads(r.text)

	value = value_received['value']

	return value

	
#----------------------------------[+]binary-----------------------------------


def binaryencode(payload):
	connectioncheck()


	data = json.dumps({"input": payload,"recipe":{"op":"To Binary","args":["Space",8]},"outputType":"string"})
	API_ENDPOINT = "http://localhost:3000/bake"
	headers_dict = {"Content-Type":"application/json"}

	# #sending post request and saving response as response object
	r = requests.post(url = API_ENDPOINT, headers=headers_dict,data = data)
  
	# # # # extracting response text 
	value_received = json.loads(r.text)

	value = value_received['value']

	return value

def binarydecode(payload):
	connectioncheck()


	data = json.dumps({"input": payload,"recipe":{"op":"From Binary","args":["Space",8]},"outputType":"string"})
	API_ENDPOINT = "http://localhost:3000/bake"
	headers_dict = {"Content-Type":"application/json"}

	# #sending post request and saving response as response object
	r = requests.post(url = API_ENDPOINT, headers=headers_dict,data = data)
  
	# # # # extracting response text 
	value_received = json.loads(r.text)

	value = value_received['value']

	return value

#----------------------------------[+]octal-----------------------------------


def octalencode(payload):
	connectioncheck()


	data = json.dumps({"input": payload,"recipe":{"op":"To Octal","args":["Space"]},"outputType":"string"})
	API_ENDPOINT = "http://localhost:3000/bake"
	headers_dict = {"Content-Type":"application/json"}

	# #sending post request and saving response as response object
	r = requests.post(url = API_ENDPOINT, headers=headers_dict,data = data)
  
	# # # # extracting response text 
	value_received = json.loads(r.text)

	value = value_received['value']

	return value

def octaldecode(payload):
	connectioncheck()


	data = json.dumps({"input": payload,"recipe":{"op":"From Octal","args":["Space"]},"outputType":"string"})
	API_ENDPOINT = "http://localhost:3000/bake"
	headers_dict = {"Content-Type":"application/json"}

	# #sending post request and saving response as response object
	r = requests.post(url = API_ENDPOINT, headers=headers_dict,data = data)
  
	# # # # extracting response text 
	value_received = json.loads(r.text)

	value = value_received['value']

	return value

#----------------------------------[+]base32-----------------------------------


def base32encode(payload):
	connectioncheck()


	data = json.dumps({"input": payload,"recipe":{"op":"To Base32","args":["A-Z2-7="]},"outputType":"string"})
	API_ENDPOINT = "http://localhost:3000/bake"
	headers_dict = {"Content-Type":"application/json"}

	# #sending post request and saving response as response object
	r = requests.post(url = API_ENDPOINT, headers=headers_dict,data = data)
  
	# # # # extracting response text 
	value_received = json.loads(r.text)

	value = value_received['value']

	return value

def base32decode(payload):
	connectioncheck()


	data = json.dumps({"input": payload,"recipe":{"op":"From Base32","args":["A-Z2-7="]},"outputType":"string"})
	API_ENDPOINT = "http://localhost:3000/bake"
	headers_dict = {"Content-Type":"application/json"}

	# #sending post request and saving response as response object
	r = requests.post(url = API_ENDPOINT, headers=headers_dict,data = data)
  
	# # # # extracting response text 
	value_received = json.loads(r.text)

	value = value_received['value']

	return value

#----------------------------------[+]base58-----------------------------------



def base58encode(payload):
	connectioncheck()


	data = json.dumps({"input": payload,"recipe":{"op":"To Base58","args":["123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"]},"outputType":"string"})
	API_ENDPOINT = "http://localhost:3000/bake"
	headers_dict = {"Content-Type":"application/json"}

	# #sending post request and saving response as response object
	r = requests.post(url = API_ENDPOINT, headers=headers_dict,data = data)
  
	# # # # extracting response text 
	value_received = json.loads(r.text)

	value = value_received['value']

	return value

def base58decode(payload):
	connectioncheck()


	data = json.dumps({"input": payload,"recipe":{"op":"From Base58","args":["123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"]},"outputType":"string"})
	API_ENDPOINT = "http://localhost:3000/bake"
	headers_dict = {"Content-Type":"application/json"}

	# #sending post request and saving response as response object
	r = requests.post(url = API_ENDPOINT, headers=headers_dict,data = data)
  
	# # # # extracting response text 
	value_received = json.loads(r.text)

	value = value_received['value']

	return value

#----------------------------------[+]base62-----------------------------------


def base62encode(payload):
	connectioncheck()


	data = json.dumps({"input": payload,"recipe":{"op":"To Base62","args":["0-9A-Za-z"]},"outputType":"string"})
	API_ENDPOINT = "http://localhost:3000/bake"
	headers_dict = {"Content-Type":"application/json"}

	# #sending post request and saving response as response object
	r = requests.post(url = API_ENDPOINT, headers=headers_dict,data = data)
  
	# # # # extracting response text 
	value_received = json.loads(r.text)

	value = value_received['value']

	return value

def base62decode(payload):
	connectioncheck()


	data = json.dumps({"input": payload,"recipe":{"op":"From Base62","args":["0-9A-Za-z"]},"outputType":"string"})
	API_ENDPOINT = "http://localhost:3000/bake"
	headers_dict = {"Content-Type":"application/json"}

	# #sending post request and saving response as response object
	r = requests.post(url = API_ENDPOINT, headers=headers_dict,data = data)
  
	# # # # extracting response text 
	value_received = json.loads(r.text)

	value = value_received['value']

	return value


#----------------------------------[+]url-----------------------------------



def urlencode(payload):
	connectioncheck()


	data = json.dumps({"input": payload,"recipe":{"op":"URL Encode","args":[True]},"outputType":"string"})
	API_ENDPOINT = "http://localhost:3000/bake"
	headers_dict = {"Content-Type":"application/json"}

	# #sending post request and saving response as response object
	r = requests.post(url = API_ENDPOINT, headers=headers_dict,data = data)
  
	# # # # extracting response text 
	value_received = json.loads(r.text)

	value = value_received['value']

	return value

def urldecode(payload):
	connectioncheck()


	data = json.dumps({"input": payload,"recipe":{"op":"URL Decode","args":[True]},"outputType":"string"})
	API_ENDPOINT = "http://localhost:3000/bake"
	headers_dict = {"Content-Type":"application/json"}

	# #sending post request and saving response as response object
	r = requests.post(url = API_ENDPOINT, headers=headers_dict,data = data)
  
	# # # # extracting response text 
	value_received = json.loads(r.text)

	value = value_received['value']

	return value



#----------------------------------[+]html-----------------------------------



def htmlencode(payload):
	connectioncheck()


	data = json.dumps({"input": payload,"recipe":{"op":"To HTML Entity","args":[True,"Named entities"]},"outputType":"string"})
	API_ENDPOINT = "http://localhost:3000/bake"
	headers_dict = {"Content-Type":"application/json"}

	# #sending post request and saving response as response object
	r = requests.post(url = API_ENDPOINT, headers=headers_dict,data = data)
  
	# # # # extracting response text 
	value_received = json.loads(r.text)

	value = value_received['value']

	return value

def htmldecode(payload):
	connectioncheck()


	data = json.dumps({"input": payload,"recipe":{"op":"From HTML Entity","args":[True,"Named entities"]},"outputType":"string"})
	API_ENDPOINT = "http://localhost:3000/bake"
	headers_dict = {"Content-Type":"application/json"}

	# #sending post request and saving response as response object
	r = requests.post(url = API_ENDPOINT, headers=headers_dict,data = data)
  
	# # # # extracting response text 
	value_received = json.loads(r.text)

	value = value_received['value']

	return value