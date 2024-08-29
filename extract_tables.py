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
            not any(keyword in type_data['name'] for keyword in ['mutation', 'max', 'min', 'aggregate', 'stddev', 'sum', 'var'])):
            columns = [field['name'] for field in type_data['fields']]
            tables.append({'name': type_data['name'], 'columns': columns})
    
    return tables

def main():
    schema_file = './schema.json'  # Replace with the path to your schema.json file
    tables = extract_tables_from_schema(schema_file)
    
    for table in tables:
        print(f"Table: {table['name']}")
        print("Columns:")
        for column in table['columns']:
            print(f"  - {column}")
        print()

if __name__ == '__main__':
    main()