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
* Serial
* USB
* TCP/IP
* UDP (*socket* backend)


# Usage
A test case is treated as one (or more) *Task*, and a *Task* takes over the followng things:
* Instrument initialization at setup
* Instrument termination at cleanup or error
* Log management for all instruments and the *Task* itself
* Parameter preparations, e.g. loading data, pre-calculations, conditional operations, if any

The *Task* can be used either directly or case template.

**Directly:**


TBD..


# Instrument extension
TBD..
