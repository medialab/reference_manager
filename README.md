# BibLib

## 1. Install dependencies

### 1.1. For Mac OS X

#### Intall Apple Xcode and Command Line Tools
…
#### Install Homebrew

    ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"
    brew update
    brew doctor

#### Install MongoDB

Install MongoDB with brew:

    brew install mongodb

Create a data folder for the BibLib MongoDB:

    mkdir $HOME/somewhere

Start MongoDB:

    mongod --dbpath $HOME/somewhere/mongodb

#### Install pip

    easy_install pip

#### Install python VirtualEnv

Install virtualenv and virtualenvwrapper:

    sudo pip install virtualenv
    sudo pip install virtualenvwrapper


### 1.2. For Ubuntu

#### Intall MongoDB

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
    
#### Install pip

    easy_install pip

#### Install python VirtualEnv

Install virtualenv and virtualenvwrapper:

    sudo apt-get install python-virtualenv
    sudo pip install virtualenvwrapper

### 1.2. For CentOS

#### Intall MongoDB

See the online documentation: [Install MongoDB on Red Hat Enterprise, CentOS, or Fedora Linux](http://docs.mongodb.org/manual/tutorial/install-mongodb-on-red-hat-centos-or-fedora-linux/ "Install MongoDB on Red Hat Enterprise, CentOS, or Fedora Linux")

Create the file /etc/yum.repos.d/mongodb.repo
with:
	[mongodb]
	name=MongoDB Repository
	baseurl=http://downloads-distro.mongodb.org/repo/redhat/os/x86_64/
	gpgcheck=0
	enabled=1

Then install the packages:

	yum install mongo-10gen mongo-10gen-server

	service mongod start

	chkconfig mongod on
	
##### Install Python

	## Python 2.7:
	wget http://python.org/ftp/python/2.7.5/Python-2.7.5.tar.bz2
	tar xf Python-2.7.5.tar.bz2
	cd Python-2.7.5
	./configure --prefix=/usr/local
	make -j4
	make altinstall

	## Distribute et pip
	wget http://pypi.python.org/packages/source/d/distribute/distribute-0.6.35.tar.gz
	tar xfz distribute-0.6.35.tar.gz
	cd distribute-0.6.35
	python2.7 setup.py install
	easy_install-2.7 pip
	pip-2.7 install --upgrade pip

	## Virtualenv et création de l'environnement dans /store/python-env
	pip-2.7 install virtualenv
	virtualenv-2.7 /store/python-env --distribute
	
	## Virtualenvwrapper
	yum install python-virtualenv.noarch
	yum install python-virtualenvwrapper.noarch
	pip-2.7 install virtualenvwrapper

Configure your batch profile:
    
    cd ~
    vi .bash_profile

Add these lines to the .profile file in your home directory:

    # Python Virtual Env
    export WORKON_HOME=$HOME/.virtualenvs
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

	
	vi .bashrc
	export VIRTUALENVWRAPPER_LOG_DIR="$WORKON_HOME"
	export VIRTUALENVWRAPPER_HOOK_DIR="$WORKON_HOME"

## 2. Intall BibLib and common dependencies

### 2.1. Configue VirtualEnv

Create the .virtualenv folder:

    cd ~
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

### 2.2. Create the BIBLIB virtualenv

#### To create the BIBLIB virtualenv

    virtualenv BIBLIB

or

    v.mk BIBLIB

#### To activate the BIBLIB virtualenv

	source ~/BIBLIB/bin/activate

or

	v BIBLIB

#### To deactivate the BIBLIB virtualenv
    
    deactivate

or

	v.deactivate

### 2.3. Install BibLib

Create the BibLib HOME Folder where you want :

    cd /var/opt/
    sudo mkdir biblib
    sudo chown ??? biblib
    sudo chgrp ??? biblib

Clone the git repository:

    cd /var/opt/biblib
    git clone git@github.com:medialab/reference_manager.git
    # or
    git clone https://github.com/medialab/reference_manager.git

or update it:

    git reset --hard HEAD
    git pull

Install the working txjsonrpc for JSON-RPC 2.0:

    v BIBLIB
    cd /var/opt/biblib
    git clone git@github.com:asl2/PyZ3950.git
    # or
    git clone https://github.com/asl2/PyZ3950.git
    cd PyZ3950
    python setup.py install

Install the last version of PyZ3950, not the pip one:

    v BIBLIB
    cd /var/opt/biblib
    git clone git@github.com:hefee/txjsonrpc.git
    # or
    git clone https://github.com/hefee/txjsonrpc.git
    cd txjsonrpc
    python setup.py install

Install BibLib required modules:

    v BIBLIB
    cd /var/opt/biblib/reference_manager
    pip install -r requirements.txt

Add BibLib paths to virtualenv

    v BIBLIB
    cd /var/opt/biblib/reference_manager
    add2virtualenv .
    cd biblib
    add2virtualenv .

## 3. Configure
    
### 3.1. Edit config.json

    cd /var/opt/biblib/reference_manager
    cd conf
    cp config.template.json config.json
    vi config.json

#### Configure mongodb server

    "mongodb": {
        "db": "biblib",
        "host": "localhost",
        "port": 27017,
        "default_corpus": "aime"
    }

#### Configure JSON-RPC port

	"jsonrpc": {
        "port": 8080
    }

#### Configure external services
	
    Don't use it for the moment. Will be replace by the targets notion in version 0.6...
	
## 4. Launch and test BibLib

### 4.1. Terminal 1

#### Start the mongodb server

	mongod --dbpath $HOME/somewhere/mongodb

### 4.2. Terminal 2

#### Clean corpus
Be careful! Create the mongodb database of the specified corpus if not already existing, erase all data and create the indexes inside this corpus database.

    cd /var/opt/biblib/reference_manager
    v BIBLIB
    python biblib clean -c aime

#### Conf corpus
Insert or update in the corpus the types and user interface fields located in the "conf" folder
    cd /var/opt/biblib/reference_manager
    v BIBLIB
    python biblib conf -c aime

#### Import metadata in the corpus
Import a metadata file

    cd /var/opt/biblib/reference_manager
    v BIBLIB
    python biblib import -c aime -f endnotexml -i data/endnotexml/endnote-aime.xml

#### Export metadata
Export as a metadata file

    cd /var/opt/biblib/reference_manager
    v BIBLIB
    python biblib export -c aime -f metajson -o data/result/result_aime_metajson.json
    python biblib export -c aime -f html -o data/result/result_aime_html.html
    
#### Convert metadata
Convert a metadata file to another format

    cd /var/opt/biblib/reference_manager
    v BIBLIB
    python biblib convert -f endnotexml -i data/endnotexml/endnote-aime.xml -r metajson -o data/result/result_aime_metajson.json
    python biblib convert -f endnotexml -i data/endnotexml/endnote-aime.xml -r html -o data/result/result_aime_html.html

### 4.3. Terminal 3

#### Start the JSON-RPC server
To start the JSON-RPC server using the bash script:

    cd /var/opt/biblib/reference_manager
    ./start_jsonrpc.sh BIBLIB

To start an restart the JSON-RPC server manually:

    cd /var/opt/biblib/reference_manager
    v BIBLIB
    ps -U ???
    kill ???
    twistd -noy biblib/services/jsonrpc_service.tac -l server.log &
    # or
    twistd -noy biblib/services/jsonrpc_service.tac -l -


### 4.4. Terminal 4

#### Start the BibLib Front web server

BibLib Front (blf) is a javascript program that can be embedded in any HTML page.

A customizable web page is located in:

	cd /var/opt/biblib/reference_manager
	less biblib/front/index.html

You can use the simple python HTTP server or any other to serve this web page:

	cd /var/opt/biblib/reference_manager
	cd biblib/front
	python -m SimpleHTTPServer 8090

### 4.5 Test in a web browser

#### Test with the very simple HTML web page
Modify this HTML web page to test the JSON-RPC server:
    
    cd /var/opt/biblib/reference_manager
    cd test
    vi test_jsonrpc.html
    
Modify the endPoint:
    
    endPoint : 'http://localhost:8080',
    
Try this test web page in your browser:

	file:///var/opt/biblib/reference_manager/test/test_jsonrpc.html

#### Start using BibLib Front

In your web browser try this URL (see 4.4):
	
    http://localhost:8090

