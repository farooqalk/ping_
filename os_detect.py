import nmap, json

def detect_os(target_ip):
    nm = nmap.PortScanner()
    nm.nmap_path = r'C:\\Program Files (x86)\\Nmap\\nmap.exe'  # Modify this path as per your Nmap installation location
    nm.scan(hosts=target_ip, arguments='-O')

    if target_ip in nm.all_hosts():
        host = nm[target_ip]
        # Beautify (pretty print) the JSON data
        formatted_json = json.dumps(host, indent=4)

        # Print the formatted JSON
        print(formatted_json)

        # Dump the formatted JSON data to a file
        #with open("formatted_data.json", "w") as json_file:
        #    json.dump(host, json_file, indent=4)
            
        if 'osmatch' in host:
            os_match = host['osmatch']
            for match in os_match:
                print(f"Operating System Guess: {match['osclass'][0]['vendor']} {match['osclass'][0]['osfamily']} {match['osclass'][0]['osgen']}: {match['osclass'][0]['accuracy']}%")
        else:
            print("No OS information available.")
    else:
        print(f"Host {target_ip} is down or not responding.")

if __name__ == "__main__":
    #target_ip = input("Enter the IP address of the device to detect its OS: ")
    target_ip = "192.168.2.34"
    detect_os(target_ip)
