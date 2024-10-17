import re

# Updated pattern to disallow whitespace in location (only allows alphanumeric characters and hyphens)
COMMAND_PATTERN = r"^(?P<location>[a-zA-Z0-9\-]+)?\s*(?P<subcommand>turn\s+\w+\s+\w+|set\s+\w+(-\w+)?\s+to\s+\d+\s+K|open\s+\w+|close\s+\w+)$"

# Define individual subcommand patterns
LIGHTING_COMMAND_PATTERN = r"turn\s+(?P<device>\w+)\s+(?P<state>\w+)"
THERMAL_DEVICE_COMMAND_PATTERN = r"set\s+(?P<device>\w+(-\w+)?)\s+to\s+(?P<temperature>\d+)\s+K"
BARRIER_COMMAND_PATTERN = r"(?P<action>(open|close|lock|unlock))\s+(?P<barrier>(gate|curtains|garage-door|blinds|window|shutter|trapdoor|portcullis|drawbridge|blast-door|airlock))"
APPLIANCE_COMMAND_PATTERN = r"turn\s+(?P<appliance>\w+)\s+(?P<state>\w+)"

# Updated lists for valid devices, appliances, barriers, etc.
VALID_LIGHT_SOURCES = ['lamp', 'bulb', 'neon', 'sconce', 'brazier']
VALID_THERMAL_DEVICES = ['oven', 'thermostat', 'electric-blanket', 'incinerator', 'reactor-core']
VALID_BARRIERS = ['gate', 'curtains', 'garage-door', 'blinds', 'window', 'shutter', 'trapdoor', 'portcullis', 'drawbridge', 'blast-door', 'airlock']
VALID_APPLIANCES = ['coffee-maker', 'oven', 'air-conditioner', 'centrifuge', 'synchrotron', 'laser-cannon']
VALID_ACTIONS = ['open', 'close', 'lock', 'unlock']
VALID_STATES = ['on', 'off']

def parse_command(command):
    """Parse the command using a regular expression and then delegate to subcommands."""
    match = re.match(COMMAND_PATTERN, command.strip())
    
    if not match:
        return None, None

    # Extract location and subcommand
    location = match.group('location') or 'unspecified location'
    subcommand = match.group('subcommand').strip()

    # Print out what has been captured for debugging
    print(f"Location: {location}")
    print(f"Subcommand: {subcommand}")

    # Match subcommands in correct priority order
    if re.match(LIGHTING_COMMAND_PATTERN, subcommand):
        return {"location": location.strip(), "subcommand": re.match(LIGHTING_COMMAND_PATTERN, subcommand).groupdict(), "type": "lighting"}, "lighting"
    elif re.match(THERMAL_DEVICE_COMMAND_PATTERN, subcommand):
        return {"location": location.strip(), "subcommand": re.match(THERMAL_DEVICE_COMMAND_PATTERN, subcommand).groupdict(), "type": "thermal_device"}, "thermal_device"
    elif re.match(BARRIER_COMMAND_PATTERN, subcommand):
        return {"location": location.strip(), "subcommand": re.match(BARRIER_COMMAND_PATTERN, subcommand).groupdict(), "type": "barrier"}, "barrier"
    elif re.match(APPLIANCE_COMMAND_PATTERN, subcommand):
        return {"location": location.strip(), "subcommand": re.match(APPLIANCE_COMMAND_PATTERN, subcommand).groupdict(), "type": "appliance"}, "appliance"
    
    return None, None

def validate_command(parsed_command, command_type):
    """Validate the parsed command based on the command type."""
    subcommand = parsed_command['subcommand']
    
    if command_type == "lighting":
        device = subcommand['device']
        state = subcommand['state']
        if device not in VALID_LIGHT_SOURCES:
            return f"Invalid light source: {device}. Valid light sources are: {', '.join(VALID_LIGHT_SOURCES)}"
        if state not in VALID_STATES:
            return f"Invalid state: {state}. Valid states are: {', '.join(VALID_STATES)}"
    
    elif command_type == "thermal_device":
        device = subcommand['device']
        temperature = subcommand['temperature']
        if device not in VALID_THERMAL_DEVICES:
            return f"Invalid thermal device: {device}. Valid thermal devices are: {', '.join(VALID_THERMAL_DEVICES)}"
        # No restriction on temperature range, so accepting any numeric input

    elif command_type == "barrier":
        action = subcommand['action']
        barrier = subcommand['barrier']
        if barrier not in VALID_BARRIERS:
            return f"Invalid barrier: {barrier}. Valid barriers are: {', '.join(VALID_BARRIERS)}"
        if action not in VALID_ACTIONS:
            return f"Invalid action: {action}. Valid actions are: {', '.join(VALID_ACTIONS)}"
    
    elif command_type == "appliance":
        appliance = subcommand['appliance']
        state = subcommand['state']
        if appliance not in VALID_APPLIANCES:
            return f"Invalid appliance: {appliance}. Valid appliances are: {', '.join(VALID_APPLIANCES)}"
        if state not in VALID_STATES:
            return f"Invalid state: {state}. Valid states are: {', '.join(VALID_STATES)}"

    return None  # No validation issues

def repl():
    """REPL loop that reads and evaluates commands."""
    # Define grammar rules
    grammar_rules = """
    Grammar Rules:
    <command> ::= <location>? ( <lighting_command> | <barrier_command> | <appliance_command> | <thermal_device_command> )

    <lighting_command> ::= "turn" <light_source> <state>
    <thermal_device_command> ::= "set" <thermal_device> "to" <number> "K"
    <barrier_command> ::= <barrier_action> <barrier>
    <appliance_command> ::= "turn" <appliance> <state>

    <light_source> ::= "lamp" | "bulb" | "neon" | "sconce" | "brazier"
    <barrier> ::= "gate" | "curtains" | "garage-door" | "blinds" | "window" | "shutter"
                | "trapdoor" | "portcullis" | "drawbridge" | "blast-door" | "airlock"
    <thermal_device> ::= "oven" | "thermostat" | "electric-blanket" | "incinerator"
                        | "reactor-core"
    <appliance> ::= "coffee-maker" | "oven" | "air-conditioner" | "centrifuge"
                  "synchrotron" | "laser-cannon"
    <state> ::= "on" | "off"
    <barrier_action> ::= "open" | "close" | "lock" | "unlock"
    <number> ::= any sequence of digits
    """
    print("Welcome to the REPL Command.")
    print(grammar_rules)  # Print the grammar rules at the start
    print("Type your command to test the validity or Type 'exit' to quit.\n")
    
    while True:
        command = input("> ")
        if command.lower() == "exit":
            print("Exiting...")
            break
        
        parsed_command, command_type = parse_command(command)
        if parsed_command:
            # Validate the parsed command
            validation_error = validate_command(parsed_command, command_type)
            if validation_error:
                print(validation_error)
            else:
                # Generate canned responses based on the command type
                location = parsed_command['location']
                subcommand = parsed_command['subcommand']
                if command_type == "lighting":
                    print(f"Turning {subcommand['device']} {subcommand['state']} in {location}.")
                elif command_type == "thermal_device":
                    print(f"Setting {subcommand['device']} to {subcommand['temperature']} K in {location}.")
                elif command_type == "barrier":
                    print(f"{subcommand['action'].capitalize()} the {subcommand['barrier']} in {location}.")
                elif command_type == "appliance":
                    print(f"Turning {subcommand['appliance']} {subcommand['state']} in {location}.")
        else:
            print("Invalid command format.")

if __name__ == "__main__":
    repl()
