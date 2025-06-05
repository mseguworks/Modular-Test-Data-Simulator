import pandas as pd
import numexpr as ne

def apply_rules(data, rules):
    errors = []
    for rule in rules:
        try:
            condition = rule['condition']
            data[rule['name']] = ne.evaluate(condition, local_dict=data.to_dict('series'))
        except Exception as e:
            errors.append(f"Error applying rule {rule['name']}: {str(e)}")
    return data, errors
