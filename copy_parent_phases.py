import json
import os

os.chdir(r'C:\Users\steph\OneDrive\Documents\GitHub\disarm-navigator-17')

with open('nav-app/src/assets/DISARM.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Build a map of all techniques by ID
all_techniques = {}
for obj in data['objects']:
    if obj.get('type') == 'attack-pattern':
        ext_refs = obj.get('external_references', [])
        if ext_refs:
            tech_id = ext_refs[0].get('external_id')
            if tech_id:
                all_techniques[tech_id] = obj

# For each sub-technique, copy parent's kill_chain_phases
fixed_count = 0
for tech_id, obj in all_techniques.items():
    if obj.get('x_mitre_is_subtechnique', False):
        # Extract parent ID (e.g., T0014.002 -> T0014)
        if '.' in tech_id:
            parent_id = tech_id.split('.')[0]
            parent = all_techniques.get(parent_id)
            if parent and 'kill_chain_phases' in parent:
                # Copy parent's kill_chain_phases to sub-technique
                obj['kill_chain_phases'] = parent['kill_chain_phases'].copy()
                fixed_count += 1
                print(f"Copied kill_chain_phases from {parent_id} to {tech_id}")

# Write back
with open('nav-app/src/assets/DISARM.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"\nCopied kill_chain_phases to {fixed_count} sub-techniques")
