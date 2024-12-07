from is_subset import is_subset
input_data = {
    "user_id": "12345",  # String
    "age": 30,  # Integer
    "height": 5.9,  # Float
    "is_active": True,  # Boolean
    "email": "john.doe@example.com",  # String
    "address": {
        "street": "123 Elm St",  # String
        "city": "Metropolis",  # String
        "zipcode": 12345  # Integer
    },
    "preferences": {
        "notifications": True,  # Boolean
        "newsletter_subscription": False,  # Boolean
        "theme": "dark"  # String
    },
    "salary": 85000.50,  # Float
    "activity_log": [
        {"date": "2024-11-01", "action": "login", "status": "success"},  # Dict
        {"date": "2024-11-05", "action": "purchase", "status": "success", "item": "Laptop"}  # Dict
    ]
}

# Test for nested dictionary matching
def test_is_subset_nested_dict():
    predicate = {"address": {"city": "Metropolis"}}
    assert is_subset(input_data, predicate) is True

def test_is_subset_nested_dict_not_match():
    predicate = {"address": {"city": "Gotham"}}
    assert is_subset(input_data, predicate) is False

# Test for boolean nested dictionary matching
def test_is_subset_nested_dict_bool():
    predicate = {"preferences": {"notifications": True}}
    assert is_subset(input_data, predicate) is True

def test_is_subset_nested_dict_bool_not_match():
    predicate = {"preferences": {"notifications": False}}
    assert is_subset(input_data, predicate) is False

# Test for dictionary with `__is` condition (Exact match)
def test_is_subset_is_condition():
    predicate = {"user_id": {"__is": "12345"}}
    assert is_subset(input_data, predicate) is True

def test_is_subset_is_condition_not_match():
    predicate = {"user_id": {"__is": "67890"}}
    assert is_subset(input_data, predicate) is False

# Test for dictionary with `__not` condition (Not equal match)
def test_is_subset_not_condition():
    predicate = {"user_id": {"__not": "67890"}}
    assert is_subset(input_data, predicate) is True

def test_is_subset_not_condition_not_match():
    predicate = {"user_id": {"__not": "12345"}}
    assert is_subset(input_data, predicate) is False

# Test for dictionary with `__in` condition (Value in list)
def test_is_subset_in_condition():
    predicate = {"age": {"__in": [25, 30]}}
    assert is_subset(input_data, predicate) is True

def test_is_subset_in_condition_not_match():
    predicate = {"age": {"__in": [40, 50]}}
    assert is_subset(input_data, predicate) is False

# Test for dictionary with `__matches` condition (Regex match)
def test_is_subset_matches_condition():
    predicate = {"email": {"__matches": r".*example\.com$"}}
    assert is_subset(input_data, predicate) is True

def test_is_subset_matches_condition_not_match():
    predicate = {"email": {"__matches": r".*gmail\.com$"}}
    assert is_subset(input_data, predicate) is False

# Test for dictionary with `__not_matches` condition (Negative regex match)
def test_is_subset_not_matches_condition():
    predicate = {"email": {"__not_matches": r".*gmail\.com$"}}
    assert is_subset(input_data, predicate) is True

def test_is_subset_not_matches_condition_not_match():
    predicate = {"email": {"__not_matches": r".*example\.com$"}}
    assert is_subset(input_data, predicate) is False

# Test for dictionary with `__is` in a nested dictionary
def test_is_subset_nested_is_condition():
    predicate = {"address": {"city": {"__is": "Metropolis"}}}
    assert is_subset(input_data, predicate) is True

def test_is_subset_nested_is_condition_not_match():
    predicate = {"address": {"city": {"__is": "Gotham"}}}
    assert is_subset(input_data, predicate) is False