import json

def extract_tables_and_fields(schema):
    tables = {}

    # Iterate over the types in the schema
    for type_def in schema.get('__schema', {}).get('types', []):
        type_description = type_def.get('description', '')
        if isinstance(type_description, str) and type_description.startswith('columns and relationships of'):
            table_name = type_def['name']
            columns = []
            
            for field in type_def.get('fields', []):
                if field.get('description') is None:
                    field_name = field['name']
                    field_type = field['type'].get('name') or field['type'].get('ofType', {}).get('name')
                    columns.append({'name': field_name, 'type': field_type})
            
            tables[table_name] = columns

    return tables

def main():
    schema_file = './schema.json'  # Replace with the path to your schema.json file
    
    # Load the schema.json file
    with open(schema_file, 'r') as file:
        schema = json.load(file)
    
    tables = extract_tables_and_fields(schema)
    
    # Display the tables and fields
    for table, fields in tables.items():
        print(f"Table: {table}")
        for field in fields:
            print(f"  Field: {field['name']}, Type: {field['type']}")

if __name__ == "__main__":
    main()