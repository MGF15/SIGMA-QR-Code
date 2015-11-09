#!/usr/bin/python
#SIGMA QR-Code 
#Coded by MGF15

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import os , pyqrcode 
from urllib import unquote

PORT_NUMBER = 8080
Dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
final = open(Dir+'QR.html','r').read()

class myHandler(BaseHTTPRequestHandler):
	
	def do_GET(self):
		if self.path=="/":
			self.path="/index.html"
		try:
			sendReply = False
			if self.path.endswith(".html"):
				type='text/html'
				sendReply = True
			if self.path.endswith(".css"):
				type='text/css'
				sendReply = True
			if self.path.endswith(".svg"):
				type='image/svg+xml'
				sendReply = True
			if sendReply == True:
				f = open(Dir + self.path) 
				self.send_response(200)
				self.send_header('Content-type',type)
				self.end_headers()
				html = f.read()
				self.wfile.write(html)
				f.close()
			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)
	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		t = self.rfile.read(content_length)
		v = unquote(t).decode('utf8')
		if v.split('=')[0] == 'Link' :
			Qr = v.split('=')[1]
			qr = pyqrcode.create(Qr)
			qr.svg('qr-code.svg', scale=9)
		if v.split('=')[0] == 'Play' :
			Qr = v.split('Play=')[1]
			qr = pyqrcode.create(Qr)
			qr.svg('qr-code.svg', scale=7)
		if v.split('=')[0] == 'Text' :
			Qr = v.split('=')[1]
			qr = pyqrcode.create(Qr)
			qr.svg('qr-code.svg', scale=9)
		if v.split('=')[0] == 'Tel' :
			Qr = v.split('=')[1]
			qr = pyqrcode.create('TEL:'+Qr)
			qr.svg('qr-code.svg', scale=9)
		if v.split('=')[0] == 'Sms':
			sms = v.replace('&','=').split('=')
			SMs = 'SMSTO:'+sms[1]+':'+sms[3].replace('+',' ')
			qr = pyqrcode.create(SMs)
			qr.svg('qr-code.svg', scale=9)
		if v.split('=')[0] == 'BTC':
			Qr = v.split('=')[1]
			qr = pyqrcode.create(Qr)
			qr.svg('qr-code.svg', scale=9)
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		s = final.replace('qr-code','qr-code.svg')
		self.wfile.write(s)
		
server = HTTPServer(('127.0.0.1', PORT_NUMBER), myHandler)
print '[+] Open LocalHost in Your Browser on Port' , PORT_NUMBER
print '\n[+] Started httpserver on port ' , PORT_NUMBER

server.serve_forever()
