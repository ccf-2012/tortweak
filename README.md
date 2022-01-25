# tortweak 

Hardlink tweaks of file/folder to get more crossed.

## Require
* transmission
* python3 and pip3


## Install dependencies
```sh
pip3 install -r requirements.txt
```
or:
```sh
pip install qbittorrent-api
pip install transmission-rpc
pip install deluge_client

pip install pytz
```

* Tip: install pip3 in Synology
```sh
# install python in DSM
sudo python3 -m ensurepip
```

* Tip: install python3 / pip3 in QNAP
```sh
opkg install python3-pip
```

## Usage
```sh
python tortweak.py -h 
```

```
usage: tortweak.py [-h] -s HOST -p PORT -u USERNAME -w PASSWORD -d DOCKER_DIR
                   -r REAL_DIR

Hardlink tweaks of file/folder to get more crossed.

options:
  -h, --help            show this help message and exit
  -s HOST, --host HOST  host of transmission
  -p PORT, --port PORT  port of transmission
  -u USERNAME, --username USERNAME
                        username of transmission
  -w PASSWORD, --password PASSWORD
                        password of transmission
  -d DOCKER_DIR, --docker_dir DOCKER_DIR
                        root dir in docker
  -r REAL_DIR, --real_dir REAL_DIR
                        real dir path
```                        


## Example
```sh 
python tortweak.py -s 192.168.5.8 -p 8091 -u transmission -w password -d /downloads -r /share/CACHEDEV1_DATA/Video/QB
```

