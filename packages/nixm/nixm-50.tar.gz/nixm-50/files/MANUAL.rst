**NAME**


``nixm`` - NIXM


**SYNOPSIS**

|
| ``nixm <cmd> [key=val] [key==val]``
| ``nixmd`` 
| ``nixms``
|

**DESCRIPTION**


NIXM contains all the python3 code to program objects in a functional
way. It provides a base Object class that has only dunder methods, all
methods are factored out into functions with the objects as the first
argument. It is called Object Programming (OP), OOP without the
oriented.

NIXM allows for easy json save//load to/from disk of objects. It
provides an "clean namespace" Object class that only has dunder
methods, so the namespace is not cluttered with method names. This
makes storing and reading to/from json possible.

NIXM has all you need to program a unix cli program, such as disk
perisistence for configuration files, event handler to handle the
client/server connection, deferred exception handling to not crash
on an error, etc.

NIXM is Public Domain.

1. You need to set PYTHONPATH="." if you run this locally.
2. You might need to uninstall and rm -fR ~/.cache/pip in case of error.


**INSTALL**

installation is done with pipx

|
| ``$ pipx install nixm``
| ``$ pipx ensurepath``
|
| <new terminal>
|
| ``$ nixm srv > nixm.service``
| ``$ sudo mv nixm.service /etc/systemd/system/``
| ``$ sudo systemctl enable nixm --now``
|
| joins ``#nixm`` on localhost
|

**USAGE**

use ``nixm`` to control the program, default it does nothing

|
| ``$ nixm``
| ``$``
|

see list of commands

|
| ``$ nixm cmd``
| ``cfg,cmd,dne,dpl,err,exp,imp,log,mod,mre,nme,``
| ``now,pwd,rem,req,res,rss,srv,syn,tdo,thr,upt``
|

start daemon

|
| ``$ nixmd``
| ``$``
|

start service

|
| ``$ nixms``
| ``<runs until ctrl-c>``
|

show request to the prosecutor

|
| $ ``nixm req``
| Information and Evidence Unit
| Office of the Prosecutor
| Post Office Box 19519
| 2500 CM The Hague
| The Netherlands
|

**COMMANDS**

here is a list of available commands

|
| ``cfg`` - irc configuration
| ``cmd`` - commands
| ``dpl`` - sets display items
| ``err`` - show errors
| ``exp`` - export opml (stdout)
| ``imp`` - import opml
| ``log`` - log text
| ``mre`` - display cached output
| ``now`` - show genocide stats
| ``pwd`` - sasl nickserv name/pass
| ``rem`` - removes a rss feed
| ``res`` - restore deleted feeds
| ``req`` - reconsider
| ``rss`` - add a feed
| ``syn`` - sync rss feeds
| ``tdo`` - add todo item
| ``thr`` - show running threads
| ``upt`` - show uptime
|

**CONFIGURATION**

irc

|
| ``$ nixm cfg server=<server>``
| ``$ nixm cfg channel=<channel>``
| ``$ nixm cfg nick=<nick>``
|

sasl

|
| ``$ nixm pwd <nsvnick> <nspass>``
| ``$ nixm cfg password=<frompwd>``
|

rss

|
| ``$ nixm rss <url>``
| ``$ nixm dpl <url> <item1,item2>``
| ``$ nixm rem <url>``
| ``$ nixm nme <url> <name>``
|

opml

|
| ``$ nixm exp``
| ``$ nixm imp <filename>``
|

**SOURCE**

source is at `https://github.com/otpcr/nixm  <https://github.com/otpcr/nixm>`_


**FILES**

|
| ``~/.nixm``
| ``~/.local/bin/nixm``
| ``~/.local/bin/nixmd``
| ``~/.local/bin/nixms``
| ``~/.local/pipx/venvs/nixm/*``
|

**AUTHOR**

|
| Bart Thate <``bthate@dds.nl``>
|

**COPYRIGHT**

|
| ``NIXM`` is Public Domain.
|