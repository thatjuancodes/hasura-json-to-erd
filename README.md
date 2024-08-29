# hasura_json_to_erd

This is a collection of python scripts for converting hasura graphql schema.json export to an ERD diagram

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)

## Installation

Instructions on how to install and set up the project.

```sh
# Clone the repository
git clone https://github.com/thatjuancodes/hasura-json-to-erd.git

# Navigate to the project directory
cd hasura-json-to-erd

# Install dependencies
pip install graphviz

## Usage

1. Export your hasura schema.json file
2. Place it in the root directory of this project
3. Run the commands:

- For converting to an image
`python setup.py schema.json`

- For showing the tables on the command line
`python extract_tables.py`

- For converting to mermaid markdown format
`python convert_to_mermaid_syntax.py schema.json`

Note: for mermaid format, you can go to this playround and paste the results from the generated .md file and it will show the diagram for you