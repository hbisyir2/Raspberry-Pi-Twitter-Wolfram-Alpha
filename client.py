#!/usr/bin/python
 
import socket   #for sockets
import sys  #for exit
import hashlib #for hashes
import pickle #for pickling
import shlex
from twython import TwythonStreamer
from twython import Twython

consumer_key = 'cwprnikWusVvHw3yqjTsGcSjq'
consumer_secret = 'zMJfCUpq3GwGvkfXzyZORjSApxlURCDR594dcZN6vKg94x4VyI'
access_token = '828979421306613760-auf4iGihUObzqXF5q7raDABPhROp3WI'
access_token_secret = 'HL9HCaEnoEIaZprJKFC8eWWb7H1QS1DluNLiYIIn6Omiz'

tweetReceived = False


class MyStreamer(TwythonStreamer):
    print("Waiting on Tweet...")
    def on_success(self, data):
        if 'text' in data:
            tweet = shlex.split(data['text'])
        if len(tweet) == 3:
            print(tweet)
            question = tweet[2]
            host = tweet[1].split(':')[0]
            port = tweet[1].split(':')[1]
            print("Address:", host)
            print("Port:", port)
            print("Question:", question)

            # create an INET, STREAMing socket
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except socket.error:
                print('Failed to create socket')
                sys.exit()

            print('Socket Created')

            try:
                remote_ip = socket.gethostbyname(host)

            except socket.gaierror:
                # could not resolve
                print('Hostname could not be resolved. Exiting')
                sys.exit()

            # Connect to remote server
            s.connect((remote_ip, int(port)))

            print('Socket Connected to ' + host + ' on ip ' + remote_ip)

            # Send some data to remote server
            message = question
            message_bytes = message.encode('utf-8')
            checksum = hashlib.md5()
            checksum.update(message_bytes)
            checkstring = checksum.hexdigest()
            tuple = (message, checkstring)
            tupledump = pickle.dumps(tuple)

            try:
                # Set the whole string
                # s.sendall(bytes(message, encoding="ascii"))
                s.sendall(tupledump)
            except socket.error:
                # Send failed
                print('Send failed')
                sys.exit()

            print('Message send successfully')

            # Now receive data
            reply = s.recv(4096)
            answer = pickle.loads(reply)
            messager = answer[0]
            scheck = answer[1]
            bytesmessager = messager.encode('utf-8')
            checksum = hashlib.md5()
            checksum.update(bytesmessager)
            checkstring2 = checksum.hexdigest()

            answers = messager.split('\n')
            for a in answers:
                m = "@" + data['in_reply_to_screen_name'] + " #\"" + a + "\""
                twitter.update_status(status=m)
                print("Tweeted answer(s)")

            print('Reply from server: ' + messager)
            print('Checksum generated: ' + checkstring2)
            print('Checksum received: ' + scheck)
            if scheck == checkstring2:
                print('Checksums match!')
            else:
                print('Checksums are incorrect')

            data.clear()

stream = MyStreamer(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
    )

stream.statuses.filter(track='@ECE4564SQUAAAAD')
