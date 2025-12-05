"""
SECOM MES Operators API Client (Async Version)

This module provides async Python functions to interact with the SECOM Manufacturing Execution System
Operators REST API endpoints. Each function is documented with Agent_card and A2A specifications
for use by AI agents in the Solace Agent Mesh framework.

API Base URL: http://localhost:8080/api/v1
Database: MariaDB 11.2

Note: All functions are async and must be called with await.
"""

import httpx
from typing import TypedDict, List, Optional, Any, Dict
from datetime import datetime


# ============================================================================
# Type Definitions (Schemas)
# ============================================================================

class Operator(TypedDict, total=False):
    """Operator entity schema"""
    operatorId: int
    operatorCode: str
    operatorName: str
    employeeNumber: str
    department: str
    hireDate: str  # date format: YYYY-MM-DD
    email: str
    status: str
    createdAt: str  # datetime format: ISO 8601
    updatedAt: str  # datetime format: ISO 8601


class ProductType(TypedDict, total=False):
    """Product Type entity schema"""
    productTypeId: int
    productCode: str
    productName: str
    productFamily: str
    targetYield: float
    specificationVersion: str
    createdAt: str


class Equipment(TypedDict, total=False):
    """Equipment entity schema"""
    equipmentId: int
    equipmentCode: str
    equipmentName: str
    equipmentType: str
    location: str
    manufacturer: str
    installDate: str  # date format: YYYY-MM-DD
    status: str
    createdAt: str
    updatedAt: str


class Shift(TypedDict, total=False):
    """Shift entity schema"""
    shiftId: int
    shiftCode: str
    shiftName: str
    startTime: str  # time format: HH:MM:SS
    endTime: str  # time format: HH:MM:SS
    description: str
    createdAt: str


class Lot(TypedDict, total=False):
    """Lot entity schema"""
    lotId: int
    lotNumber: str
    productType: ProductType
    equipment: Equipment
    operator: Operator
    shift: Shift
    productionStart: str  # datetime format: ISO 8601
    productionEnd: str  # datetime format: ISO 8601
    waferCount: int
    status: str
    createdAt: str
    updatedAt: str


# ============================================================================
# Configuration
# ============================================================================

# Default base URL for the API
DEFAULT_BASE_URL = "http://localhost:8080/api/v1"


# ============================================================================
# Helper Functions
# ============================================================================

async def _make_request(
    method: str,
    endpoint: str,
    base_url: str = DEFAULT_BASE_URL,
    json_data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    timeout: int = 30
) -> httpx.Response:
    """
    Internal async helper function to make HTTP requests.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint path
        base_url: Base URL of the API
        json_data: JSON payload for POST/PUT requests
        params: Query parameters
        timeout: Request timeout in seconds

    Returns:
        Response object

    Raises:
        httpx.HTTPStatusError: On request failure
    """
    url = f"{base_url}{endpoint}"

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.request(
            method=method,
            url=url,
            json=json_data,
            params=params,
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )
        response.raise_for_status()
        return response


# ============================================================================
# Operators API Functions
# ============================================================================

async def get_operator_by_id(operator_id: int, base_url: str = DEFAULT_BASE_URL) -> Operator:
    """
    Get operator by ID.

    Returns a single operator record by operator ID from the SECOM MES database.

    Agent_card:
    -----------
    skill_id: get_operator_by_id
    skill_name: Get Operator by ID
    description: Retrieves detailed information about a specific production operator
                 using their unique operator ID. Returns complete operator profile
                 including name, department, contact information, and employment details.
    capabilities:
      - Fetch individual operator records
      - Validate operator existence
      - Retrieve operator employment details

    A2A Spec:
    ---------
    input_schema:
      type: object
      required:
        - operator_id
      properties:
        operator_id:
          type: integer
          format: int32
          description: Unique identifier for the operator
          example: 1
        base_url:
          type: string
          description: Optional base URL for the API (default: http://localhost:8080/api/v1)
          example: "http://localhost:8080/api/v1"

    output_schema:
      type: object
      properties:
        operatorId:
          type: integer
          format: int32
          description: Unique operator identifier
        operatorCode:
          type: string
          description: Unique operator code
        operatorName:
          type: string
          description: Full name of the operator
        employeeNumber:
          type: string
          description: Employee number
        department:
          type: string
          description: Department name (e.g., Production, Quality, Maintenance)
        hireDate:
          type: string
          format: date
          description: Date operator was hired (YYYY-MM-DD)
        email:
          type: string
          description: Operator email address
        status:
          type: string
          description: Operator status (e.g., Active, Inactive)
        createdAt:
          type: string
          format: date-time
          description: Timestamp when record was created
        updatedAt:
          type: string
          format: date-time
          description: Timestamp when record was last updated

    error_responses:
      - status: 404
        description: Operator not found
      - status: 500
        description: Internal server error

    Args:
        operator_id: The unique identifier of the operator
        base_url: Base URL for the API (default: http://localhost:8080/api/v1)

    Returns:
        Operator dictionary containing operator details

    Raises:
        httpx.HTTPStatusError: If the API request fails

    Example:
        >>> operator = await get_operator_by_id(1)
        >>> print(operator['operatorName'])
        'John Smith'
    """
    response = await _make_request("GET", f"/operators/{operator_id}", base_url=base_url)
    return response.json()


