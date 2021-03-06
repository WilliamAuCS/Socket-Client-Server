# About

#### Created by:
William Au - WilliamAu@csu.fullerton.edu  
Swagat Buha - buha3210@csuf.fullerton.edu  
Yanjie Shi - yanjieshi@csu.fullerton.edu  
Daniel Pestolesi - danpestolesi@csu.fullerton.edu  

### To use:

1. Ensure python is installed on your system

2. run
```sh
python serv.py 1234
```
(or another unused port number) File located [here](/receiver)

3. run
```sh
python cli.py localhost 1234
```
(matching the server port number) File located [here](/sender)


### Commands:

**put <filename>** : Sends file from client to server

**get <filename> :** Sends file from server to client

**ls :** Returns files within server

**quit :** Exits program


### Note:

You may want to remove "message.txt" from [reciever](/receiver) and "s_mess.txt"
from [sender](/sender) to be able to text both put and get commands.

For additional information on client/server arguments, type:  
```sh
python cli.py -h
```
or  
```sh
python serv.py -h
```
