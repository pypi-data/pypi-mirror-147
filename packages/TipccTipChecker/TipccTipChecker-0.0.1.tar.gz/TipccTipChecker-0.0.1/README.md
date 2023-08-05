How to use?
Import the package

from TipccTipChecker import checktip

Create a json file to send data to
Ex: tipdata.json

Get the discord message content (normally with message.content or msg.content)
tip = message.content

Get the user who sent the message (normally with message.author.id or msg.author.id)
tipauthor = message.author.id

Get the location of the json file to send data to
filelocation = ('json/file/location.json')

Send the message to the tip checker
tipchecker.checktip(tip, tipauthor, filelocation)

The tip checker will reply with the tip's data