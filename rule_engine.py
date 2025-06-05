import pandas as pd
import numexpr as ne

def apply_rules(df, rules, config):
    alerts = []
    for rule in rules:
        name = rule["name"]
        condition = rule["condition"]
        if name in config:
            condition = condition.replace(str(rule["configurable"]), str(config[name]))
        try:
            matched = ne.evaluate(condition, local_dict=df.to_dict(orient='series'))
            alerts.append(df[matched])
        except Exception as e:
            print(f"Error applying rule {name}: {e}")
    if alerts:
        return pd.concat(alerts)
    else:
        return pd.DataFrame()
