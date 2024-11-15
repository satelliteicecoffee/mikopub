# Overview
Miko-series test automation framework.

Public version for general purpose.

**Can do:**
* Automatic instrument control/monitoring
* Instrument interface standardization
* Real-time logging in .csv and/or .log format
* Built-in setup/cleanup and emergency stop mechanisms (proper interface programming required)
* Some colorspace and other calculations

**Supported interfaces:**
* Serial, USB, TCP/IP and UDP

**Note:** UDP is not supported by pyvisa originally. 
This framework offers an alternative interface to communicate with UDP devices with python socket module. 
The behaviour of UDP resources will be the same as other pyvisa-based ones in this framework.


# Description
This framework is a further development from pyvisa and logging modules. 
It offers automatic test task entry-exit handling mechanisms, straightforward logging methods and easy instrument extension templates.

# Usage
In this framework, a test case is treated as one (or more, for complex cases) *Task*. A *Task* takes over the followng things:
* Instrument initialization and termination at setup, cleanup stages or when error happens
* Management of logger interfaces for all instruments and data in one *Task*
* Preparation of test case parameters, e.g. loading parameters, pre-calculations, conditional operations, if any

In real-world scenarios, the execution of test cases usually involves in setting up the environment, preparing and operating the instruments while logging data and final cleanup. This framework handles the process using a similar approach. 

Generally speaking, 


# Instrument extension
TBD..
