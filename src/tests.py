import optparse
import sys
import time

from hiredict.context import HiRedictContext, HiRedictReply


if __name__ == "__main__":
    option_parser = optparse.OptionParser()
    
    option_parser.add_option("--hostname", dest="hostname", type="string", default="0.0.0.0")
    option_parser.add_option("--port", dest="port", type="int", default=6379)

    options, _ = option_parser.parse_args()

    time.sleep(2)

    c = HiRedictContext(options.hostname, options.port, 1.0)

    if not c.isRunning():
        print("Error during hiredict connection to redict-db")
        sys.exit(1)
    
    reply = c.sendCommand("PING")

    if reply is None:
        print("Error during PING command")
        sys.exit(1)
    
    print(f"PING: {reply.str()}")

    reply = c.sendCommand(f"SET foo hello world")

    if reply is None:
        print("Error during SET command")
        sys.exit(1)

    print(f"SET: {reply.str()}")