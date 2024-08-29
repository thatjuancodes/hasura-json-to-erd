# hasura_json_to_erd

This is a collection of python scripts for converting hasura graphql schema.json export to an ERD diagram

## Table of Contents

- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)

## Dependencies

I'm using 3.9.7 as I'm developing this. I'm guessing any python version that works well with graphviz

## Installation

Instructions on how to install and set up the project.

```sh
# Clone the repository
git clone https://github.com/thatjuancodes/hasura-json-to-erd.git

# Navigate to the project directory
cd hasura-json-to-erd

# Install dependencies
pip install graphviz
```

## Usage

1. Export your hasura schema.json file
2. Place it in the root directory of this project
3. Run the commands:

- For converting to an image
```sh
python setup.py schema.json
```

- For showing the tables on the command line
```sh
`python extract_tables.py`
```

- For converting to mermaid markdown format
```sh
`python convert_to_mermaid_syntax.py schema.json`
```

Note: for mermaid format, you can go to [this playground site](https://mermaid.live/edit) and paste the results from the generated .md file and it will show the diagram for you