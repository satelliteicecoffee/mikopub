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

Based mainly on PyVISA.

# Usage
A test case is treated as one (or more) *Task*, and a *Task* takes over the followng things:
* Instrument initialization at setup
* Instrument termination at cleanup or error
* Log management for all instruments and the *Task* itself
* Parameter preparations, e.g. loading data, pre-calculations, conditional operations, if any

The *Task* can be used either directly or as a test case template.

**Directly:**

Import necessary modules

```python
import mikopub
import mikopub.instrument.example_instrument
```

Create the *Task* instance.
```python
task_1 = mikopub.Task()
```

Create and configure the *log* logger if you want recorded automatic recorded logs.
```python
log_path = os.path.join(os.path.dirname(__file__), 'example_task.log')
task_1.setloglogger(log_path)
```

Create and configure the *csv* logger for selective data log in csv format.
```python
csv_path = os.path.join(os.path.dirname(__file__), 'example_task.csv')
task_1.setcsvlogger(csv_path)
```

Create the *instrument* instance and don't forget to add it to the *Task*.
```python
instrument_1 = mikopub.instrument.example_instrument.example_instrument()
task_1.addInstr(instrument_1)
```

Connect the *instrument* before the task.\
Run all instrument and logger operations in the *Task* context.
```python
instrument_1.connectUDP(udpIP="192.168.10.11", udpPort=8000)
with task_1 as t:
    inpu_int = 10

    # instrument operation with auto log recording
    result_1 = instrument_1.exampleFunc1(x=inpu_int)
    instrument_1.exampleFunc2()

    # load any paramters in this format
    t.var["log-1"] = inpu_int
    t.var["log-2"] = result_1

    # this function writes the above loaded data to csv log
    # a title row is generated the first time logVar is called
    t.logVar()
```

Your data and operation logs should appear now in the *Task* script folder.


# Instrument extension

See *mikopub.instument.example_instrument* for full code.\

**Key points:**

Use super() to inherit base functions from *_visa_instrument*.
```python
class example_instrument(_visa_instrument):
    def __init__(self):
        super(example_instrument, self).__init__()
```

*switchRemote()*, *terminateErrorInstr()* and *terminateInstr()* are necessary functions to have for any instrument.\
*Task* context manager calls them automatically at start and cleanup or when error occurs.
* *switchRemote(toStatus="on")* is called when the *Task* context starts
* *terminateErrorInstr()* is called when error occurs during the *Task* context.
* *terminateInstr()* is called whtn *Task* finishes without abnormality

It's OK to leave empty if instuments are safe without on/off or remote operations.
```python
# switching codes for the instruemnt
def switchRemote(self, toStatus: Literal["on", "off"]) -> None:
```
```python
# terminating codes for the instrument when error happens
# e.g. cut off power output or open relay
def terminateErrorInstr(self):
    self.switchRemote(toStatus="off")
```
```python
# terminating codes for the instrument when task finish normally
def terminateInstr(self) -> None:
    self.switchRemote(toStatus="off")
```

Connect to and command the instrument using APIs in *_visa_instrument* base class.\

Connnection examples:
```python
# create instrument instance and connect to serial port 8, baudrate 38400
e_instr = example_instrument()
e_instr.connectSerial(comPort=8, baudrate=38400)
```
```python
# serial port on linux
e_instr.connectSerial(comPort="/dev/ttyS", baudrate=38400)
```
```python
# UDP interface
e_instr = connectUDP(udpIP="192.168.20.25", udpPort=2025)
```

IO examples:
```python
# Query ID of the instrument and print
instrument_id = self.query("*IDN?")
print(instrument_id)
```
```python
# Query ID of the instrument and print
byte_return = self.queryBytes(b"\x02\x200\x03")
print(byte_return)
```
