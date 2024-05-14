import requests

def send_command(command):
    url = 'http://127.0.0.1:5863/management'
    data = {'command': command}
    response = requests.post(url, json=data)
    
    # Verbose
    # print("Response Status Code:", response.status_code)
    # print("Response Content:", response.content)

    return response.json()

def help_message():
    print("Available Commands:")
    print("- status: General module report.")
    print("- algorithm [automation] [auto/default/random]: Pick an algorithm for automation.")
    print("- list [automation]: shows all available algorithms")
    print("- help [command]: Additional help for a command.")
    print("- exit: Quit the client application.")

if __name__ == '__main__':

    # Welcome text
    print("Network Optimizer Client | Desire6G")
    print("Enter command and press the Return key to execute, type help for a list of commands\n")

    # Loop
    while True:
        command = input("] ")

        # Filter input
        command = command.lower().split(" ")

        # Cases

        if command[0] == "help":
            help_message()
        elif command[0] == "status":
            result = send_command(command)
            print("Response:", result)
        elif command[0] == "algorithm":
            if len(command) != 2:
                result = send_command(command)
                print("Response:", result)
            else:
                print("Missing arguments, type help.")
        elif command[0] == "list":
            if len(command) != 1:
                result = send_command(command)
                print("Response:", result)
            else:
                print("Second argument missing.")
        elif command[0] == "exit":
            break
        elif command[0] == "":
            pass
        else:
            print("Command not found!")
