"""
SECOM MES Operators API Client Package

This package provides Python functions to interact with the SECOM Manufacturing
Execution System (MES) Operators REST API. All functions are designed to be
called by AI agents with comprehensive documentation including Agent_card
specifications and A2A (Agent-to-Agent) input/output schemas.

Main Module: operators_api
"""

from .operators_api import (
    # Type definitions
    Operator,
    Lot,
    ProductType,
    Equipment,
    Shift,

    # Core API functions
    get_operator_by_id,
    get_all_operators,
    get_operator_lots,
    get_operators_by_department,
    get_operator_by_code,

    # Utility functions
    get_operator_summary,
    search_operators,
    safe_get_operator,

    # Configuration
    DEFAULT_BASE_URL,
)

__version__ = "1.0.0"

__all__ = [
    # Type definitions
    'Operator',
    'Lot',
    'ProductType',
    'Equipment',
    'Shift',

    # Core API functions
    'get_operator_by_id',
    'get_all_operators',
    'get_operator_lots',
    'get_operators_by_department',
    'get_operator_by_code',

    # Utility functions
    'get_operator_summary',
    'search_operators',
    'safe_get_operator',

    # Configuration
    'DEFAULT_BASE_URL',
]