async def get_all_operators(base_url: str = DEFAULT_BASE_URL) -> List[Operator]:
    """
    Get all operators.

    Returns a list of all production operators in the SECOM MES database.

    Agent_card:
    -----------
    skill_id: get_all_operators
    skill_name: Get All Operators
    description: Retrieves a complete list of all production operators in the system.
                 Returns comprehensive operator roster including all active and inactive
                 operators with their full details.
    capabilities:
      - List all operators in the system
      - Generate operator rosters
      - Perform operator analytics
      - Export operator data

    A2A Spec:
    ---------
    input_schema:
      type: object
      properties:
        base_url:
          type: string
          description: Optional base URL for the API (default: http://localhost:8080/api/v1)
          example: "http://localhost:8080/api/v1"

    output_schema:
      type: array
      items:
        type: object
        properties:
          operatorId:
            type: integer
            format: int32
            description: Unique operator identifier
          operatorCode:
            type: string
            description: Unique operator code
          operatorName:
            type: string
            description: Full name of the operator
          employeeNumber:
            type: string
            description: Employee number
          department:
            type: string
            description: Department name
          hireDate:
            type: string
            format: date
            description: Date operator was hired
          email:
            type: string
            description: Operator email address
          status:
            type: string
            description: Operator status
          createdAt:
            type: string
            format: date-time
            description: Record creation timestamp
          updatedAt:
            type: string
            format: date-time
            description: Record update timestamp

    error_responses:
      - status: 500
        description: Internal server error

    Args:
        base_url: Base URL for the API (default: http://localhost:8080/api/v1)

    Returns:
        List of Operator dictionaries

    Raises:
        httpx.HTTPStatusError: If the API request fails

    Example:
        >>> operators = await get_all_operators()
        >>> print(f"Total operators: {len(operators)}")
        Total operators: 25
    """
    response = await _make_request("GET", "/operators", base_url=base_url)
    return response.json()


