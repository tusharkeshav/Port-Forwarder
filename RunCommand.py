from subprocess import getstatusoutput, Popen
from Logging import log
from configparser import ConfigParser


# TODO: Refactoring
class RunCommand:
    """
    TODO: Need Refactoring
    Functionality: \n
    1. Can run specified command giving no output. \n
    2. Can run specified command and result of command as output.
    """

    def executeWithoutOutput(self, cmd: str) -> bool:
        log.info("Executing command with Popen: " + cmd)
        # os.system(cmd)
        proc = Popen([cmd], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        log.info('Command submitted')
        return True

    def execute(self, cmd: str, protocol: str, port: int) -> str:
        cmd = cmd.format(protocol, port)
        print('Executing command: ' + cmd)
        status, output = getstatusoutput(cmd)
        if status != 0:
            # return 0, {'message': "There's no such {} process".format(cmd)}
            return 0, "No such process found"
        return status, output
        pass

    def executeWithOutput(self, cmd):
        print('Executing command: ' + cmd)
        status, output = getstatusoutput(cmd)
        return status, output

    def execute_and_return_pid(self, cmd):
        print('Executing command: ' + cmd)
        process = Popen([cmd], shell=False, stdin=None, stdout=None, stderr=None, close_fds=True)
        pid = process.pid
        self.write_pid(pid)
        return pid

    def write_pid(self, pid):
        config = ConfigParser()
        config.read('app.pid')
        config.set('pid', 'SSH', str(pid))
        with open('app.pid', 'w') as data:
            config.write(data)
            log.info('Successfully written PID')

    def read_pid(self):
        config = ConfigParser()
        config.read('app.pid')
        return config['pid']['SSH']

# res = RunCommand()
# print(res.read_pid())
# res.write_pid(433)
# print(res.read_pid())
