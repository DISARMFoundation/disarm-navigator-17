import json
import os

# Change to script directory
os.chdir(r'C:\Users\steph\OneDrive\Documents\GitHub\disarm-navigator-17')

# Read the DISARM.json file
with open('nav-app/src/assets/DISARM.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Counter for how many sub-techniques we fix
fixed_count = 0

# Iterate through all objects
for obj in data['objects']:
    # Check if this is a sub-technique (attack-pattern with x_mitre_is_subtechnique = true)
    if obj.get('type') == 'attack-pattern' and obj.get('x_mitre_is_subtechnique') == True:
        # If it has kill_chain_phases, remove it
        if 'kill_chain_phases' in obj:
            del obj['kill_chain_phases']
            fixed_count += 1
            # Get the technique ID for reporting
            tech_id = obj.get('external_references', [{}])[0].get('external_id', 'unknown')
            print(f"Removed kill_chain_phases from sub-technique: {tech_id}")

# Write the fixed data back
with open('nav-app/src/assets/DISARM.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"\nFixed {fixed_count} sub-techniques")
print("Updated nav-app/src/assets/DISARM.json")
