import json

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

def main():
    schema_file = './schema.json'  # Replace with the path to your schema.json file
    
    # Load the schema.json file
    with open(schema_file, 'r') as file:
        schema = json.load(file)
    
    # Extract relationships
    relationships = extract_relationships(schema)
    
    # Display the relationships
    for table, rels in relationships.items():
        print(f"Table: {table}")
        for rel in rels:
            print(f"  Relationship: {rel[0]}, Related Table: {rel[1]}")

    # Display total tables
    total_tables = len(relationships)
    print(f"Total tables with relationships: \033[92m{total_tables}\033[0m")

    # Display total count of relationships
    total_relationships = sum(len(rels) for rels in relationships.values())
    print(f"Total relationships extracted: \033[92m{total_relationships}\033[0m")

if __name__ == "__main__":
    main()