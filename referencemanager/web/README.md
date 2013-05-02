how to run this test
===

Welcome to the test part of the reference manager.

Let's use `~/remanager` as our project home directory, and `remanager` the installed virtualenv name. 

Normally, this should be your installation path:
	
	~/remanager
		README.md
		+ mongodb/
			# contain all db files
			...
		+ src/
			+ test/
				index.html
				...
			+ dissemination/
				metajsonrpc.tac
				...
			...


Voila some basic steps in order to get it running:

1. start mongo daemon
 
		$ cd ~/remanager/mongodb
		$ mongod --path .

1. start twisted server to handle jsonRPC requests (we use the workon command available with virtualenvwrapper). Twisted will use localhost:8080 (feel free to change it at the very beginning of the metajsonrpc.tac file)
		
		$ cd ~/remanager/src/dissemination
		$ workon remanager
		(remanager)$ twistd -noy metajsonrpc.tac -l -

1. start a simple server to serve index.html page (necessary for .less dependencies)

		$ cd ~/remanager/src/test
		$ python -m SimpleHTTPServer 8090
		
	
Normally, the index page should be aivailable under `http://localhost:8090/`
	


