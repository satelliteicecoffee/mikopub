'''
mikopub.utils.task
Task and task template for test taskflows
'''
import os

import mikopub
import mikopub.instrument.example_instrument

task_1 = mikopub.Task()

log_path = os.path.join(os.path.dirname(__file__), 'example_task.log')
csv_path = os.path.join(os.path.dirname(__file__), 'example_task.csv')

task_1.setloglogger(log_path)
task_1.setcsvlogger(csv_path)

instrument_1 = mikopub.instrument.example_instrument.example_instrument()

task_1.addInstr(instrument_1)

instrument_1.connectUDP(udpIP="192.168.10.11", udpPort=8000)
with task_1 as t:
    inpu_int = 10
    result_1 = instrument_1.exampleFunc1(x=inpu_int)
    instrument_1.exampleFunc2()

    t.var["log-1"] = inpu_int
    t.var["log-2"] = result_1
    t.logVar()
    pass

pass
