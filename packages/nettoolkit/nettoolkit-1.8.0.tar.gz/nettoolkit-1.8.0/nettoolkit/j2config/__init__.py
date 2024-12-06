__doc__ = '''Package which helps simplifying text output generation from template.'''


from .j2 import PrepareConfig
from .read_conditions import get_variables, get_conditions, JinjaVarCheck
from .data_collect import ABSRegion


__all__ = [
	'PrepareConfig',
	'get_conditions', 'get_variables', 'JinjaVarCheck',
	'ABSRegion'
	
]

