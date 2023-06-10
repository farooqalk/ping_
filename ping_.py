from distutils import command
from itertools import count
from matplotlib.pyplot import sca
from pythonping import ping
import netifaces
import socket
from getmac import get_mac_address
import requests
from mac_vendor_lookup import MacLookup
import os
from os import system, name
import colorama
from colorama import Fore
from colorama import Style
import threading

class ping_:
    def __init__(self) -> None:
        self.devices = {}
        self.IPsFound = []
        self.macsFound = []
        self.vendorsFound = []
        pass

    def getVendor(self, mac_address:str) -> str:
        """Gets the vendor of a device using MAC address

        Args:
            mac_address (str): mac address of a device

        Returns:
            str: vendorName: Any | Literal['N/A']
        """
        vendorName = ""

        try:
            vendorName = MacLookup().lookup(mac_address.upper())
        except:
            vendorName = "N/A"

        return vendorName

    def outputRes(self):
        """Outputs results of script
        """
        for l in range(len(self.IPsFound)):
            print(
                f'''|{l}| IP> {self.IPsFound[l]} || MAC> {self.macsFound[l]} || Vendor> {self.vendorsFound[l]}'''
            )


    
    def outputIndex(self, index):
        """Return information of client at the requested index

        Args:
            index (int): index of element to be printed
        """
        print(
            f"|{index}| IP> {self.IPsFound[index]} || MAC> {self.macsFound[index]} || Vendor> {self.vendorsFound[index]}")


    
    def printHelpMenu(self, menu):
        """Print the help menu using the dictionary supplied as an arg

        Args:
            menu (list): key-value pair
        """
        for key, value in menu.items():
            print(key, value)

    def pingIP(self, IPadd:str, length:float):
        """Used to ping a certain ping

        Args:
            IPadd (str): IP address to be ping'ed
            length (float): Timeout after
        """
        result:bool = ping(f'{IPadd}', count=1, size=1, timeout=length)
        if result.success() == True:
            self.IPsFound.append(IPadd)

    def generateMACs(self):
        """Loops through each IP and gets its MAC address
        """
        # Get macs for each IP found
        for h in range(len(self.IPsFound)):
            # Get MAC address and save it to variable
            macAddr = get_mac_address(ip=(self.IPsFound[h]))
            # Append IP to array
            self.macsFound.append(macAddr)
            h += 1

    def generateVendors(self):
        """Loops through each IP, uses MAC address to find the device vendor
        """
        # Get vendor for each MAC found
        for p in range(len(self.IPsFound)):
            # Get vendor using the MAC addresses in the macsFound array
            vendor = self.getVendor(self.macsFound[p])
            # Vendor to vendorsFound array
            self.vendorsFound.append(vendor)
            p += 1
            
    def prompt(self):
        userInput = ""
        helpMenu = {
            'print': "| Output the results table",
            'ping ': "| usage: ping 0-255 [REPLACE IP INDEX]",
            'ip   ': "| Pick a certain index to print all info about a certain IP adddress",
            'clear': "| Clears terminal window",
            'save ': "| Saves results to log.txt",
            'help ': "| Prints this help menu",
            'exit ': "| Quits program",
        }

        commands = ['exit', 'print', 'ip', 'help', 'clear', 'save', 'ping']

        # TODO: Add error handling
        while True:

            userInput = input('# ').lower()

            # Exit
            if(userInput == commands[0]):
                print("Bye :D")
                break

            # Output results table
            elif(userInput == commands[1]):
                self.outputRes()

            # Get info of a certain index
            elif userInput == commands[2]:
                while True:
                    try:
                        userInput = int(input('Index: '))
                        self.outputIndex(userInput)
                        break

                    except:
                        print("Something Went Wrong :/")

            # Help menu
            elif(userInput == commands[3]):
                self.printHelpMenu(helpMenu)

            elif(userInput == commands[4]):
                # for windows
                if name == 'nt':
                    system('cls')

                # for mac and linux(here, os.name is 'posix')
                else:
                    system('clear')

            elif(userInput == commands[5]):
                try:
                    fileName = ""
                    while fileName == "" or fileName == " " or "\n":
                        fileName = input('Filename: ')
                        #print(f"Filename: {fileName}")
                        if "." not in fileName and not fileName == "" or not fileName == " ":
                            fileName += ".txt"
                            break

                    f = open(fileName, "w")
                    
                    for l in range(len(self.IPsFound)):
                        f.write(
                            f'''|{l}| IP> {self.IPsFound[l]} || MAC> {self.macsFound[l]} || Vendor> {self.vendorsFound[l]}\n'''
                        )
                    f.close()
                except:
                    print(Fore.RED + "An error occured while saving" + Style.RESET_ALL)
            
            elif(commands[6] in userInput):

                try:
                    newString = userInput.replace("ping", "")
                    newString = newString.replace(" ", "")
                    indexFound = int(newString)
                    system(f"ping {self.IPsFound[indexFound]}")

                except:
                    print(Fore.RED + 'Invalid Usage. Enter "help" to see usage.' + Style.RESET_ALL)

        # Invalid Commands
            elif(userInput not in commands):
                print(
                    Fore.RED + f'"{userInput}" is not a valid command!' + Style.RESET_ALL)

    def scan(self, length:float):
        """Scans the active network

        Args:
            length (float): Timeout
        """

        gateways = netifaces.gateways()
        default_gateway = gateways['default'][netifaces.AF_INET][0]
        print(f"Default Gateway: {default_gateway}")
        matches, j, matchIndex = 0, 0, 0

        defGatewayNoLastDigits = ""
        defGatewayNoLastDigitsString = ""


        defList = list(default_gateway)


        for i in range(len(default_gateway)):
            if (default_gateway[i] == "."):
                matches += 1
                if(matches >= 3):
                    matchIndex = i
                    while(j <= i):
                        defList[j] = ""
                        j += 1
            i += 1

        # Break down the default gateway to get rid of the last digit(s)
        for k in range(len(default_gateway)):

            defGatewayNoLastDigits += default_gateway[k]
            if(k >= matchIndex):
                break
        defGatewayNoLastDigitsString = "".join(defGatewayNoLastDigits)

        i = 1
        # Check for all IPs in the known range
        while (i <= 255):
            # Check if the IP exists
            #print(f"Scanning: {defGatewayNoLastDigitsString+str(i)}")
            thread1 = threading.Thread(target=self.pingIP, args=((str(defGatewayNoLastDigitsString) + str(i)), length))
            thread1.start()
            i += 1
            # Fixes index out of bounds by waiting for the last ping to finish
            if(i==255):
                thread1.join()
