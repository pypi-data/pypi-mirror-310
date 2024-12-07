from typing import Dict
import requests
import json
import pubchempy as pcp
import re

def get_reaction_smiles(reaction_id: str, output_file: str = "compound_smiles.json") -> Dict[str, str]:
    """
    Get SMILES representation of reactants and products for a KEGG reaction
    
    Args:
        reaction_id: KEGG reaction ID (e.g., 'R00001')
        output_file: Path to output JSON file
    
    Returns:
        Dictionary containing compound IDs and their corresponding SMILES strings
    """
    compound_smiles = {}
    
    # Get reaction information and extract compound IDs
    try:
        response = requests.get(f"http://rest.kegg.jp/get/rn:{reaction_id}", timeout=10)
        response.raise_for_status()
        
        # Extract compound IDs from EQUATION line
        equation_line = next(line for line in response.text.split('\n') 
                           if line.startswith('EQUATION'))
        compounds = re.findall(r'(?:\d*\s*)?(C\d{5})', equation_line)
        
    except (requests.RequestException, StopIteration) as e:
        print(f"Error occurred while fetching reaction {reaction_id}: {e}")
        return compound_smiles

    # Get SMILES for each compound
    for compound_id in compounds:
        try:
            # Get PubChem ID
            conv_response = requests.get(
                f"http://rest.kegg.jp/conv/pubchem/cpd:{compound_id}",
                timeout=10
            )
            conv_response.raise_for_status()
            
            if not conv_response.text.strip():
                print(f"No conversion data found for compound {compound_id}")
                continue
                
            # Extract PubChem CID and get SMILES
            pubchem_id = conv_response.text.strip().split('\t')[1].split(':')[1]
            print(f"PubChem ID for compound {compound_id}: {pubchem_id}")
            
            pubchem_compounds = pcp.get_compounds(pubchem_id, 'cid')
            
            if pubchem_compounds:
                compound = pubchem_compounds[0]
                canonical_smiles = compound.canonical_smiles
                isomeric_smiles = compound.isomeric_smiles or compound.canonical_smiles
                compound_smiles[compound_id] = {
                    'canonical_smiles': canonical_smiles,
                    'isomeric_smiles': isomeric_smiles
                }
                # print(f"化合物 {compound_id} 的Canonical SMILES: {canonical_smiles}")
                # print(f"化合物 {compound_id} 的Isomeric SMILES: {isomeric_smiles}")
            else:
                print(f"No PubChem data found for compound {compound_id}")
                
        except Exception as e:
            print(f"Error occurred while processing compound {compound_id}: {e}")
            continue

    # Save results
    # Organize data as a list format
    formatted_compounds = []
    for compound_id, smiles_data in compound_smiles.items():
        try:
            # Get compound name
            name_response = requests.get(f"http://rest.kegg.jp/get/cpd:{compound_id}", timeout=10)
            name_response.raise_for_status()
            name = next(line.split()[1].replace(';', '') for line in name_response.text.split('\n') 
                       if line.startswith('NAME'))
        except:
            name = "Unknown"
            
        compound_data = {
            "name": name,
            "Kegg_id": compound_id,
            "gotenzymes smiles": smiles_data['canonical_smiles'],
            "Isomeric smiles": smiles_data['isomeric_smiles'],
            "Canonical smiles": smiles_data['canonical_smiles']
        }
        formatted_compounds.append(compound_data)
    
    with open(output_file, 'w') as f:
        json.dump(formatted_compounds, f, indent=2, ensure_ascii=False)
    return compound_smiles

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Get SMILES representation of reactants and products for a KEGG reaction')
    parser.add_argument('reaction_id', help='KEGG reaction ID')
    parser.add_argument('--output', '-o', default='compound_smiles.json',
                       help='Path to output JSON file (default: compound_smiles.json)')
    
    args = parser.parse_args()
    get_reaction_smiles(args.reaction_id, args.output)

    '''
    Usage examples:
    Example 1:
    In console, enter:
    python get_reaction_smiles.py R00382
    This will get SMILES representation for reaction R00382 and save to compound_smiles.json
    
    Example 2:
    In console, enter:
    python get_reaction_smiles.py R00001 --output compound_smiles.json
    This will get SMILES representation for reaction R00001 and save to compound_smiles.json
    '''

