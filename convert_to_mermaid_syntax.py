import json
import sys

def extract_tables_from_schema(schema):
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
    
    # Add tables and their columns in Mermaid syntax
    for table, fields in tables.items():
        erd.append(f"class {table} {{")
        for field in fields:
            erd.append(f"  {field['type']} {field['name']}")
        erd.append("}")

    # Add relationships
    for table, rels in relationships.items():
        for relationship_name, related_table in rels:
            erd.append(f"    {table} ||--o{{ {related_table} : {relationship_name}")
    
    return "\n".join(erd)

def generate_mermaid_erd_tables_only(tables):
    erd = ["erDiagram"]
    
    # Add tables and their columns in Mermaid syntax
    for table, fields in tables.items():
        erd.append(f"class {table} {{")
        for field in fields:
            erd.append(f"  {field['type']} {field['name']}")
        erd.append("}")
    
    return "\n".join(erd)

def main():
    schema_file = './schema.json'  # Replace with the path to your schema.json file
    output_file = './erd_diagram.md'  # Replace with the desired output file path
    
    # Load the schema.json file
    with open(schema_file, 'r') as file:
        schema = json.load(file)
    
    tables = extract_tables_from_schema(schema)
    # Extract relationships
    relationships = extract_relationships(schema)

    # Check for the --tables-only flag
    if '--tables-only' in sys.argv:
        erd = generate_mermaid_erd_tables_only(tables)
    else:
        erd = generate_mermaid_erd(tables, relationships)
    
    with open(output_file, 'w') as f:
        f.write(erd)

if __name__ == '__main__':
    main()