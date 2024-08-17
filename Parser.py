import subprocess
import time
import requests
import signal

# Discord webhook URL
DISCORD_WEBHOOK_URL = "Enter your Discord API_Key Here!"

# ANSI escape codes for color
RED = '\033[91m'
RESET = '\033[0m'

def send_discord_notification(message):
    """
    Sends a notification to Discord using a webhook.
    """
    payload = {"content": message}
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

def print_highlighted(message, color=RESET):
    """
    Prints a message with optional color highlighting.
    """
    print(f"{color}{message}{RESET}")

def process_amass_output(input_file):
    try:
        # Read all lines from the input file
        with open(input_file, "r") as infile:
            lines = infile.readlines()

        # Extract the first field from each line, sort, and remove duplicates
        unique_lines = sorted(set(line.split()[0] for line in lines))

        # Write the unique lines to the output file
        with open("amass.txt", "w") as outfile:
            for line in unique_lines:
                outfile.write(line + "\n")

        print("Processed Amass output successfully")
        send_discord_notification("Amass.txt Created..!")
    except Exception as e:
        print(f"Error processing Amass output: {e}")

def combine_and_sort_files():
    try:
        # Wait for 2 seconds to ensure amass.txt file is created
        time.sleep(2)
        print_highlighted("Combining files...")

        # Use cat command to combine subfinder.txt, assetfinder.txt, and amass.txt
        subprocess.run(["cat", "assetfinder.txt", "subfinder.txt", "amass.txt"], stdout=open("combined.txt", "w"), stderr=subprocess.PIPE, text=True)

        print("Combined files successfully")
        send_discord_notification("Combined.txt Created..!")
    except Exception as e:
        print(f"Error combining files: {e}")

def grep_keyword():
    try:
        # Prompt user to enter the keyword to grep
        keyword = input("Enter The GREP Keyword: ")

        # Use grep command to filter lines containing the keyword
        subprocess.run(["grep", keyword, "combined.txt"], stdout=open("temp.txt", "w"), stderr=subprocess.PIPE, text=True)

        # Rename the temporary file to combined.txt
        subprocess.run(["mv", "temp.txt", "combined.txt"], stderr=subprocess.PIPE, text=True)

        print("Grep command executed successfully")
        send_discord_notification("Grep Executed..!")
    except Exception as e:
        print(f"Error executing grep command: {e}")

def run_httprobe():
    try:
        # Wait for 10 seconds after combined.txt file is created
        time.sleep(5)
        print_highlighted("--------------------------------------")
        print_highlighted("~   Here Are The LIVE Sub-Domains   ~", color=RED)
        print_highlighted("--------------------------------------")

        # Run httprobe command on combined.txt and display output in terminal
        with open("combined.txt", "r") as infile:
            subprocess.run(["httprobe", "-c", "10"], stdin=infile, text=True)

        print("httprobe command executed successfully")
    except Exception as e:
        print(f"Error executing httprobe command: {e}")

def handle_interrupt(signal, frame):
    print("\nInterruption Detected... Exiting... Thank you for using SubInspect!")
    send_discord_notification("SubInspect process interrupted by user")
    exit(0)

def collect_output():
    """
    Collects the output of the script and sends it to Discord.
    """
    with open("output.txt", "w") as output_file:
        subprocess.run(["python3", "auto_amass.py"], stdout=output_file, stderr=subprocess.PIPE, text=True)
    with open("output.txt", "r") as output_file:
        output_message = output_file.read()
    send_discord_notification(output_message)

if __name__ == "__main__":
    # Register the interrupt signal handler
    signal.signal(signal.SIGINT, handle_interrupt)

    # Main program logic
    process_amass_output("amass_raw.txt")
    combine_and_sort_files()
    grep_keyword()
    run_httprobe()
    collect_output()
