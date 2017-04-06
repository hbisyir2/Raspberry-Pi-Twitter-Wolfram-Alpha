import socket
import sys
import hashlib
import pickle
import wolframalpha

app_id = "8PQ4UW-QTTRJG78EW" #wolfram alpha account number

HOST = ''
PORT = 8888

client = wolframalpha.Client(app_id) #opens wolfram client

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates socket connection
print ('Socket created')

try:
	s.bind((HOST, PORT))
except (socket.error, msg):
	print ('Bind failed. Error Code: ' + str(msg[0]) + 'message ' + msg[1])
	sys.exit()

print ('Socket bind complete')

s.listen(10)
print ('Socket now listening...')

while 1:
	conn, addr = s.accept()
	print ('\nconnected with ' + addr[0] + ':' + str(addr[1]))

	data = conn.recv(1024) #recieves data from client
	m = hashlib.md5() #for checksum generation
	datapickle = pickle.loads(data) #unpickles the tuple
	question = datapickle[0] #separates tuple into question and checksum
	rec_checksum = datapickle[1]
	question_bytes = question.encode('utf-8')
	m.update(question_bytes)
	q_checksum = m.hexdigest() #generates new checksum
	print ('question recieved: ' + question) #prints relavant information
	print ('checksum recieved: ' + rec_checksum) #and compares checksums
	print ('checksum generated: ' + q_checksum)
	if (rec_checksum == q_checksum):
		print ('Checksums match!')
	else:
		print ('Different checksums!')
	res = client.query(question) #generates answer from wolfram alpha
	answer = ""
	try:
		answer = (next(res.results).text)
	except Exception:
		answer = "invalid question"
	m = hashlib.md5() #generates checksum for answer
	answer_bytes = answer.encode('utf-8')
	m.update(answer_bytes)
	a_checksum = m.hexdigest()
	print ('answer recieved: ' + answer) #prints relavant information
	print ('checksum generated from answer: ' + a_checksum)
	if not data:
		break
	replytup = (answer, a_checksum) #creates response payload
	reply = pickle.dumps(replytup) #pickles the payload
	conn.sendall(reply) #sends response
	print ('sent reply to client\nSocket now listening...') #listens for new connection

conn.close()
s.close()
