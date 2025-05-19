# CORVOS
A Discord bot for quoting and speaking to users using user submitted content
CorvOS is a Discord bot born out of a desire to store interesting quotes and have them posted back whenever you want. Save memories without needing to screenshot your favorite moments from chat. CorvOS attempts to recreate the feel of sites like bash.org, storing line by line messages and recovering them in an embedded message window that displays whatever you want. 
Want CorvOS to speak to chat? It can do that too! By storing various one liner quotes, you can have CorvOS speak it back to chat. Each set of quotes and one liners is restricted to each individual guild.

# REQUIREMENTS
Requires Python 3 and sqlite3. See below for pip packages to install.
Package           Version
----------------- -------
aiohappyeyeballs  2.6.1
aiohttp           3.11.16
aiosignal         1.3.2
attrs             25.3.0
DateTime          5.5
discord.py        2.5.2
dotenv            0.9.9
frozenlist        1.6.0
greenlet          3.2.0
idna              3.10
multidict         6.4.3
pip               24.0
propcache         0.3.1
python-dotenv     1.1.0
pytz              2025.2
setuptools        78.1.0
SQLAlchemy        2.0.40
typing_extensions 4.13.2
yarl              1.20.0
zope.interface    7.2


# Commands
$ping --> checks if the bot is online. 
$quote [x] --> specify a number of messages to get and store - this will store x messages up from the calling message. EX: 3 messages are posted back to back that you want to quote. use $quote 3 and the messages above you will be stored and displayed in a single embed
$recall --> recalls a message for display in an embedded format - any quote you've saved using $quote will be stored in this format. 
$store [message] --> store a single message for the bot to repeat. EX: $store "this message here" will store the message for recall later
$speak --> repeats a stored message that was saved using $store
