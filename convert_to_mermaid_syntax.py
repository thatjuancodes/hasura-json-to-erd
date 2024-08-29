import json

def extract_tables_from_schema(schema_file):
    with open(schema_file, 'r') as f:
        schema = json.load(f)
    
    # Check if the schema is nested under 'data' or directly under '__schema'
    if '__schema' in schema:
        schema_data = schema['__schema']
    elif 'data' in schema and '__schema' in schema['data']:
        schema_data = schema['data']['__schema']
    else:
        raise KeyError("The schema does not contain a '__schema' key.")
    
    tables = []

    for type_data in schema_data['types']:
        # Exclude system-generated types and specific keywords
        if (type_data['kind'] == 'OBJECT' and 
            not type_data['name'].startswith(('query_root', 'mutation_root', 'subscription_root', 'hasura_', '_')) and
            not any(keyword in type_data['name'] for keyword in ['mutation', 'max', 'min', 'aggregate', 'stddev', 'sum', 'var', 'avg'])):
            columns = [field['name'] for field in type_data['fields']]
            tables.append({'name': type_data['name'], 'columns': columns})
    
    return tables

def generate_mermaid_erd(tables):
    erd = ["erDiagram"]
    
    for table in tables:
        erd.append(f"    {table['name']} {{")
        for column in table['columns']:
            erd.append(f"        string {column}")
        erd.append("    }")
    
    return "\n".join(erd)

def main():
    schema_file = './schema.json'  # Replace with the path to your schema.json file
    output_file = './erd_diagram.md'  # Replace with the desired output file path
    
    tables = extract_tables_from_schema(schema_file)
    erd = generate_mermaid_erd(tables)
    
    with open(output_file, 'w') as f:
        f.write(erd)

if __name__ == '__main__':
    main()