# Detailed Design for Event Registration System Module

## Module: `event_registration.py`

### Overview
This module implements a self-contained event registration system with in-memory data storage. It is designed to be used as a backend for a web application, providing all necessary functionality for event listing, user registration, account management, and reporting. The module is structured as a single Python class `EventRegistration` with supporting data classes.

### Data Classes

#### `Event`
A simple data class to represent an event.

**Attributes:**
- `id` (int): Unique identifier for the event
- `name` (str): Name of the event
- `description` (str): Detailed description of the event
- `date` (str): Date of the event (format: YYYY-MM-DD)
- `time` (str): Time of the event (format: HH:MM)
- `location` (str): Location where the event will be held

#### `User`
A simple data class to represent a user registration.

**Attributes:**
- `id` (int): Unique identifier for the user
- `name` (str): Full name of the user
- `email` (str): Email address of the user
- `phone` (str): Phone number of the user
- `event_ids` (list[int]): List of event IDs the user is registered for

### Main Class: `EventRegistration`

#### Initialization
```python
def __init__(self):
    """
    Initialize the EventRegistration system with sample events and empty user database.
    Creates 6 sample events as specified in requirements.
    """
```

**Initial Data:**
- `self.events`: Dictionary mapping event_id → Event object
- `self.users`: Dictionary mapping user_id → User object
- `self.next_event_id`: Counter for generating new event IDs (starts at 7)
- `self.next_user_id`: Counter for generating new user IDs (starts at 1)

**Sample Events Created:**
1. Event 1: AI Agentic Programming Workshop
   - Date: 2024-06-15, Time: 10:00, Location: Tech Hub Auditorium
2. Event 2: Leadership Development Seminar
   - Date: 2024-06-20, Time: 14:00, Location: Business Center Room 101
3. Event 3: Innovation Workshop
   - Date: 2024-06-25, Time: 11:00, Location: Innovation Lab
4. Event 4: Entrepreneurship Bootcamp
   - Date: 2024-07-01, Time: 09:00, Location: Startup Garage
5. Event 5: Community Building Forum
   - Date: 2024-07-05, Time: 13:00, Location: Community Hall
6. Event 6: Metaverse Exploration Session
   - Date: 2024-07-10, Time: 15:00, Location: Virtual Reality Lab

#### Core Methods

##### 1. Event Management Methods

```python
def get_all_events(self) -> list[Event]:
    """
    Retrieve all events for display on home page.
    
    Returns:
        list[Event]: List of all Event objects, sorted by date
    """
```

```python
def get_event_by_id(self, event_id: int) -> Event | None:
    """
    Get detailed information about a specific event.
    
    Args:
        event_id (int): ID of the event to retrieve
        
    Returns:
        Event | None: Event object if found, None otherwise
    """
```

```python
def create_event(self, name: str, description: str, date: str, time: str, location: str) -> Event:
    """
    Create a new event (for system extensibility).
    
    Args:
        name (str): Event name
        description (str): Event description
        date (str): Event date (YYYY-MM-DD)
        time (str): Event time (HH:MM)
        location (str): Event location
        
    Returns:
        Event: The newly created Event object
        
    Raises:
        ValueError: If date or time format is invalid
    """
```

##### 2. User Registration Methods

```python
def register_user_for_event(self, event_id: int, name: str, email: str, phone: str) -> tuple[bool, str, int]:
    """
    Register a user for an event with validation.
    
    Args:
        event_id (int): ID of the event to register for
        name (str): User's full name
        email (str): User's email address
        phone (str): User's phone number
        
    Returns:
        tuple[bool, str, int]: 
            - bool: Success status (True/False)
            - str: Message describing the result
            - int: User ID if registration successful, -1 otherwise
            
    Validation Rules:
        - All fields must be non-empty
        - Email must contain '@' and '.'
        - Phone must contain only digits and be 10-15 characters
        - Event must exist
        - Email must not already be registered for this event
    """
```

```python
def validate_registration_data(self, name: str, email: str, phone: str) -> tuple[bool, str]:
    """
    Validate user registration data.
    
    Args:
        name (str): User's full name
        email (str): User's email address
        phone (str): User's phone number
        
    Returns:
        tuple[bool, str]: Validation result and error message if invalid
    """
```

##### 3. User Account Management Methods

```python
def get_user_registrations(self, user_id: int) -> list[Event] | None:
    """
    Get all events a user is registered for.
    
    Args:
        user_id (int): ID of the user
        
    Returns:
        list[Event] | None: List of Event objects the user is registered for,
                           or None if user doesn't exist
    """
```

```python
def delete_user_account(self, user_id: int) -> tuple[bool, str]:
    """
    Delete a user account and all their registrations.
    
    Args:
        user_id (int): ID of the user to delete
        
    Returns:
        tuple[bool, str]: Success status and message
    """
```

```python
def find_user_by_email(self, email: str) -> int | None:
    """
    Find user ID by email address.
    
    Args:
        email (str): Email address to search for
        
    Returns:
        int | None: User ID if found, None otherwise
    """
```

##### 4. Reporting Methods

```python
def get_registration_report(self) -> dict:
    """
    Generate a report of registrations per event.
    
    Returns:
        dict: Dictionary with event_id as keys and registration count as values
    """
```

```python
def get_detailed_report(self) -> list[dict]:
    """
    Generate a detailed report for display.
    
    Returns:
        list[dict]: List of dictionaries with event details and registration count
        Each dict contains:
            - event_id (int)
            - event_name (str)
            - registrations (int)
    """
```

##### 5. Utility Methods

```python
def get_event_registrants(self, event_id: int) -> list[User] | None:
    """
    Get all users registered for a specific event.
    
    Args:
        event_id (int): ID of the event
        
    Returns:
        list[User] | None: List of User objects registered for the event,
                          or None if event doesn't exist
    """
```

```python
def is_email_registered_for_event(self, email: str, event_id: int) -> bool:
    """
    Check if an email is already registered for a specific event.
    
    Args:
        email (str): Email address to check
        event_id (int): Event ID to check
        
    Returns:
        bool: True if email is registered for the event, False otherwise
    """
```

### Error Handling
The module includes comprehensive error handling:
- Invalid input validation with descriptive error messages
- Graceful handling of non-existent events/users
- Type checking for all method parameters
- Consistent return patterns (success boolean + message)

### Data Persistence Strategy
While this implementation uses in-memory storage for simplicity, the design allows for easy migration to a database by:
1. Replacing dictionary storage with database calls
2. Maintaining the same method signatures
3. Adding database connection management

### Testing Considerations
The module is designed to be easily testable:
- All methods return predictable types
- No side effects except on internal data structures
- Clear separation of concerns
- Validation logic is isolated in dedicated methods

### Usage Example
```python
# Initialize the system
system = EventRegistration()

# Get all events for home page
events = system.get_all_events()

# Register a user for event 1
success, message, user_id = system.register_user_for_event(
    event_id=1,
    name="John Doe",
    email="john@example.com",
    phone="1234567890"
)

# Get user's registered events
user_events = system.get_user_registrations(user_id)

# Generate registration report
report = system.get_detailed_report()

# Delete user account
success, message = system.delete_user_account(user_id)
```

This design provides a complete, self-contained backend system that can be easily integrated with any web framework (Flask, Django, FastAPI) by creating appropriate view functions that call these methods and return JSON responses or render templates.