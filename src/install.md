# Ref Manager installation guide

## Install dependencies on Mac OS X
### Intall Apple Xcode and Command Line Tools
…
### Install Homebrew
    ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"
    brew update
    brew doctor

### Install MongoDB
Install MongoDB with brew:

    brew install mongodb

Create a data folder for the AIME MongoDB:

	mkdir $HOME/somewhere

Start MongoDB:

    mongod --dbpath $HOME/somewhere
    
### Install pip
    easy_install pip


## Install dependencies on Ubuntu

### Intall MongoDB

Import the 10gen public GPG Key:

    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10

If the port is blocked by the firewall:
    
    nmap -p 11371 keyserver.ubuntu.com

You have to do this manualy:

    keydir="/var/tmp/10gen-key"
    mkdir -p $keydir
    wget -O $keydir/10gen-gpg-key.asc http://docs.mongodb.org/10gen-gpg-key.asc
    sudo apt-key add $keydir/10gen-gpg-key.asc 
    rm -rf $keydir

Then include the following line for the 10gen repository:
    
    vi /etc/apt/sources.list.d/10gen.list
    deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen

Update apt-get:

    sudo apt-get update
    
Install Packages:

    sudo apt-get install mongodb-10gen

Configure MongoDB:

    vi /etc/mongodb.conf
    
Control script:

    vi /etc/init.d/mongodb

This MongoDB instance will store its data files in the /var/lib/mongodb and its log files in /var/log/mongodb, and run using the mongodb user account.

Starting MongoDB:

    sudo service mongodb start
    
You can verify that mongod has started successfully by checking the contents of the log file at /var/log/mongodb/mongodb.log.

Stopping MongoDB:

    sudo service mongodb stop
    
Restarting MongoDB:

    sudo service mongodb restart
    
### Install python VirtualEnv

Install virtualenv and virtualenvwrapper:

    sudo apt-get install python-virtualenv
    sudo pip install virtualenvwrapper
 
Create AIME virtualenv:

    virtualenv AIME

Switch to the AIME virtualenv:
    
    source ~/AIME/bin/activate
    
To deactivate:
	
	deactivate
    
## Intall dependencies on both Mac OS X and Ubuntu

### Install python VirtualEnv

Install virtualenv and virtualenvwrapper:

    sudo pip install virtualenv
	sudo pip install virtualenvwrapper
	
Create the .virtualenv folder:

	mkdir .virtualenv
	
Configure your batch profile:
	
	cd ~
	vi .profile

Add these lines to the .profile file in your home directory:

    # Python Virtual Env
    export WORKON_HOME=$HOME/.virtualenv
    source /usr/local/bin/virtualenvwrapper.sh
    export PIP_VIRTUALENV_BASE=$WORKON_HOME
    export PIP_RESPECT_VIRTUALENV=true
    alias v=workon
    alias v.deactivate=deactivate
    alias v.mk='mkvirtualenv --no-site-packages'
    alias v.mk_withsitepackages='mkvirtualenv'
    alias v.rm=rmvirtualenv
    alias v.switch=workon
    alias v.add2virtualenv=add2virtualenv
    alias v.cdsitepackages=cdsitepackages
    alias v.cd=cdvirtualenv
    alias v.lssitepackages=lssitepackages

Exit and relog.

### Install required modules in python

Create the AIME virtualenv:

	mkdir .virtualenv
    v.mk AIME

Switch to the AIME virtualenv:

    v AIME

Install required modules:
    
    pip install -r requirements.txt    add2virtualenv .        
Install the correct txjsonrpc:

	git clone git@github.com:hefee/txjsonrpc.git
	cd txjsonrpc
	sudo python setup.py install


Clone the git repository:

    git clone git@github.com:medialab/aime.git
    
To update the source:
    
    git pull
	

## Configure

### Configure MongoDB:

Create the MongoDB

    mongo
	db
	show dbs
	use aime-biblio
	j = { name : "mongo" }
	db.references.insert( j )
	show dbs
	show collections
	
Edit the repository conf:

	cd aime/biblio_data/repository
    vi mongodb_repository.py
    
Modify the config dict:

    config={
    "host": "localhost",
    "port": 27017,
    "db": "aime-biblio",
    "refCol": "references"
    }
    
###Configure JSON-RPC:
Edit the json-rpc conf:

	cd aime/biblio_data/dissemination
    vi metajsonrpc.tac

Modify the json-rpc port:

    port = 8980
    
   
### Test
To test all (convert endnote, insert ref inside MongoDB, export json and MLA):

	v AIME
	cd aime/biblio_data/test
    python test_all.py
    
To start the json-rpc server:

	v AIME
	cd aime/biblio_data/dissemination
    twistd -noy metajsonrpc.tac -l -
    
or 

	twistd -noy metajsonrpc.tac -l server.log $


Modify the HTML page to test the json-rpc server
    
    cd aime/biblio_data/test
    vi test_metajsonrpc.html
    
Modify the endPoint:
	
	endPoint : 'http://aime.medialab.sciences-po.fr:8980',
	
Try this web page in your browser

...