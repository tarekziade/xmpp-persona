#!/usr/bin/python
#
# External auth script for ejabberd that enable auth against Persona.
import sys
from struct import unpack, pack, error as struct_error
import browserid


verifier = browserid.LocalVerifier(['*'])


def debug(msg):
    sys.stderr.write(msg + '\n')
    sys.stderr.flush()


def read_stdin():
    """Reads a command sent by ejabberd via stdin
    """
    # get the record size in the first two bytes
    size, = unpack('>h', sys.stdin.read(2))
    # read the record
    return sys.stdin.read(size).split(':')


def return_result(result=True):
    """Return the result of a command
    """
    sys.stdout.write(pack('>hh', 2, result and 1 or 0))
    sys.stdout.flush()


def auth(user, host, password):
    """Authenticates a user.
    """
    if password.startswith('persona:'):
        password = password[len('persona:'):]
    else:
        # just accept any password for other people for now
        return True
    # the password is the assertion
    try:
        verifier.verify(password, '*')
    except ValueError, UnicodeDecodeError:
        return False

    return True


def main():
    debug('Mozilla Persona Authentication Plugin...')
    while True:
        try:
            request = read_stdin()
        except struct_error:
            return_result(False)

        command = request[0]

        if command == 'auth':
            user, host, password = request[1], request[2], request[3]
            return_result(auth(user, auth, password))
        elif command == 'isuser':
            # we'll just always say yes for now.
            return_result()
        else:
            debug('%r not supported' % command)
            return_result(False)



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

    debug('Bye!')
    sys.exit(0)