async def get_operator_lots(operator_id: int, base_url: str = DEFAULT_BASE_URL) -> List[Lot]:
    """
    Get operator's lots.

    Returns all production lots processed by a specific operator. This includes
    complete lot information with related entities (product type, equipment, shift).

    Agent_card:
    -----------
    skill_id: get_operator_lots
    skill_name: Get Operator Production Lots
    description: Retrieves all production lots that were processed by a specific operator.
                 Returns complete lot information including product details, equipment used,
                 shift information, and production metrics. Useful for tracking operator
                 productivity, quality performance, and work history.
    capabilities:
      - Track operator production history
      - Analyze operator performance
      - Generate operator productivity reports
      - Audit operator work records
      - Calculate operator-specific quality metrics

    A2A Spec:
    ---------
    input_schema:
      type: object
      required:
        - operator_id
      properties:
        operator_id:
          type: integer
          format: int32
          description: Unique identifier for the operator
          example: 1
        base_url:
          type: string
          description: Optional base URL for the API (default: http://localhost:8080/api/v1)
          example: "http://localhost:8080/api/v1"

    output_schema:
      type: array
      items:
        type: object
        properties:
          lotId:
            type: integer
            format: int32
            description: Unique lot identifier
          lotNumber:
            type: string
            description: Lot number (e.g., LOT001)
          productType:
            type: object
            description: Product type information
            properties:
              productTypeId:
                type: integer
              productCode:
                type: string
              productName:
                type: string
              productFamily:
                type: string
              targetYield:
                type: number
              specificationVersion:
                type: string
          equipment:
            type: object
            description: Equipment information
            properties:
              equipmentId:
                type: integer
              equipmentCode:
                type: string
              equipmentName:
                type: string
              equipmentType:
                type: string
              location:
                type: string
              status:
                type: string
          operator:
            type: object
            description: Operator information
          shift:
            type: object
            description: Shift information
            properties:
              shiftId:
                type: integer
              shiftCode:
                type: string
              shiftName:
                type: string
          productionStart:
            type: string
            format: date-time
            description: Production start timestamp
          productionEnd:
            type: string
            format: date-time
            description: Production end timestamp
          waferCount:
            type: integer
            description: Number of wafers in lot
          status:
            type: string
            description: Lot status (e.g., Completed, In Progress)
          createdAt:
            type: string
            format: date-time
          updatedAt:
            type: string
            format: date-time

    error_responses:
      - status: 404
        description: Operator not found
      - status: 500
        description: Internal server error

    Args:
        operator_id: The unique identifier of the operator
        base_url: Base URL for the API (default: http://localhost:8080/api/v1)

    Returns:
        List of Lot dictionaries processed by the operator

    Raises:
        httpx.HTTPStatusError: If the API request fails

    Example:
        >>> lots = await get_operator_lots(1)
        >>> print(f"Operator processed {len(lots)} lots")
        Operator processed 45 lots
        >>> print(f"First lot: {lots[0]['lotNumber']}")
        First lot: LOT001
    """
    response = await _make_request("GET", f"/operators/{operator_id}/lots", base_url=base_url)
    return response.json()


async def get_operators_by_department(department: str, base_url: str = DEFAULT_BASE_URL) -> List[Operator]:
    """
    Get operators by department.

    Returns all operators working in a specific department. Useful for department-level
    resource management and reporting.

    Agent_card:
    -----------
    skill_id: get_operators_by_department
    skill_name: Get Operators by Department
    description: Retrieves all operators assigned to a specific department. Returns complete
                 operator profiles for all personnel in the specified department. Supports
                 department-level workforce planning, resource allocation, and organizational
                 reporting.
    capabilities:
      - Filter operators by department
      - Generate department rosters
      - Support workforce planning
      - Enable department-level analytics
      - Facilitate resource allocation

    A2A Spec:
    ---------
    input_schema:
      type: object
      required:
        - department
      properties:
        department:
          type: string
          description: Department name to filter by
          example: "Production"
          enum: ["Production", "Quality", "Maintenance", "Engineering"]
        base_url:
          type: string
          description: Optional base URL for the API (default: http://localhost:8080/api/v1)
          example: "http://localhost:8080/api/v1"

    output_schema:
      type: array
      items:
        type: object
        properties:
          operatorId:
            type: integer
            format: int32
            description: Unique operator identifier
          operatorCode:
            type: string
            description: Unique operator code
          operatorName:
            type: string
            description: Full name of the operator
          employeeNumber:
            type: string
            description: Employee number
          department:
            type: string
            description: Department name (matches input filter)
          hireDate:
            type: string
            format: date
            description: Date operator was hired
          email:
            type: string
            description: Operator email address
          status:
            type: string
            description: Operator status
          createdAt:
            type: string
            format: date-time
          updatedAt:
            type: string
            format: date-time

    error_responses:
      - status: 404
        description: Department not found or no operators in department
      - status: 500
        description: Internal server error

    Args:
        department: Name of the department to filter by
        base_url: Base URL for the API (default: http://localhost:8080/api/v1)

    Returns:
        List of Operator dictionaries in the specified department

    Raises:
        httpx.HTTPStatusError: If the API request fails

    Example:
        >>> prod_operators = await get_operators_by_department("Production")
        >>> print(f"Production department has {len(prod_operators)} operators")
        Production department has 12 operators
    """
    response = await _make_request("GET", f"/operators/department/{department}", base_url=base_url)
    return response.json()


