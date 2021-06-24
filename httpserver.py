'''Stefano Vanucci MATRICOLA: 0000938120 '''

#!/bin/env python
import sys, signal
import http.server
import socketserver
import base64

from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler

class AuthHandler(SimpleHTTPRequestHandler):
    ''' Main class to present webpages and authentication. '''
    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Auth\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.path.endswith('users.txt'):
            self.do_AUTHHEAD()
            self.wfile.write('Unauthorized')
        ''' Present frontpage with user authentication. '''
        if self.headers.get('Authorization') == None:
            self.do_AUTHHEAD()
            self.wfile.write('No auth header received')
        else:
            if authenticateUser(self.headers.get('Authorization')):
                SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.do_AUTHHEAD()
                self.wfile.write(self.headers.get('Authorization'))
                self.wfile.write('Not authenticated')


server = socketserver.ThreadingTCPServer(('',8080), AuthHandler )

server.daemon_threads = True  

server.allow_reuse_address = True  

#Funzione di autenticazione
def authenticateUser(token):
    lines = []
    print('TOKEN: ' + token)
    decoded = base64.b64decode((token.replace('Basic', '')).strip()).decode('UTF-8') 
    print('DECODED: ' + decoded)
    with open("users.txt","r") as f:
        lines = f.readlines()

    for line in lines:
        print('NUOVA LINEA: ' + line)
        if(line == decoded):
            return True
            
    return False
#Funzione per permettere l'uscita attraverso Ctrl+C
def signal_handler(signal, frame):
    print( 'Exiting http server (Ctrl+C pressed)')
    try:
      if( server ):
        server.server_close()
    finally:
      sys.exit(0)

#Interrompe l’esecuzione se da tastiera arriva la sequenza (CTRL + C) 
signal.signal(signal.SIGINT, signal_handler)

#Loop infinito
try:
  while True:
    sys.stdout.flush()
    server.serve_forever()
except KeyboardInterrupt:
  pass

server.server_close()