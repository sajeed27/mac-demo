from dataclasses import dataclass
from typing import Optional, List, Tuple, Dict
import re
from datetime import datetime


@dataclass
class Event:
    """A simple data class to represent an event."""
    id: int
    name: str
    description: str
    date: str  # format: YYYY-MM-DD
    time: str  # format: HH:MM
    location: str


@dataclass
class User:
    """A simple data class to represent a user registration."""
    id: int
    name: str
    email: str
    phone: str
    event_ids: List[int]  # List of event IDs the user is registered for


class EventRegistration:
    """
    A simple registration system for events.
    This class provides all functionality for event listing, user registration,
    account management, and reporting.
    """

    def __init__(self):
        """
        Initialize the EventRegistration system with sample events and empty user database.
        Creates 6 sample events as specified in requirements.
        """
        self.events: Dict[int, Event] = {}
        self.users: Dict[int, User] = {}
        self.next_event_id = 7  # starts after sample events
        self.next_user_id = 1

        # Create sample events
        sample_events = [
            (1, "Event 1: AI Agentic Programming Workshop",
             "This event is for members who want to learn about AI agentic programming.",
             "2024-06-15", "10:00", "Tech Hub Auditorium"),
            (2, "Event 2: Leadership Development Seminar",
             "This event is for members who want to learn about leadership.",
             "2024-06-20", "14:00", "Business Center Room 101"),
            (3, "Event 3: Innovation Workshop",
             "This event is for members who want to learn about innovation.",
             "2024-06-25", "11:00", "Innovation Lab"),
            (4, "Event 4: Entrepreneurship Bootcamp",
             "This event is for members who want to learn about entrepreneurship.",
             "2024-07-01", "09:00", "Startup Garage"),
            (5, "Event 5: Community Building Forum",
             "This event is for members who want to learn about community building.",
             "2024-07-05", "13:00", "Community Hall"),
            (6, "Event 6: Metaverse Exploration Session",
             "This event is for members who want to learn about Metaverse.",
             "2024-07-10", "15:00", "Virtual Reality Lab"),
        ]

        for event_id, name, description, date, time, location in sample_events:
            self.events[event_id] = Event(event_id, name, description, date, time, location)

    # 1. Event Management Methods

    def get_all_events(self) -> List[Event]:
        """
        Retrieve all events for display on home page.

        Returns:
            list[Event]: List of all Event objects, sorted by date
        """
        events_list = list(self.events.values())
        # Sort by date, then time
        events_list.sort(key=lambda e: (e.date, e.time))
        return events_list

    def get_event_by_id(self, event_id: int) -> Optional[Event]:
        """
        Get detailed information about a specific event.

        Args:
            event_id (int): ID of the event to retrieve

        Returns:
            Event | None: Event object if found, None otherwise
        """
        return self.events.get(event_id)

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
        # Validate date format
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")

        # Validate time format
        try:
            datetime.strptime(time, "%H:%M")
        except ValueError:
            raise ValueError("Invalid time format. Use HH:MM")

        event_id = self.next_event_id
        self.next_event_id += 1
        event = Event(event_id, name, description, date, time, location)
        self.events[event_id] = event
        return event

    # 2. User Registration Methods

    def validate_registration_data(self, name: str, email: str, phone: str) -> Tuple[bool, str]:
        """
        Validate user registration data.

        Args:
            name (str): User's full name
            email (str): User's email address
            phone (str): User's phone number

        Returns:
            tuple[bool, str]: Validation result and error message if invalid
        """
        # Check non-empty
        if not name or not name.strip():
            return False, "Name cannot be empty"
        if not email or not email.strip():
            return False, "Email cannot be empty"
        if not phone or not phone.strip():
            return False, "Phone cannot be empty"

        # Email validation: simple check for @ and .
        if "@" not in email or "." not in email:
            return False, "Invalid email format"

        # Phone validation: digits only, 10-15 characters
        phone_digits = re.sub(r'\D', '', phone)
        if len(phone_digits) < 10 or len(phone_digits) > 15:
            return False, "Phone number must be 10-15 digits"
        if not phone_digits.isdigit():
            return False, "Phone number must contain only digits"

        return True, ""

    def is_email_registered_for_event(self, email: str, event_id: int) -> bool:
        """
        Check if an email is already registered for a specific event.

        Args:
            email (str): Email address to check
            event_id (int): Event ID to check

        Returns:
            bool: True if email is registered for the event, False otherwise
        """
        for user in self.users.values():
            if user.email.lower() == email.lower() and event_id in user.event_ids:
                return True
        return False

    def register_user_for_event(self, event_id: int, name: str, email: str, phone: str) -> Tuple[bool, str, int]:
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
        """
        # Validate event exists
        if event_id not in self.events:
            return False, f"Event with ID {event_id} does not exist", -1

        # Validate registration data
        is_valid, error_msg = self.validate_registration_data(name, email, phone)
        if not is_valid:
            return False, error_msg, -1

        # Check if email already registered for this event
        if self.is_email_registered_for_event(email, event_id):
            return False, f"Email {email} is already registered for this event", -1

        # Find existing user by email or create new user
        user_id = self.find_user_by_email(email)
        if user_id is not None:
            # Existing user: add event to their registrations
            user = self.users[user_id]
            if event_id not in user.event_ids:
                user.event_ids.append(event_id)
            return True, f"Successfully registered for event", user_id
        else:
            # New user
            user_id = self.next_user_id
            self.next_user_id += 1
            new_user = User(user_id, name.strip(), email.strip(), phone.strip(), [event_id])
            self.users[user_id] = new_user
            return True, f"Successfully registered for event", user_id

    # 3. User Account Management Methods

    def find_user_by_email(self, email: str) -> Optional[int]:
        """
        Find user ID by email address.

        Args:
            email (str): Email address to search for

        Returns:
            int | None: User ID if found, None otherwise
        """
        for user_id, user in self.users.items():
            if user.email.lower() == email.lower():
                return user_id
        return None

    def get_user_registrations(self, user_id: int) -> Optional[List[Event]]:
        """
        Get all events a user is registered for.

        Args:
            user_id (int): ID of the user

        Returns:
            list[Event] | None: List of Event objects the user is registered for,
                               or None if user doesn't exist
        """
        if user_id not in self.users:
            return None

        user = self.users[user_id]
        events = []
        for event_id in user.event_ids:
            event = self.events.get(event_id)
            if event:
                events.append(event)
        # Sort by date
        events.sort(key=lambda e: (e.date, e.time))
        return events

    def delete_user_account(self, user_id: int) -> Tuple[bool, str]:
        """
        Delete a user account and all their registrations.

        Args:
            user_id (int): ID of the user to delete

        Returns:
            tuple[bool, str]: Success status and message
        """
        if user_id not in self.users:
            return False, f"User with ID {user_id} does not exist"

        del self.users[user_id]
        return True, f"User account {user_id} deleted successfully"

    # 4. Reporting Methods

    def get_registration_report(self) -> Dict[int, int]:
        """
        Generate a report of registrations per event.

        Returns:
            dict: Dictionary with event_id as keys and registration count as values
        """
        report = {event_id: 0 for event_id in self.events.keys()}
        for user in self.users.values():
            for event_id in user.event_ids:
                if event_id in report:
                    report[event_id] += 1
        return report

    def get_detailed_report(self) -> List[Dict]:
        """
        Generate a detailed report for display.

        Returns:
            list[dict]: List of dictionaries with event details and registration count
            Each dict contains:
                - event_id (int)
                - event_name (str)
                - registrations (int)
        """
        basic_report = self.get_registration_report()
        detailed = []
        for event_id, count in basic_report.items():
            event = self.events.get(event_id)
            if event:
                detailed.append({
                    "event_id": event_id,
                    "event_name": event.name,
                    "registrations": count
                })
        # Sort by event_id
        detailed.sort(key=lambda x: x["event_id"])
        return detailed

    # 5. Utility Methods

    def get_event_registrants(self, event_id: int) -> Optional[List[User]]:
        """
        Get all users registered for a specific event.

        Args:
            event_id (int): ID of the event

        Returns:
            list[User] | None: List of User objects registered for the event,
                              or None if event doesn't exist
        """
        if event_id not in self.events:
            return None

        registrants = []
        for user in self.users.values():
            if event_id in user.event_ids:
                registrants.append(user)
        return registrants