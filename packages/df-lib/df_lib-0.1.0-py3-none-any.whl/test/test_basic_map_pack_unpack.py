'''
This test:

1. Loads the sample JSON data
2. Performs a round-trip serialize/deserialize
3. Validates that the key structures are preserved
4. Does deep comparison of tile data, settlements, vendors, cargo and vehicles
5. Checks numeric values, strings and nested data structures
6. Verifies integrity of highlights/lowlights

The test ensures that the serialization format preserves all the important data and relationships in the map structure. Key areas tested include:

- Map dimensions and tile properties
- Settlement hierarchy and attributes 
- Vendor inventories and properties
- Cargo and vehicle details
- Special map markers (highlights/lowlights)

The deep comparison helps catch any data loss or corruption that might occur during serialization.
'''
# import pytest
import json
import os
from df_lib.map_struct import serialize_map, deserialize_map


def compare_none_is_0(a, b):
    assert (a == b) or (a is None and b is 0) or (a is 0 and b is None)


def test_map_roundtrip(test_map_json_1):
    # # Load the test data
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # json_path = os.path.join(current_dir, 'df_map_obj-trimmed.json')
    
    # with open(json_path) as f:
    #     test_data = json.load(f)

    test_data = test_map_json_1
    # Serialize the data
    serialized = serialize_map(test_data)
    assert isinstance(serialized, bytes)
    assert len(serialized) > 0

    # Deserialize back
    deserialized = deserialize_map(serialized)
    
    # Compare key structures
    assert 'tiles' in deserialized
    assert 'highlights' in deserialized
    assert 'lowlights' in deserialized
    
    # Verify dimensions match
    assert len(test_data['tiles']) == len(deserialized['tiles'])
    assert len(test_data['tiles'][0]) == len(deserialized['tiles'][0])

    # Deep compare a few key tiles with settlements
    for y, row in enumerate(test_data['tiles']):
        for x, tile in enumerate(row):
            deserial_tile = deserialized['tiles'][y][x]
            
            # Compare tile attributes
            assert tile['terrain_difficulty'] == deserial_tile['terrain_difficulty']
            assert tile['region'] == deserial_tile['region']
            assert tile['weather'] == deserial_tile['weather']
            assert tile['special'] == deserial_tile['special']
            assert len(tile['settlements']) == len(deserial_tile['settlements'])

            # Compare settlements if present
            for i, settlement in enumerate(tile['settlements']):
                deserial_settlement = deserial_tile['settlements'][i]
                
                # Check settlement attributes
                assert settlement['sett_id'] == deserial_settlement['sett_id']
                assert settlement['name'] == deserial_settlement['name']
                assert settlement['sett_type'] == deserial_settlement['sett_type']
                assert len(settlement['vendors']) == len(deserial_settlement['vendors'])

                # Compare vendors
                for j, vendor in enumerate(settlement['vendors']):
                    deserial_vendor = deserial_settlement['vendors'][j]
                    
                    assert vendor['vendor_id'] == deserial_vendor['vendor_id']
                    assert vendor['name'] == deserial_vendor['name']
                    assert vendor['money'] == deserial_vendor['money']
                    compare_none_is_0(vendor['fuel'], deserial_vendor['fuel'])
                    compare_none_is_0(vendor['water'], deserial_vendor['water'])
                    compare_none_is_0(vendor['food'], deserial_vendor['food'])
                    
                    # Compare inventory lengths
                    assert len(vendor['_cargo_inventory']) == len(deserial_vendor['_cargo_inventory'])
                    assert len(vendor['_vehicle_inventory']) == len(deserial_vendor['_vehicle_inventory'])
                    
                    # Compare first cargo item if present
                    if vendor['_cargo_inventory']:
                        cargo = vendor['_cargo_inventory'][0]
                        deserial_cargo = deserial_vendor['_cargo_inventory'][0]
                        
                        assert cargo['cargo_id'] == deserial_cargo['cargo_id']
                        assert cargo['name'] == deserial_cargo['name']
                        assert cargo['quantity'] == deserial_cargo['quantity']
                        assert cargo['base_price'] == deserial_cargo['base_price']
                    
                    # Compare first vehicle if present  
                    if vendor['_vehicle_inventory']:
                        vehicle = vendor['_vehicle_inventory'][0]  
                        deserial_vehicle = deserial_vendor['_vehicle_inventory'][0]
                        
                        assert vehicle['vehicle_id'] == deserial_vehicle['vehicle_id']
                        assert vehicle['name'] == deserial_vehicle['name']
                        assert vehicle['wear'] == deserial_vehicle['wear']
                        assert vehicle['base_value'] == deserial_vehicle['base_value']

    # Compare highlights/lowlights
    assert deserialized['highlights'] == test_data.get('highlights', [])
    assert deserialized['lowlights'] == test_data.get('lowlights', [])
