# Overview
Miko-series test automation framework.

Public version for general purpose.


# Description
This framework is a further development from pyvisa and logging modules. 
It offers automatic test task entry-exit and error handling mechanisms, 
straightforward logging methods and easy instrument extension templates.

Supported interfaces: Serial, USB, TCP/IP and UDP*.
**Note:** UDP is not supported by pyvisa originally. This framework offers an alternative interface to communicate with UDP devices with python socket module. The behaviour of UDP resources will be the same as other pyvisa-based ones in this framework.
