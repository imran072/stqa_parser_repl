# STQA REPL Parser

This project implements a Read-Eval-Print Loop (REPL) for parsing various commands related to lighting, appliances, barriers, and thermal devices. The project demonstrates parsing based on a grammar and handles user inputs through a command-line interface. The parser is implemented in Python and can be run via Docker.

## Features

- Supports commands for lighting, appliances, barriers, and thermal devices
- Flexible command structure with optional location
- Validates inputs and provides responses based on the command
- Implemented REPL loop to continually process user input
- Dockerized for easy setup and usage

## Grammar Rules

The following grammar rules are used to parse the commands:

```ebnf
<command> ::= <location>? ( <lighting_command> | <barrier_command> | <appliance_command> | <thermal_device_command> )

<lighting_command> ::= "turn" <light_source> <state>
<thermal_device_command> ::= "set" <thermal_device> "to" <temperature>
<barrier_command> ::= <barrier_action> <barrier>
<appliance_command> ::= "turn" <appliance> <state>

<barrier_action> ::= "lock" | "unlock" | "open" | "close"
<state> ::= "on" | "off"
<temperature> ::= <number> "K"

<light_source> ::= "lamp" | "bulb" | "neon" | "sconce" | "brazier"
<barrier> ::= "gate" | "curtains" | "garage-door" | "blinds" | "window" | "shutter"
                | "trapdoor" | "portcullis" | "drawbridge" | "blast-door" | "airlock"
<thermal_device> ::= "oven" | "thermostat" | "electric-blanket" | "incinerator"
                      | "reactor-core"
<appliance> ::= "coffee-maker" | "oven" | "air-conditioner" | "centrifuge"
                "synchrotron" | "laser-cannon"
```

# Setup and Usage
## Running with Python

- **Clone the repository:**

```bash
git clone https://github.com/imran072/stqa-repl-parser.git
cd stqa-repl-parser
```

- **Run the REPL loop using Python:**
```bash
python3 parser_repl.py
```
- To exit the REPL, type `exit`.

# Running with Docker
- Pull the Docker image from Docker Hub:

```bash
docker pull imran072/stqa-repl-parser:latest
```

- Run the Docker container:
```bash
docker run -it imran072/stqa-repl-parser:latest
```