Libraries used:
	socket
	sys
	hashlib
	pickle
	shlex
	twython
	requests
	wolframalpha
	
To initialize server, run server.py. Server will wait for a connection from a client.

To initialize client, run client.py. Client will start listening for a tweet containing "@ECE4564SQUAAAAD"

Tweet format:
	@ECE4564SQUAAAAD address:port "Question"
	
	ex. 
		@ECE4564SQUAAAAD 192.168.1.1:8888 "What time is is?"