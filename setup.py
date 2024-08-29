import json
import sys
from graphviz import Digraph

def extract_tables_from_schema(schema):
    tables = []

    for type_data in schema['types']:
        # Exclude system-generated types and specific keywords
        if (type_data['kind'] == 'OBJECT' and 
            not type_data['name'].startswith(('query_root', 'mutation_root', 'subscription_root', 'hasura_', '_')) and
            not any(keyword in type_data['name'] for keyword in ['mutation', 'max', 'min', 'aggregate', 'stddev', 'sum', 'var'])):
            columns = [field['name'] for field in type_data['fields']]
            tables.append({'name': type_data['name'], 'columns': columns})
    
    return tables

def extract_relationships_from_schema(schema):
    relationships = []

    for type_data in schema['types']:
        # Exclude system-generated types and specific keywords
        if (type_data['kind'] == 'OBJECT' and 
            not type_data['name'].startswith(('query_root', 'mutation_root', 'subscription_root', 'hasura_', '_')) and
            not any(keyword in type_data['name'] for keyword in ['mutation', 'max', 'min', 'aggregate', 'stddev', 'sum', 'var'])):
            
            for field in type_data['fields']:
                field_type = None
                if field['type'] is not None:
                    if field['type']['kind'] == 'OBJECT':
                        field_type = field['type']['name']
                    elif field['type']['ofType'] is not None:
                        field_type = field['type']['ofType']['name']
                
                if field_type and field_type != type_data['name']:
                    relationships.append({
                        'from': type_data['name'],
                        'to': field_type,
                        'field': field['name']
                    })
    
    return relationships

def generate_diagram(tables, relationships, output_file='schema_diagram'):
    dot = Digraph(comment='Database Schema')

    # Group tables into rows of 3
    for i in range(0, len(tables), 3):
        with dot.subgraph() as s:
            s.attr(rank='same')
            for table in tables[i:i+3]:
                print(f"Processing table: {table['name']}")
                table_label = f"{table['name']}|{{" + "|".join(table['columns']) + "}}"
                s.node(table['name'], label=table_label, shape='record')

    # Add relationships to the diagram
    # for relationship in relationships:
    #     dot.edge(relationship['from'], relationship['to'], label=relationship['field'])

    dot.render(output_file, format='png', cleanup=True)
    print(f"Diagram saved as {output_file}.png")

def main():
    if len(sys.argv) != 2:
        print("Usage: python setup.py <schema.json>")
        sys.exit(1)
    
    schema_file = sys.argv[1]
    
    with open(schema_file, 'r') as f:
        schema = json.load(f)
    
    if '__schema' in schema:
        schema_data = schema['__schema']
    elif 'data' in schema and '__schema' in schema['data']:
        schema_data = schema['data']['__schema']
    else:
        raise KeyError("The schema does not contain a '__schema' key.")
    
    tables = extract_tables_from_schema(schema_data)
    relationships = extract_relationships_from_schema(schema_data)
    generate_diagram(tables, relationships)

if __name__ == '__main__':
    main()