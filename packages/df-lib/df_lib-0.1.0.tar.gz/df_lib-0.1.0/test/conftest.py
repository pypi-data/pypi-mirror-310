# SPDX-FileCopyrightText: 2023-present Oori Data <info@oori.dev>
# SPDX-License-Identifier: Apache-2.0
# test/conftest.py
'''
Fixtures/setup/teardown for DF_Lib tests

General note: After setup as described in the README.md for this directory, run the tests with:

pytest test
'''

import pytest
# import pytest_asyncio


@pytest.fixture
def test_map_json_1():
    '''
3x3 map sample with:
- Valid x,y coordinate sequences
- One settlement (Seattle) with two vendors
- One vendor with cargo inventory (water drums)
- One vendor with vehicle inventory (Ram 1500)
- One highlighted tile at Seattle's location
- Representative values for all required fields
- Proper nesting of all data structures
    '''
    return TEST_MAP_JSON_1


TEST_MAP_JSON_1 = {
    "tiles": [
        [
            {
                "x": 0,
                "y": 0,
                "terrain_difficulty": 0,
                "region": 0,
                "weather": 0,
                "special": 0,
                "settlements": []
            },
            {
                "x": 1,
                "y": 0,
                "terrain_difficulty": 1,
                "region": 0,
                "weather": 0,
                "special": 0,
                "settlements": []
            },
            {
                "x": 2,
                "y": 0,
                "terrain_difficulty": 2,
                "region": 120,
                "weather": 0,
                "special": 0,
                "settlements": []
            }
        ],
        [
            {
                "x": 0,
                "y": 1,
                "terrain_difficulty": 1,
                "region": 0,
                "weather": 0,
                "special": 0,
                "settlements": []
            },
            {
                "x": 1,
                "y": 1,
                "terrain_difficulty": 2,
                "region": 120,
                "weather": 0,
                "special": 0,
                "settlements": [
                    {
                        "sett_id": "00000000-0000-0000-0000-000000000042",
                        "name": "Seattle",
                        "sett_type": "dome",
                        "vendors": [
                            {
                                "vendor_id": "26e100eb-53bc-4575-8920-21fb8ac62780",
                                "name": "Seattle Water Plant",
                                "money": 1000,
                                "fuel": None,
                                "fuel_price": None,
                                "water": 2000,
                                "water_price": 6,
                                "food": None,
                                "food_price": None,
                                "_cargo_inventory": [
                                    {
                                        "cargo_id": "38e7a44b-5474-4c8d-977e-1d3b2e262e82",
                                        "name": "Water Drums",
                                        "quantity": 12,
                                        "volume": 278,
                                        "weight": 18,
                                        "capacity": 208.0,
                                        "fuel": None,
                                        "water": 2496.0,
                                        "food": None,
                                        "base_price": 300,
                                        "delivery_reward": None,
                                        "distributor": None,
                                        "vehicle_id": None,
                                        "warehouse_id": None,
                                        "vendor_id": "26e100eb-53bc-4575-8920-21fb8ac62780",
                                        "base_desc": "A 55 gallon drum of water."
                                    }
                                ],
                                "_vehicle_inventory": [],
                                "repair_price": None
                            },
                            {
                                "vendor_id": "000eb341-e0d3-49b1-afb4-12a280d25580",
                                "name": "Seattle Vehicles",
                                "money": 1000,
                                "fuel": None,
                                "fuel_price": None,
                                "water": None,
                                "water_price": None,
                                "food": None,
                                "food_price": None,
                                "_cargo_inventory": [],
                                "_vehicle_inventory": [
                                    {
                                        "vehicle_id": "306a2233-27c1-43df-858c-f018369a2d0b",
                                        "name": "Ram 1500",
                                        "wear": 30.0,
                                        "base_fuel_efficiency": 35,
                                        "base_top_speed": 45,
                                        "base_offroad_capability": 25,
                                        "base_cargo_capacity": 0,
                                        "base_weight_capacity": 1053,
                                        "base_towing_capacity": 3175,
                                        "ap": 19,
                                        "base_max_ap": 20,
                                        "base_value": 17000,
                                        "vendor_id": "000eb341-e0d3-49b1-afb4-12a280d25580",
                                        "warehouse_id": None,
                                        "base_desc": "2021 Ram 1500 crew cab"
                                    }
                                ],
                                "repair_price": 30
                            }
                        ]
                    }
                ]
            },
            {
                "x": 2,
                "y": 1,
                "terrain_difficulty": 3,
                "region": 120,
                "weather": 0,
                "special": 0,
                "settlements": []
            }
        ],
        [
            {
                "x": 0,
                "y": 2,
                "terrain_difficulty": 2,
                "region": 121,
                "weather": 0,
                "special": 0,
                "settlements": []
            },
            {
                "x": 1,
                "y": 2,
                "terrain_difficulty": 3,
                "region": 121,
                "weather": 0,
                "special": 0,
                "settlements": []
            },
            {
                "x": 2,
                "y": 2,
                "terrain_difficulty": 4,
                "region": 121,
                "weather": 0,
                "special": 0,
                "settlements": []
            }
        ]
    ],
    "highlights": [[1, 1]],
    "lowlights": []
}
