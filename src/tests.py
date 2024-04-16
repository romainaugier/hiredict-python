import optparse
import sys
import time
import socket

from hiredict.context import HiRedictContext, HiRedictReply


if __name__ == "__main__":
    option_parser = optparse.OptionParser()
    
    option_parser.add_option("--hostname", dest="hostname", type="string", default="localhost")
    option_parser.add_option("--port", dest="port", type="int", default=6379)
    options, _ = option_parser.parse_args()

    c = HiRedictContext(options.hostname, options.port, 1.0)

    if not c.isRunning():
        print("Error during hiredict connection to redict-db")
        sys.exit(1)
    
    reply = c.sendCommand("PING")

    if not reply.Pong():
        print("Error during PING command")
        sys.exit(1)
    
    print(f"PING: {reply.asString()}")

    reply = c.sendCommand(f"SET foo \"hello world\"")

    if reply.Error():
        print("Error during SET command")
        print(f"Error: {reply.ErrorMessage()}")
        sys.exit(1)

    print(f"SET: {reply.asString()}")

    reply = c.sendCommand(f"GET foo")
    
    if reply.Error():
        print("Error during GET command")
        print(f"Error: {reply.ErrorMessage()}")
        sys.exit(1)

    print(f"GET: {reply.asString()}")

    reply = c.sendCommand(f"SET int_var 18")

    if reply.Error():
        print("Error during GET command")
        print(f"Error: {reply.ErrorMessage()}")
        sys.exit(1)

    print(f"SET: {reply.asString()}")

    reply = c.sendCommand(f"GET int_var")

    print(f"GET: {reply.asInteger()}")