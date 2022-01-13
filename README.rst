Lamia
=====================================

.. contents::

Nmap vs Lamia Network Scanner
-----------------------------
Lamia single target scanner (one of network scanners built in lamia) is almost x3 faster than nmap while scanning 9999 ports for chosen victim.

.. image:: https://user-images.githubusercontent.com/57534862/137483059-b5daff55-1e6f-4186-ac8c-8138e17abcc0.png
   :alt: Built in Lamia Network Scanner vs Nmap performance chart

You want proof? Here you are

.. image:: https://user-images.githubusercontent.com/57534862/137483077-f6c855f7-ec8a-427f-8e59-c12ef66515f5.PNG
   :alt: Network Scanner proof
   
NMAP **496** seconds, Lamia Single Target Module **172** seconds.

General info
-----------------------------
All included  modules in Lamia I created from scratch. Lamia contains the following modules:

- Network Scanners
    - Quick
    - Intense
    - Single target (x3 times faster than nmap!)
- Remote Control
    - SSH
    - Annake (allows you to create reverse_tcp connection between two hosts)
- KeyHook (simple key logger created by me from scratch)

Technologies
------------
* Python 3.6+

Setup
------
In Lamia use only keyboard to navigate throughout modules :exclamation:
If you let, Lamia will **install** all required packages **automatically**.

.. code-block:: python
    On Windows:
    python run_lamia.py
    On Linux:
    python3 run_lamia.py
 
More detailed information about modules
---------------------------------------

Network scanner modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Quick
    This module scans the selected subnet very quickly in search of active devices, module acquires IP addresses of scanned devices
    
- Intense
    With this module, you can scan the selected network, if the module encounters an active victim, it collects information about this victim, here is the list of informations what module will try to get:
        - IP address
        - MAC address
        - Host name
        - Operating system name
        - Ports numbers that are open and services names running on these ports
        
- Single target
    This module quickly gathering information about one selected victim. If victim is active module will get below informations about this victim:
        - IP address
        - MAC address
        - Host name
        - Operating system name
        - Ports numbers that are open and services names running on these ports

Remote control modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^

- SSH module
    Allows user to connect to a remote ssh server.

- ANANKE
    Allows  user to create a reverse_tcp connection between two selected computers in the same network. Once connected, user can execute commands on the second computer via         the network.

Key-hook(Keyloger)
^^^^^^^^^^^^^^^^^^^^^^^^^^^
This is key-logger script. If this key-logger will be on victim pc it will start automatically each time victim turn on computer. After collecting data from keyboard, key-        hook automatically will sent collected data to chosen email.

Application view
---------------------------------------

.. image:: https://user-images.githubusercontent.com/57534862/110455849-2efc4a80-80c9-11eb-9e01-eea37547b035.png
   :alt: Network Scanner view