async def get_operator_by_code(code: str, base_url: str = DEFAULT_BASE_URL) -> Operator:
    """
    Get operator by code.

    Returns operator information by their unique operator code. Operator codes are
    typically used as business identifiers for quick lookups.

    Agent_card:
    -----------
    skill_id: get_operator_by_code
    skill_name: Get Operator by Code
    description: Retrieves operator information using their unique operator code (business
                 identifier). Operator codes are human-readable identifiers used in daily
                 operations for quick operator lookup. Returns complete operator profile.
    capabilities:
      - Look up operators by business identifier
      - Support barcode/RFID scanning workflows
      - Enable quick operator verification
      - Facilitate operator authentication

    A2A Spec:
    ---------
    input_schema:
      type: object
      required:
        - code
      properties:
        code:
          type: string
          description: Unique operator code (business identifier)
          example: "OP001"
          pattern: "^OP\\d{3}$"
        base_url:
          type: string
          description: Optional base URL for the API (default: http://localhost:8080/api/v1)
          example: "http://localhost:8080/api/v1"

    output_schema:
      type: object
      properties:
        operatorId:
          type: integer
          format: int32
          description: Unique operator identifier
        operatorCode:
          type: string
          description: Unique operator code (matches input)
        operatorName:
          type: string
          description: Full name of the operator
        employeeNumber:
          type: string
          description: Employee number
        department:
          type: string
          description: Department name
        hireDate:
          type: string
          format: date
          description: Date operator was hired
        email:
          type: string
          description: Operator email address
        status:
          type: string
          description: Operator status
        createdAt:
          type: string
          format: date-time
          description: Record creation timestamp
        updatedAt:
          type: string
          format: date-time
          description: Record update timestamp

    error_responses:
      - status: 404
        description: Operator with specified code not found
      - status: 500
        description: Internal server error

    Args:
        code: The unique operator code
        base_url: Base URL for the API (default: http://localhost:8080/api/v1)

    Returns:
        Operator dictionary containing operator details

    Raises:
        httpx.HTTPStatusError: If the API request fails

    Example:
        >>> operator = await get_operator_by_code("OP001")
        >>> print(f"{operator['operatorName']} - {operator['department']}")
        John Smith - Production
    """
    response = await _make_request("GET", f"/operators/code/{code}", base_url=base_url)
    return response.json()


# ============================================================================
# Utility Functions for AI Agents
# ============================================================================

