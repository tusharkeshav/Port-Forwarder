import psutil
from properties import ApplicationProperties
from process.RunCommand import RunCommand
from log.Logging import log


class Process:
    """
    Functionality: \n
    1. Check if specified process even exist/running in system \n
    2. Can start specified process
    3. Can kill specified process
    """

    def __init__(self):
        self.protocol = ApplicationProperties.PORT()[0]  # protocol
        self.port = ApplicationProperties.PORT()[1]  # port = 22
        self.path = ApplicationProperties.BINARY_PATH()

    def check(self):

        pid = 0
        status = -1
        for process in psutil.process_iter():
            if process.name() == 'ngrok':
                pid = process.pid
                cmd = "ps aux | grep '[n]grok {} {}'"
                status, output = RunCommand.execute(self, cmd=cmd, protocol=self.protocol, port=self.port)
                log.info('Process exist. List of process: {}'.format(output))
                return (status, output)
        else:
            log.debug('No process found by psutil module.')
            return -1, None

    def get_pid(self, cmd):
        status, output = RunCommand.executeWithOutput(self, cmd)
        if status != 0:
            return -1  # No process found
        else:
            return output

    def start(self):
        status, output = self.check()
        if status == 0:  # success
            self.kill()
        elif status != 0:
            cmd = 'setsid {} {} {}'.format(self.path, self.protocol, self.port)
            log.info('Executing command: ' + cmd)
            RunCommand.executeWithoutOutput(self, cmd)
        pass

    def kill(self):

        # TODO: Note: We are extracting all the process that are associated with keyword Ngrok. TODO: But as process
        #  spawn by setsid, we see that 2 process are running one is setsid(parent) and other is ngrok(child) one So,
        #  for now we consider that new process spawn up always have PID greater than the parent. But it might not be
        #  the case always. Need to look more
        cmd_check_pid = "ps aux | grep '[n]grok {} {}'".format(self.protocol,
                                                               self.port) + " | awk -F: '{ split($0,a,\" \"); print a[2] }' | tail -1"
        PID = self.get_pid(cmd_check_pid)
        if PID == -1:
            print('No such process exist or Process is already killed.')
            return
        log.info('Running Process PID: {}'.format(PID))
        cmd_kill = 'kill -9 {}'.format(PID)
        status, output = RunCommand.executeWithOutput(self, cmd_kill)

        # TODO: Recheck if ngrok session killed or not

        if status == 0:
            log.info('Successfully killed the process.')
            return status, output
        pass

# t = Process()
# # status, output = t.check()
# # print(status, output)
# print(t.kill())
# print(t.start())