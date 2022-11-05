import psutil
from Ports import Ports
from RunCommand import RunCommand
from Logging import log


class Process:
    def __init__(self):
        self.protocol = Ports.SSH.value[0]  # protocol = SSH
        self.port = Ports.SSH.value[1]  # port = 22

    def check(self):

        pid = 0
        status = -1
        for process in psutil.process_iter():
            if process.name() == 'ngrok':
                pid = process.pid
                cmd = "ps aux | grep '[n]grok {} {}'"
                status, output = RunCommand.execute(self, cmd=cmd, protocol=self.protocol, port=self.port)
                return (status, output)
        else:
            return -1, None

    def get_pid(self, cmd):
        status, output = RunCommand.executeWithOutput(self, cmd)
        if status != 0:
            return -1   # No process found
        else:
            return output

    def start(self):
        status, output = self.check()
        if status == 0:  # success
            self.kill()
        elif status != 0:
            cmd = 'setsid /home/akhil/Documents/ngrok-2.2.2-linux-amd64/ngrok {} {}'.format(self.protocol, self.port)
            log.info('Executing command: '+ cmd)
            RunCommand.executeWithoutOutput(self, cmd)
        pass

    def kill(self):
        cmd_check_pid = "ps aux | grep '[n]grok {} {}'".format(self.protocol, self.port) + " | awk -F: '{ split($0,a,\" \"); print a[2] }'"
        PID = self.get_pid(cmd_check_pid)
        if PID == -1:
            print('No such process exist or Process is already killed.')
            return
        print('Running Process PID: ', PID)
        cmd_kill = 'kill -9 {}'.format(PID)
        status, output = RunCommand.executeWithOutput(self, cmd_kill)

        # TODO: Recheck if ngrok session killed or not

        if status == 0:
            print('Process killed')
            return status, output
        pass

# t = Process()
# # status, output = t.check()
# # print(status, output)
# print(t.kill())
# print(t.start())