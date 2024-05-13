import requests

def send_command(command):
    url = 'http://127.0.0.1:5000/execute'
    data = {'command': command}
    response = requests.post(url, json=data)
    return response.json()

if __name__ == '__main__':
    command = input("Enter command: ")
    result = send_command(command)
    print("Server response:", result)
