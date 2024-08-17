import sys
import time
import socket
import subprocess
import dns.resolver as dns_resolver
import requests
import signal

# ANSI escape codes for color
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

# Your Discord webhook URL
DISCORD_WEBHOOK_URL = "Enter your Discord API_Key Here!"

def send_discord_notification(message):
    """
    Sends a notification to Discord using a webhook.
    """
    payload = {
        "content": message
    }
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

def resolve_domain(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        print(f"IP address for {domain}: {GREEN}{ip_address}{RESET}")
        send_discord_notification(f"Resolved {domain} to IP address: {ip_address}")
        return ip_address
    except socket.gaierror:
        send_discord_notification(f"Could not resolve {domain}")
        print(f"Could not resolve {domain}")

def is_domain_alive(domain):
    try:
        ip_address = resolve_domain(domain)
        if ip_address:
            result = subprocess.call(['ping', '-c', '1', ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            status = "alive" if result == 0 else "not responding to ping"
            send_discord_notification(f"{domain} is {status} : {ip_address}")
    except Exception as e:
        send_discord_notification(f"Error occurred: {e}")
        print(f"Error occurred: {e}")

def get_dns_records(domain):
    record_types = ['A', 'CNAME', 'MX', 'NS']
    
    for record_type in record_types:
        try:
            answers = dns_resolver.resolve(domain, record_type)
            send_discord_notification(f"Fetching {record_type} records for {domain}")
            print(f"{GREEN}{record_type} records for {domain}{RESET}:")
            for rdata in answers:
                print(rdata)
        except (dns_resolver.NoAnswer, dns_resolver.NXDOMAIN):
            send_discord_notification(f"No {record_type} records found for {domain}")
            print(f"{RED}No {record_type} records found for {domain}{RESET}")

def enumerate_subdomains(domain):
    try:
        # Notify that subfinder is running
        send_discord_notification("Subfinder is running!")

        # Run the subfinder command and capture the output
        subfinder_result = subprocess.run(['subfinder', '-d', domain], capture_output=True, text=True)

        # Check if there were any errors
        if subfinder_result.returncode != 0:
            send_discord_notification(f"Error occurred during subfinder execution: {subfinder_result.stderr}")
            print(f"Error occurred during subfinder execution: {subfinder_result.stderr}")
            return

        # Print the output of the subfinder command
        subdomains = subfinder_result.stdout.splitlines()
        with open("subfinder.txt", "w") as file:
            for subdomain in subdomains:
                file.write(subdomain + "\n")
        send_discord_notification("Subfinder execution completed: File saved in subfinder.txt")
        print("Subfinder enumeration completed.")
        send_discord_notification("Subfinder enumeration completed.")
    except Exception as e:
        send_discord_notification(f"Error occurred during subdomain enumeration: {e}")
        print(f"Error occurred during subdomain enumeration: {e}")

def enumerate_assets(domain):
    try:
        # Notify that assetfinder is running
        send_discord_notification("Assetfinder is running!")

        # Using subprocess.PIPE to capture the output of assetfinder
        assetfinder_process = subprocess.Popen(['assetfinder', domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for the assetfinder process to finish and get the output
        assetfinder_output, assetfinder_error = assetfinder_process.communicate()
        
        # Print the output of the assetfinder process (if any)
        if assetfinder_output is not None:
            assets = assetfinder_output.decode().splitlines()
            with open("assetfinder.txt", "w") as file:
                for asset in assets:
                    file.write(asset + "\n")
            send_discord_notification("Assetfinder execution completed: File saved in assetfinder.txt")
            print("Assetfinder enumeration completed.")
            send_discord_notification("Assetfinder enumeration completed.")
        else:
            send_discord_notification("Assetfinder execution failed.")
            print("Assetfinder execution failed.")
    except Exception as e:
        send_discord_notification(f"Error occurred during asset enumeration: {e}")
        print(f"Error occurred during asset enumeration: {e}")

def enumerate_amass(domain):
    try:
        # Notify that Amass is running
        send_discord_notification("Amass is running!")

        # Open the file for appending
        with open("amass_raw.txt", "a") as file:
            # Run the amass command with stdout as a PIPE
            amass_process = subprocess.Popen(['amass', 'enum', '-d', domain], stdout=subprocess.PIPE, text=True)

            # Read and append each line to the file in real-time
            for line in iter(amass_process.stdout.readline, ''):
                # Write the line to the file
                file.write(line)
                file.flush()  # Force the buffer to flush to the file

            # Wait for the amass process to finish
            amass_process.wait()

        send_discord_notification("Amass execution completed. Data saved in amass_raw.txt")
        print("Amass enumeration completed. Data saved in amass_raw.txt")
        send_discord_notification("Amass enumeration completed.")
    except Exception as e:
        send_discord_notification(f"Error occurred during Amass enumeration: {e}")
        print(f"Error occurred during Amass enumeration: {e}")

def handle_interrupt(signal, frame):
    print("\nInterruption Detected... Exiting... Thank you for using SubInspector!")
    sys.exit(0)

if __name__ == "__main__":
    # Register the interrupt signal handler
    signal.signal(signal.SIGINT, handle_interrupt)

    # Print the introductory information with a delay
    intro = """
\033[93mNATIONAL FORENSIC SCIENCES UNIVERSITY\033[0m
Name: Sahil Shah
Enrollment: 01230030008002022
Project Guide: \033[94mMr. Prakash Khasor\033[0m
Minor Project M.Sc. Cyber Security Sem II
"""

    for char in intro:
        sys.stdout.write(char)
        sys.stdout.flush()
        if char != '\n':  # Adjust to skip newlines if needed
            time.sleep(0.02)  # Adjust the delay for the desired speed

    print("\n")

    # ASCII art for "SubInspector"
    subinspect_ascii_art = [
        """
  _________       ___.     .___                         ________            __   
 /   _____/ __ __ \_ |__   |   |  ____    ____________  \_____  \   ____  _/  |_ 
 \_____  \ |  |  \ | __ \  |   | /    \  /  ___/\____ \   _(__  < _/ ___\ \   __\\
/_______  /|____/  |___  / |___||___|  //____  >|   __/ /______  / \___  > |__|  
        \/             \/            \/      \/ |__|           \/      \/        
                                                                                
~ Sahil_Shah

        """
    ]

    for line in subinspect_ascii_art:
        print(line)
        time.sleep(0.2)  # Adjust the delay for the desired speed

    if len(sys.argv) != 2:
        print("Usage: python <script_name> <domain>")
        sys.exit(1)

    domain_name = sys.argv[1]
    print("Resolving domain...")
    ip_address = resolve_domain(domain_name)
    if ip_address:
        print("\nChecking if domain is alive...")
        is_domain_alive(domain_name)
        print("\nRetrieving DNS records...")
        get_dns_records(domain_name)
        print("\nEnumerating subdomains...")
        enumerate_subdomains(domain_name)
        print("\nEnumerating assets...")
        enumerate_assets(domain_name)
        print("\nEnumerating subdomains with Amass...")
        enumerate_amass(domain_name)
