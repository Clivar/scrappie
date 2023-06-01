from typing import List, Dict, Any, Literal, Optional
from dataclasses import dataclass

@dataclass
class Condition:
    type: str
    value: Any

def validate_conditions(conditions: List[Condition]):
    known_types = {'greater_than', 'equals', 'less_than'}
    for condition in conditions:
        if condition.type not in known_types:
            print(f"Unknown condition type: {condition.type}")
            return False
        if condition.type in {'greater_than', 'less_than'} and not isinstance(condition.value, (int, float)):
            print(f"For '{condition.type}' condition, value should be a number. Got: {condition.value}")
            return False
        elif condition.type == 'equals' and not isinstance(condition.value, (int, float, str)):
            print(f"For 'equals' condition, value should be a number or a string. Got: {condition.value}")
            return False
    return True

def check_condition(condition: Condition, result) -> bool:
    if condition.type == 'equals' and result.match != condition.value:
        return False
    elif condition.type == 'greater_than' and float(result.match) <= condition.value:
        return False
    elif condition.type == 'less_than' and float(result.match) >= condition.value:
        return False
    return True

def notify(result, conditions):
    for condition in conditions:
        if check_condition(condition, result):
            if condition.type == "equals":
                print(f"Condition met: Result {result.order}'s match '{result.match}' equals the expected value '{condition.value}'")
            elif condition.type == "greater_than":
                print(f"Condition met: Result {result.order}'s match '{result.match}' is greater than the expected value '{condition.value}'")
            elif condition.type == "less_than":
                print(f"Condition met: Result {result.order}'s match '{result.match}' is less than the expected value '{condition.value}'")

