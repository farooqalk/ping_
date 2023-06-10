from ping_ import ping_
import argparse
import time

start = time.time()
parser = argparse.ArgumentParser()

parser.add_argument('-t', '--time', required=False, help="Timeout for each ping")
parser.parse_args()
args = vars(parser.parse_args())
pingTime = args["time"]

try:
    int(pingTime)
except:
    pingTime = 4
    print(f"Invalid input for ping timeout. Using default value: {pingTime}")
    
ping = ping_()

ping.scan(int(pingTime))

ping.generateMACs()

ping.generateVendors()

ping.outputRes()
print(f"Time taken: {round(time.time()-start)} || Results: {len(ping.IPsFound)}")

ping.prompt()