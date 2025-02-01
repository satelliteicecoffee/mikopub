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

*switchRemote()* and *terminateInstr()* are necessary functions to have. *Task* context manager rely on them to start and clean the instuments.\
It's OK to leave empty if instuments are safe without on/off or remote operations.
```python
def switchRemote(self, toStatus: Literal["on", "off"]) -> None:
    # switching codes for the instruemnt
```
```python
def terminateInstr(self) -> None:
    # termination codes for the instrument
```
