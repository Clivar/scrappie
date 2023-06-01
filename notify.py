from typing import List, Dict, Any, Literal, Optional
from dataclasses import dataclass

@dataclass
class Condition:
    type: str
    value: Any

def validate_conditions(conditions: List[Condition]):
    known_types = {'greater than', 'equals', 'less than'}
    for condition in conditions:
        if condition.type not in known_types:
            print(f"Unknown condition type: {condition.type}")
            return False
        if condition.type in {'greater than', 'less than'} and not isinstance(condition.value, (int, float)):
            print(f"For '{condition.type}' condition, value should be a number. Got: {condition.value}")
            return False
        elif condition.type == 'equals' and not isinstance(condition.value, (int, float, str)):
            print(f"For 'equals' condition, value should be a number or a string. Got: {condition.value}")
            return False
    return True

def check_condition(condition: Condition, result) -> bool:
    if condition.type == 'equals' and result != condition.value:
        print(f"Condition not met: {result} != {condition.value}")
        return False
    elif condition.type == 'greater_than' and result <= condition.value:
        print(f"Condition not met: {result} <= {condition.value}")
        return False
    elif condition.type == 'less_than' and result >= condition.value:
        print(f"Condition not met: {result} >= {condition.value}")
        return False
    return True

def notify(results, conditions):
    for result in results:
        for condition in conditions:
            if check_condition(condition, result):
                print(f"Condition met: {result}")

