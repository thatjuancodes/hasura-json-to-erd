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

def extract_relationships(schema):
    relationships = {}
    
    # Iterate over the types in the schema
    for type_def in schema.get('__schema', {}).get('types', []):
        type_description = type_def.get('description', '')
        if isinstance(type_description, str) and type_description.startswith('columns and relationships of'):
            table_name = type_def['name']
            table_relationships = []
            
            for field in type_def.get('fields', []):
                if field.get('description') in ['An object relationship', 'An array relationship', 'An aggregate relationship']:
                    relationship_name = field['name']
                    related_table = field['type'].get('name') or field['type'].get('ofType', {}).get('name')
                    table_relationships.append((relationship_name, related_table))
            
            if table_relationships:
                relationships[table_name] = table_relationships
    
    return relationships

def generate_mermaid_erd(tables, relationships):
    erd = ["erDiagram"]
    
    # Add tables and their columns
    for table in tables:
        erd.append(f"    {table['name']} {{")
        for column in table['columns']:
            erd.append(f"        string {column}")
        erd.append("    }")

    # Add relationships
    for table, rels in relationships.items():
        for relationship_name, related_table in rels:
            erd.append(f"    {table} ||--o{{ {related_table} : {relationship_name}")
    
    return "\n".join(erd)

def main():
    schema_file = './schema.json'  # Replace with the path to your schema.json file
    output_file = './erd_diagram.md'  # Replace with the desired output file path
    
    # Load the schema.json file
    with open(schema_file, 'r') as file:
        schema = json.load(file)
    
    tables = extract_tables_from_schema(schema_file)
    # Extract relationships
    relationships = extract_relationships(schema)
    erd = generate_mermaid_erd(tables, relationships)
    
    with open(output_file, 'w') as f:
        f.write(erd)

if __name__ == '__main__':
    main()