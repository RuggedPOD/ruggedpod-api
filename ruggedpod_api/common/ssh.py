import paramiko

from StringIO import StringIO


def execute(command, hostname, username, priv_key):

    print("Execute command \"%s\" on host \"%s@%s\"" % (command, username, hostname))

    k = paramiko.RSAKey.from_private_key(StringIO(priv_key))

    c = paramiko.SSHClient()

    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    c.connect(hostname=hostname, username=username, pkey=k)

    stdin, stdout, stderr = c.exec_command(command)

    stdout_str = stdout.read()
    stderr_str = stderr.read()

    c.close()

    return (0, stdout_str, stderr_str)
