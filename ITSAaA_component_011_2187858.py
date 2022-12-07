import datetime

from netmiko import ConnectHandler

import msvcrt as m

import os

import netifaces

from urllib.request import urlopen

# clear function prints 100 break lines to "clean" terminal
def clear():
        
        print("\n" * 100)

# wait function to wait for button press after option selected is finished running  
def wait():
        print ("\nPress any key to continue...\n")
        m.getch()

# current_time will print the current time on the local machine
def current_time():
        try:

                now = datetime.datetime.now()

                print ("Current date and time is: ")
                print (now.strftime("%Y-%m-%d %H:%M:%S"))

                wait()
                clear()
        except:
                print("Error: Could not print current date and time...\n")
                wait()
                clear()
                return

# ip_address will print the current client's ip address
def ip_address():
        # Get the name of the default network interface
        default_interface = netifaces.gateways()['default'][netifaces.AF_INET][1]

        try:
                # Get the IPv4 address of the default interface
                ipv4_address = netifaces.ifaddresses(default_interface)[netifaces.AF_INET][0]

                # Print the IP address
                print("This client's local IP address is "+ipv4_address['addr'])

                wait()
                clear()
        except:
                print("Error: Failed to print the client's IP address...\n")
                wait()
                clear()
                return

# vm_connect will be called to connect to the remote host
def vm_connect():
        try:
  
                # Define the device's connection parameters
                global vm
                vm = ConnectHandler(
                device_type = "linux",
                host = "192.168.1.220",
                username = "lubuntu",
                password = "123")

                
        except:
                print("Error: Connection to the remote host failed...\n")
                wait()
                clear()
                return

# Remote_ls will connect to a remote computer using SSH
# then run an ls command in the home directory       
def remote_ls():
        try:
                vm_connect()

                # Define path and command thay will be sent to the linux vm
                path = "/home/lubuntu"
                command = "ls -l " + path
        
                # Send a command to the Linux VM and print the output
                ls_output = vm.send_command(command)
                print(ls_output)

                wait()
                clear()
        except:
                print("Error: Could not list the home directory...\n")
                wait()
                clear()
                return

# Remote_backup will take in a directory path and a file in that path
# and back up the file in the same directory
def remote_backup():
        try:
                vm_connect()
        
                # User enters path and the command is sent to the remote host
                path2 = input("Please enter the path of the directory you want to access: ")
                current_path_and_ls = vm.send_command("cd "+ path2 + " ; ls -l", read_timeout=120)
        except:
                print("Error: Could not access the selected directory...\n")
                wait()
                clear()
                return
        try:
                # Prints current directory contents
                print(current_path_and_ls)

                # User enters file name and a backup command is sent to the terminal
                file = input("\nPlease enter the name of the file you want to back up: ")
                print("\n")
                backup_and_ls = vm.send_command("cp --backup " + file + " " + file + ".old ;ls -l")

                # Prints updates directory contents
                print(backup_and_ls + "\n")

                wait()
                clear()
        except:
                print("Error: Back up request has failed...\n")
                wait()
                clear()
                return

# Save_html will request a url from the user and a directory
# and save the html code of the url in that directory
def save_html():

        
    
        
    
        try:
                # Ask the user for a URL
                url = input("\nPlease enter a URL: ")

                #parsed_url = urlparse(url)
                response = urlopen(url)
        except ValueError:

                # If the URL is invalid, print an error message and return
                print("Error: Invalid URL...")
                wait()
                clear()
                return
        except:
                print("Error: Could not open URL...")
                wait()
                clear()
                return
    
        # Ask the user for the directory where the file should be saved
        directory = input("\nPlease enter the directory you want to save the url to: ")

        # Read the response from the URL and decode it
        content = response.read().decode()
    
        # Asking the user for a filename
        filename = input("\nPlease enter a filename: ")
    
        # Creating the full path to the file
        filepath = os.path.join(directory, filename + ".txt")

        try:

                # Write the content to the file
                with open(filepath, "w") as file:
                        file.write(content)
                print("\nSelected url has been successfully saved...")
        except:
                print("Error: Could not write to file...")
                wait()
                clear()
                return
        wait()
        clear()



# This function will quit the program with cleanly with no errors   
def quit():
        try:
                print("Goodbye!")
                os._exit(1)
        except:
                print("Fatal error! Can not quit the program...")
                wait()
                clear()
                return

# Making a directory with all the options and their keys
menu = {
    "1": ["Show date and time (local computer)", current_time],
    "2": ["Show IP address (local computer)", ip_address],
    "3": ["Show Remote home directory listing", remote_ls],
    "4": ["Backup remote file", remote_backup],
    "5": ["Save web page", save_html],
    "Q": ["Quit", quit]
}

# While loop to go through the menu after a function has finished running
while True:

        # Going through the directory keys to print the menu
        for key in menu.keys():
                print(key + " - " + menu[key][0])
                
        selection = input("\nPlease select: ")
        print("\n")

        # Checking if the input is valid
        if selection in menu.keys() or selection in ["q", "Q"]:

                if selection in menu.keys():

                        # Calling the function associated with the input
                        menu[selection][1]()
                else:
                        quit()
        
        else:
                print("Invalid selection. Please try again.\n")  



        



        

                
