def get_command(response):
    """Parse the response and return the command name and arguments"""
    command = response["command"]
    if "name" not in command:
        return "Error:", "Missing 'name' field in 'command' object"
    command_name = command["name"]
    # Use an empty dictionary if 'args' field is not present in 'command' object
    arguments = command.get("args", {})

    return command_name, arguments

def execute_command(command_name, arguments):
    """Execute the command and return the result"""
    if command_name == "google":
        print(f"Execute google command {command_name} {arguments}")
        return "result: hello world"