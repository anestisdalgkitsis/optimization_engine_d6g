import requests

def send_command(command):
    url = 'http://127.0.0.1:5000/management'
    data = {'command': command}
    response = requests.post(url, json=data)
    
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.content)

    return response.json()

def help_message():
    print("Available Commands:")
    print("- status: Report")
    print("- algorithm [automation] [auto/default/random]: Pick an algorithm for automation.")
    print("- list [automation]: shows all available algorithms")
    print("- help [command]: Additional help for a command.")
    print("- exit: Quit the client application.")

if __name__ == '__main__':

    # Welcome text
    print("Network Optimizer Client | Desire6G")
    print("Enter command and press the Return key to execute, type help for a list of commands")

    # Loop
    while True:
        command = input("] ")

        # Filter input
        command = command.lower().split(" ")

        # Cases

        if command[0] == "help":
            help_message()
        elif command[0] == "status":
            if len(command) is not 1:
                result = send_command(command[1])
                print("Server response:", result)
            else:
                print("Second argument missing.")
        elif command[0] == "algorithm":
            if len(command) is not 1:
                result = send_command(command[1])
                print("Server response:", result)
            else:
                print("Second argument missing.")
        elif command[0] == "list":
            if len(command) is not 1:
                result = send_command(command[1])
                print("Server response:", result)
            else:
                print("Second argument missing.")
        elif command[0] == "exit":
            break
        elif command[0] == "":
            pass
        else:
            print("Command not found!")
