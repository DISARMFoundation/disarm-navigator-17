import json
import os

os.chdir(r'C:\Users\steph\OneDrive\Documents\GitHub\disarm-navigator-17')

with open('nav-app/src/assets/DISARM.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Get all technique IDs
all_techniques = {}
for obj in data['objects']:
    if obj.get('type') == 'attack-pattern':
        ext_refs = obj.get('external_references', [])
        if ext_refs:
            tech_id = ext_refs[0].get('external_id')
            if tech_id:
                all_techniques[tech_id] = obj

# Check sub-techniques for missing parents
orphaned = []
for tech_id, obj in all_techniques.items():
    if obj.get('x_mitre_is_subtechnique', False):
        # Extract parent ID (e.g., T0014.002 -> T0014)
        if '.' in tech_id:
            parent_id = tech_id.split('.')[0]
            if parent_id not in all_techniques:
                orphaned.append(f"{tech_id} (parent {parent_id} not found)")

print(f"Orphaned sub-techniques: {len(orphaned)}")
if orphaned:
    print("\nFirst 10 orphaned:")
    for o in orphaned[:10]:
        print(f"  {o}")