async def get_operator_summary(operator_id: int, base_url: str = DEFAULT_BASE_URL) -> Dict[str, Any]:
    """
    Get comprehensive operator summary including lots processed.

    This is a convenience function that combines operator details with their
    production history for AI agents needing complete context.

    Agent_card:
    -----------
    skill_id: get_operator_summary
    skill_name: Get Comprehensive Operator Summary
    description: Retrieves complete operator information including personal details,
                 employment information, and production history. Combines data from
                 multiple API endpoints to provide a comprehensive view of an operator's
                 profile and performance.
    capabilities:
      - Generate comprehensive operator profiles
      - Support operator performance analysis
      - Enable holistic operator assessment
      - Facilitate operator reporting

    A2A Spec:
    ---------
    input_schema:
      type: object
      required:
        - operator_id
      properties:
        operator_id:
          type: integer
          format: int32
          description: The unique identifier of the operator
          example: 1
        base_url:
          type: string
          description: Optional base URL for the API (default: http://localhost:8080/api/v1)
          example: "http://localhost:8080/api/v1"

    output_schema:
      type: object
      properties:
        operator:
          type: object
          description: Full operator details
          properties:
            operatorId:
              type: integer
              format: int32
              description: Unique operator identifier
            operatorCode:
              type: string
              description: Unique operator code
            operatorName:
              type: string
              description: Full name of the operator
            employeeNumber:
              type: string
              description: Employee number
            department:
              type: string
              description: Department name
            hireDate:
              type: string
              format: date
              description: Date operator was hired
            email:
              type: string
              description: Operator email address
            status:
              type: string
              description: Operator status
            createdAt:
              type: string
              format: date-time
              description: Record creation timestamp
            updatedAt:
              type: string
              format: date-time
              description: Record update timestamp
        lots:
          type: array
          description: List of lots processed by the operator
          items:
            type: object
            properties:
              lotId:
                type: integer
                format: int32
                description: Unique lot identifier
              lotNumber:
                type: string
                description: Lot number
              productType:
                type: object
                description: Product type information
              equipment:
                type: object
                description: Equipment used for the lot
              operator:
                type: object
                description: Operator who processed the lot
              shift:
                type: object
                description: Shift during which the lot was processed
              productionStart:
                type: string
                format: date-time
                description: Production start timestamp
              productionEnd:
                type: string
                format: date-time
                description: Production end timestamp
              waferCount:
                type: integer
                description: Number of wafers in the lot
              status:
                type: string
                description: Lot status
              createdAt:
                type: string
                format: date-time
                description: Record creation timestamp
              updatedAt:
                type: string
                format: date-time
                description: Record update timestamp
        total_lots:
          type: integer
          description: Total count of lots processed by the operator
        departments:
          type: array
          items:
            type: string
          description: List of departments (single-element array with operator's department)
        summary_generated_at:
          type: string
          format: date-time
          description: ISO 8601 timestamp when the summary was generated

    error_responses:
      - status: 404
        description: Operator with specified ID not found
      - status: 500
        description: Internal server error

    Args:
        operator_id: The unique identifier of the operator
        base_url: Base URL for the API

    Returns:
        Dictionary with operator details and lots processed

    Raises:
        httpx.HTTPStatusError: If the API request fails

    Example:
        >>> summary = await get_operator_summary(1)
        >>> print(f"{summary['operator']['operatorName']} processed {summary['total_lots']} lots")
    """
    operator = await get_operator_by_id(operator_id, base_url)
    lots = await get_operator_lots(operator_id, base_url)

    return {
        "operator": operator,
        "lots": lots,
        "total_lots": len(lots),
        "departments": [operator.get("department")],
        "summary_generated_at": datetime.now().isoformat()
    }


async def search_operators(
    department: Optional[str] = None,
    status: Optional[str] = None,
    base_url: str = DEFAULT_BASE_URL
) -> List[Operator]:
    """
    Search operators with optional filters.

    Client-side filtering helper for operators by department and/or status.
    For large datasets, prefer using dedicated API endpoints when available.

    Agent_card:
    -----------
    skill_id: search_operators
    skill_name: Search and Filter Operators
    description: Search operators with flexible filtering by department and status.
                 Provides client-side filtering for finding operators matching specific
                 criteria. Useful for ad-hoc queries and multi-criteria searches.
    capabilities:
      - Multi-criteria operator search
      - Flexible operator filtering
      - Support complex queries

    Args:
        department: Optional department filter
        status: Optional status filter (e.g., "Active", "Inactive")
        base_url: Base URL for the API

    Returns:
        Filtered list of operators

    Example:
        >>> active_production = await search_operators(department="Production", status="Active")
        >>> print(f"Found {len(active_production)} active production operators")
    """
    # Get base dataset
    if department:
        operators = await get_operators_by_department(department, base_url)
    else:
        operators = await get_all_operators(base_url)

    # Apply additional filters
    if status:
        operators = [op for op in operators if op.get("status") == status]

    return operators


# ============================================================================
# Error Handling Example
# ============================================================================

async def safe_get_operator(operator_id: int, base_url: str = DEFAULT_BASE_URL) -> Optional[Operator]:
    """
    Safely get operator by ID with error handling.

    Returns None if operator not found instead of raising an exception.
    Useful for AI agents that need graceful error handling.

    Args:
        operator_id: The unique identifier of the operator
        base_url: Base URL for the API

    Returns:
        Operator dictionary or None if not found or on error

    Example:
        >>> operator = await safe_get_operator(999)
        >>> if operator is None:
        ...     print("Operator not found")
    """
    try:
        return await get_operator_by_id(operator_id, base_url)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return None
        raise
    except httpx.HTTPError:
        return None


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    # Type definitions
    'Operator',
    'Lot',
    'ProductType',
    'Equipment',
    'Shift',

    # Core API functions (matching OpenAPI spec)
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
