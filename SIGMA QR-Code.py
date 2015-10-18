#!/usr/bin/python
#SIGMA QR-Code (URL)
#Coded by dogo h@ck (MGF15)

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep 
import pyqrcode

PORT_NUMBER = 8080
finl = '''
<html>
<title>&#931; QR Code</title>
<head>
<style>

body{
	background-color:#4DAFED;

}
.Qr img{
	padding-left: px;
	padding-top: 20px
}
p{
	font-size: 27px;
	text-align: center;

}
span{
	
	font-size: 29px;
	color: #ACD286;
}
b {
	font-size:29px;
	color :#ACD286;
}
a{
	text-decoration:none
}
a:hover{
	color :#ACD286; 
	
}

</style>
</head>
<body>
<p>Your QR Code </p>

<center>
<b>URL = </b><a href ="http://google.com" ><span>http://google.com</span></a></span>
<div class="Qr">
<img src="url.svg">
</div>
</center>
</body>
</html>
'''

class myHandler(BaseHTTPRequestHandler):
	
	def do_GET(self):
		if self.path=="/":
			self.path="/index.html"
		try:
			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True
			if self.path.endswith(".svg"):
				mimetype='image/svg+xml'
				sendReply = True
			if sendReply == True:
				f = open(curdir + sep + self.path) 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)
	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		file_content = self.rfile.read(content_length)
		g = file_content.split('url=')
		w = g[1].replace('%3A',':').replace('%2F','/')
		url = pyqrcode.create(w)
		url.svg('url.svg', scale=9)
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write(finl.replace('site',w))
		
server = HTTPServer(('', PORT_NUMBER), myHandler)
print '[+] Open LocalHost in Your Browser on Port' , PORT_NUMBER
print '\n[+] Started httpserver on port ' , PORT_NUMBER

server.serve_forever()
