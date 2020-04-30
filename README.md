# About

### To use:

1. Ensure python is installed on your system

2. run "python server.py 1234" (or any other port number) File located [here](/receiver)

3. run "python client.py localhost 1234" (matching the server port number) File located [here](/sender)


### Commands:

##### put <filename> : Sends file from client to server

##### get <filename> : Sends file from server to client

##### ls : Returns files within server

##### quit : Exits program


### Note:

You may want to remove "message.txt" from [reciever](/receiver) and "s_mess.txt"
from [sender](/sender) to be able to text both put and get commands. 
