"""
BAZI elements analysis and relationships module.
"""
from typing import Dict, Tuple

def get_element_relationship(element1: str, element2: str) -> str:
    """
    Analyze the relationship between two elements based on BAZI principles.
    """
    relationships = {
        ('Wood', 'Wood'): 'Harmony - Similar energies support each other',
        ('Wood', 'Fire'): 'Productive - Wood feeds Fire',
        ('Wood', 'Earth'): 'Weakening - Wood depletes Earth',
        ('Wood', 'Metal'): 'Destructive - Metal chops Wood',
        ('Wood', 'Water'): 'Supportive - Water nourishes Wood',
        
        ('Fire', 'Wood'): 'Supported - Fire is fed by Wood',
        ('Fire', 'Fire'): 'Harmony - Similar energies support each other',
        ('Fire', 'Earth'): 'Productive - Fire creates Earth (ash)',
        ('Fire', 'Metal'): 'Weakening - Fire melts Metal',
        ('Fire', 'Water'): 'Destructive - Water extinguishes Fire',
        
        ('Earth', 'Wood'): 'Controlling - Earth contains Wood growth',
        ('Earth', 'Fire'): 'Supported - Earth is created by Fire',
        ('Earth', 'Earth'): 'Harmony - Similar energies support each other',
        ('Earth', 'Metal'): 'Productive - Earth contains Metal',
        ('Earth', 'Water'): 'Weakening - Water erodes Earth',
        
        ('Metal', 'Wood'): 'Productive - Metal tools help Wood growth',
        ('Metal', 'Fire'): 'Controlling - Metal conducts Fire',
        ('Metal', 'Earth'): 'Supported - Metal comes from Earth',
        ('Metal', 'Metal'): 'Harmony - Similar energies support each other',
        ('Metal', 'Water'): 'Productive - Metal holds Water',
        
        ('Water', 'Wood'): 'Productive - Water nourishes Wood',
        ('Water', 'Fire'): 'Controlling - Water controls Fire',
        ('Water', 'Earth'): 'Productive - Water nourishes Earth',
        ('Water', 'Metal'): 'Supported - Water is held by Metal',
        ('Water', 'Water'): 'Harmony - Similar energies support each other'
    }
    
    return relationships.get((element1, element2), 'Unknown relationship')

def get_element_properties() -> Dict[str, Dict[str, str]]:
    """
    Get properties and characteristics of each element.
    """
    return {
        'Wood': {
            'nature': 'Growing, expanding',
            'direction': 'East',
            'season': 'Spring',
            'color': 'Green',
            'characteristics': 'Flexibility, growth, development'
        },
        'Fire': {
            'nature': 'Rising, illuminating',
            'direction': 'South',
            'season': 'Summer',
            'color': 'Red',
            'characteristics': 'Energy, transformation, passion'
        },
        'Earth': {
            'nature': 'Stable, nurturing',
            'direction': 'Center',
            'season': 'Late Summer',
            'color': 'Yellow',
            'characteristics': 'Stability, nourishment, support'
        },
        'Metal': {
            'nature': 'Condensing, solidifying',
            'direction': 'West',
            'season': 'Autumn',
            'color': 'White',
            'characteristics': 'Clarity, precision, structure'
        },
        'Water': {
            'nature': 'Flowing, adaptable',
            'direction': 'North',
            'season': 'Winter',
            'color': 'Black',
            'characteristics': 'Wisdom, flexibility, communication'
        }
    }
