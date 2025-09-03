# MCP DEMO

Testing and demonstration of the Model Content Protocol (MCP) using Python. This project enables you to experiment with and test any MCP server implementation utilizing Pydantic AI.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

This repository provides a demonstration framework for the Model Content Protocol (MCP), enabling users to test MCP server implementations using Python and Pydantic AI.  
It is intended as a collection of examples and test scripts for learning, experimentation, and interoperability testing.

## Features

- Test compatibility with any MCP server
- Built with Python and Pydantic for robust data validation
- Example scripts and configuration for quick experimentation

## Getting Started

These instructions will help you set up the project on your local machine.

### Prerequisites

- Python 3.12 or newer
- Node.js v22 or newer

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/PramudiR/mcp-demo.git
   cd mcp-demo
   ```
2. **(Optional) Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install required Python packages:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Install Node.js dependencies (if applicable):**
   ```bash
   npm install
   ```

## Usage

This repository is a demo and does not have a single entry point or main script.

- Browse the repository for sample code and scripts related to MCP testing.
- Review code comments and documentation in each Python file for instructions on how to run or adapt individual examples.
- Run specific scripts using:
  ```bash
  python path/to/example_script.py
  ```
- Refer to included documentation or comments for details on script functionality and prerequisites.

Feel free to experiment with and modify the examples to fit your MCP server implementation or testing needs.

Additionally, You can use following shell script to activate the environments. Here's an example code for the .envrc file
```bash
# Use existing Python venv
source .venv/bin/activate

# Use Node.js v22 via nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm use 22
```

## Contributing

Contributions, issues, and feature requests are welcome!

1. Fork this repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

Maintained by [PramudiR](https://github.com/PramudiR).
Collab with [Apex-Tensor](https://github.com/PramudiR-Tensor).

Feel free to open issues or reach out with questions.
