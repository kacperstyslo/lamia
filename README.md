# Lamia

## Nmap vs Lamia Network Scanner

#### Lamia single target scanner (one of network scanners built in lamia) is almost x3 faster than nmap while scanning 9999 ports for chosen victim.

![bar](https://user-images.githubusercontent.com/57534862/137483059-b5daff55-1e6f-4186-ac8c-8138e17abcc0.png)

### You want proof? Here you are

![proof](https://user-images.githubusercontent.com/57534862/137483077-f6c855f7-ec8a-427f-8e59-c12ef66515f5.PNG)

### NMAP 496 seconds, Lamia Single Target Module 172 seconds.

# Table of contents

* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [More detailed information about modules](#more-detailed-information-about-modules)
* [Application view](#application-view)

## General info

<details>
    <summary>Click here to see general information about <b>Lamia</b>!</summary>
        <b>All included  modules in Lamia I created from scratch</b>. Lamia contains the 
following modules:

- Network Scanners
    - Quick
    - Intense
    - Single target (x3 times faster than nmap!)
- Remote Control
    - SSH
    - Annake (allows you to create reverse_tcp connection between two hosts)
- KeyHook

</details>


<br>

## Technologies

<details>
    <summary>Click here to see the technologies used!</summary>
        <ul>
            <li>Python 3.8.5</li>
        </ul>
</details>

<br>

## Setup

:exclamation: In Lamia use only keyboard to navigate throughout modules :exclamation:<br/>
<details>
    <summary>Click here to see how to run <b>Lamia!</b></summary>
         If you let, Lamia will **install** all required packages <b>automatically</b>.

         On Windows:
         python run_lamia.py
         On Linux:
         python3 run_lamia.py

</details>

<br>

## More detailed information about modules

<details>
   <summary>Click here to more detailed information about modules!</summary>
      <br>
             <b>Network scanner modules</b>
             <br>
             <ul>
                <ul>
                    <li><b>Quick</b> --> This module scans the selected subnet very quickly in search of active devices, module acquires IP addresses of scanned devices)</li>
                 </ul>
            <br>
            <ul>
                <li>
                   <b>Intense</b> --> With this module, you can scan the selected network, if the 
                    module encounters an active victim, it collects information about this victim,
                    here is the list of informations what module will try to get:
                 </li>
                <ul>
                    <li>IP address</li>
                    <li>MAC address</li>
                    <li>Host name</li>
                    <li>Operating system name</li>
                    <li>Ports numbers that are open and services names running on these ports</li>
                </ul>
         </ul>
         <br>
         <ul>
            <li>  
            <b>Single target</b> --> This module quickly gathering information about one 
            selected victim. If victim is active module will get below informations about this 
            victim:
             </li>
                <ul>
                    <li>IP address</li>
                    <li>MAC address</li>
                    <li>Host name</li>
                    <li>Operating system name</li>
                    <li>Ports numbers that are open and services names running on these ports</li>
                </ul>
         </ul>
    </ul>
   <br>
   <b>Remote control modules</b>
      <ul>
        <li><b>SSH module</b> --> Allows user to connect to a remote ssh server.</li>
        <li><b>ANANKE</b> --> Allows  user to create a <b>reverse_tcp</b> connection between two 
                              selected computers in the same network. Once connected, user can 
                              execute commands on the second computer via the network.</li>
      </ul>
   <br>
   <b>Key-hook(Keyloger)</b>
       <ul>
         <li>This is key-logger script. If this key-logger will be on victim pc it will start 
            automatically each time victim turn on computer. After collecting data from keyboard, key-hook automatically will sent collected data to chosen email.</li>
      </ul>
</details>

<br>

## Application view

![scan](https://user-images.githubusercontent.com/57534862/110455849-2efc4a80-80c9-11eb-9e01-eea37547b035.png)
