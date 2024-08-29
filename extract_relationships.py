import json

def extract_relationships_from_schema(schema_file):
    with open(schema_file, 'r') as f:
        schema = json.load(f)
    
    # Check if the schema is nested under 'data' or directly under '__schema'
    if '__schema' in schema:
        schema_data = schema['__schema']
    elif 'data' in schema and '__schema' in schema['data']:
        schema_data = schema['data']['__schema']
    else:
        raise KeyError("The schema does not contain a '__schema' key.")
    
    relationships = []

    for type_data in schema_data['types']:
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

def main():
    schema_file = './schema.json'  # Replace with the path to your schema.json file
    relationships = extract_relationships_from_schema(schema_file)
    
    for relationship in relationships:
        print(f"{relationship['from']} -> {relationship['to']} : {relationship['field']}")

if __name__ == '__main__':
    main()