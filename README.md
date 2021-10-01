# Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [More detailed information about modules](#more-detailed-information-about-modules)
* [Application view](#application-view)
<br>

## General info
<details>
    <summary>Click here to see general information about <b>Lamia</b>!</summary>
        <b>All included  modules in script I created from scratch</b>. The script I created allows you to thoroughly scan the network you are connected to, obtain credentials             using the key-hook module, the intercepted data will be sent to the e-mail address of your choice. The module will also allow you to quickly generate a set of                   passwords which you can use to brute force attacks and allow you to connect to devices outside your network.
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
         python run.py
         On Linux:
         python3 run.py
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
                   <b>Intense</b> --> With this module, we can scan the selected network, if the module encounters an active device in the network, it collects information about                                       this device, here is the list of information what module will try to get about  encountered device:
                 </li>
                 <ul>
                    <li>IP address</li>
                    <li>MAC address</li>
                    <li>Host name</li>
                    <li>Operating system name</li>
                    <li>Open port number</li>
                    <li>The name of the service running on an open port</li>
                </ul>
         </ul>
         <br>
         <ul>
            <li>  
            <b>Single target</b> --> This module quickly gathering information about one selcted device. Below is a list of information that module will try to get about chosen                                       device:
             </li>
                <ul>
                    <li>IP address</li>
                    <li>MAC address</li>
                    <li>Host name</li>
                    <li>Operating system name</li>
                    <li>Open port number</li>
                    <li>The name of the service running on an open port</li>
                </ul>
         </ul>
    </ul>
   <br>
   <b>Remote control modules</b>
      <ul>
        <li><b>SSH module</b> --> Allows user to connect to a remote ssh server.</li>
        <li><b>ANANKE</b> --> Allows the user to create a reverse_tcp connection between two selected computers on the same network. 
                             Once connected, user can execute commands on the second computer via the network.</li>
      </ul>
   <br>
   <b>Key-hook(Keyloger)</b>
       <ul>
         <li>This is key-logger script. If this key-logger will be on victim pc it will start 
automatically each time victim turn on computer. After                      collecting data from keyboard, key-hook automatically will sent collected data to chosen email.</li>
      </<ul>
</details>

<br>

## Application view
![scan](https://user-images.githubusercontent.com/57534862/110455849-2efc4a80-80c9-11eb-9e01-eea37547b035.png)
