import hashlib
import json
from typing import Optional, Dict, List, Tuple, Any


class Member:
    """A class to represent a member."""
    def __init__(self, name: str, email: str, password: str, phone_number: str, address: str,
                 gender: str, occupation: str, portfolio: dict, interests: list):
        self.name = name
        self.email = email
        self.password = password  # already hashed
        self.phone_number = phone_number
        self.address = address
        self.gender = gender
        self.occupation = occupation
        self.portfolio = portfolio
        self.interests = interests
        self.enrolled_clubs: List[str] = []
        self.interested_clubs: List[str] = []

    def update_profile(self, **kwargs) -> bool:
        """Update member attributes."""
        allowed = {'name', 'phone_number', 'address', 'gender', 'occupation', 'portfolio', 'interests'}
        for key, value in kwargs.items():
            if key in allowed:
                setattr(self, key, value)
            else:
                return False
        return True

    def calculate_portfolio_summary(self) -> Tuple[float, float]:
        """Calculate total value and profit/loss."""
        total_value = self.portfolio.get('current_value', 0.0)
        initial = self.portfolio.get('initial_deposit', 0.0)
        profit_loss = total_value - initial
        return total_value, profit_loss


class Club:
    """A class to represent a club."""
    def __init__(self, club_id: str, name: str, description: str):
        self.club_id = club_id
        self.name = name
        self.description = description

    def to_dict(self) -> dict:
        return {
            'club_id': self.club_id,
            'name': self.name,
            'description': self.description
        }


class MACCenter:
    """Main class for MAC Center member management system."""
    def __init__(self):
        self.members: Dict[str, Member] = {}
        self.clubs: Dict[str, Club] = {}
        self.logged_in_user: Optional[str] = None
        self._initialize_clubs()

    def _initialize_clubs(self):
        """Pre-populate the 12 clubs."""
        clubs_data = [
            ("club_1", "Launch PAD", "This club is for members who want to launch their own startup."),
            ("club_2", "AI Club", "This club is for members who want to learn about AI."),
            ("club_3", "Book Club", "This club is for members who want to read and discuss books."),
            ("club_4", "Cybersecurity Club", "This club is for members who want to learn about cybersecurity."),
            ("club_5", "Data Science Club", "This club is for members who want to learn about data science."),
            ("club_6", "Finance Club", "This club is for members who want to learn about finance."),
            ("club_7", "Marketing Club", "This club is for members who want to learn about marketing."),
            ("club_8", "Sales Club", "This club is for members who want to learn about sales."),
            ("club_9", "Entrepreneurship Club", "This club is for members who want to learn about entrepreneurship."),
            ("club_10", "Leadership Club", "This club is for members who want to learn about leadership."),
            ("club_11", "Innovation Club", "This club is for members who want to learn about innovation."),
            ("club_12", "Entrepreneurship Club", "This club is for members who want to learn about entrepreneurship."),
        ]
        for club_id, name, description in clubs_data:
            self.clubs[club_id] = Club(club_id, name, description)

    def _hash_password(self, password: str) -> str:
        """Hash a password using SHA-256 with a simple salt."""
        salt = "mac_center_salt"
        return hashlib.sha256((password + salt).encode()).hexdigest()

    def _verify_password(self, hashed_password: str, password: str) -> bool:
        """Verify a password against its hash."""
        return hashed_password == self._hash_password(password)

    def _validate_email(self, email: str) -> bool:
        """Validate email format and uniqueness."""
        if '@' not in email or '.' not in email:
            return False
        if email in self.members:
            return False
        return True

    def _validate_portfolio(self, portfolio: dict) -> bool:
        """Validate portfolio structure."""
        required = {'initial_deposit', 'current_value', 'holdings'}
        if not isinstance(portfolio, dict):
            return False
        if not all(key in portfolio for key in required):
            return False
        if not isinstance(portfolio['initial_deposit'], (int, float)):
            return False
        if not isinstance(portfolio['current_value'], (int, float)):
            return False
        if not isinstance(portfolio['holdings'], dict):
            return False
        return True

    def _get_club_by_id(self, club_id: str) -> Optional[Club]:
        """Return Club object by ID."""
        return self.clubs.get(club_id)

    def register(self, name: str, email: str, password: str, confirm_password: str,
                 phone_number: str, address: str, gender: str, occupation: str,
                 portfolio: dict, interests: list) -> bool:
        """Register a new member."""
        if not all([name, email, password, confirm_password, phone_number, address, gender, occupation]):
            return False
        if password != confirm_password:
            return False
        if not self._validate_email(email):
            return False
        if not self._validate_portfolio(portfolio):
            return False
        hashed_pw = self._hash_password(password)
        new_member = Member(name, email, hashed_pw, phone_number, address, gender, occupation, portfolio, interests)
        self.members[email] = new_member
        return True

    def login(self, email: str, password: str) -> bool:
        """Log in a member."""
        if email not in self.members:
            return False
        member = self.members[email]
        if self._verify_password(member.password, password):
            self.logged_in_user = email
            return True
        return False

    def logout(self) -> bool:
        """Log out the current user."""
        if self.logged_in_user is None:
            return False
        self.logged_in_user = None
        return True

    def view_profile(self) -> Optional[dict]:
        """Return the profile of the logged-in user."""
        if self.logged_in_user is None:
            return None
        member = self.members[self.logged_in_user]
        return {
            'name': member.name,
            'email': member.email,
            'phone_number': member.phone_number,
            'address': member.address,
            'gender': member.gender,
            'occupation': member.occupation,
            'portfolio': member.portfolio,
            'interests': member.interests,
            'enrolled_clubs': member.enrolled_clubs,
            'interested_clubs': member.interested_clubs
        }

    def edit_profile(self, **kwargs) -> bool:
        """Update the profile of the logged-in user."""
        if self.logged_in_user is None:
            return False
        member = self.members[self.logged_in_user]
        # Prevent editing email and password via this method
        if 'email' in kwargs or 'password' in kwargs:
            return False
        if 'portfolio' in kwargs and not self._validate_portfolio(kwargs['portfolio']):
            return False
        return member.update_profile(**kwargs)

    def delete_account(self, password: str) -> bool:
        """Delete the account of the logged-in user."""
        if self.logged_in_user is None:
            return False
        member = self.members[self.logged_in_user]
        if not self._verify_password(member.password, password):
            return False
        del self.members[self.logged_in_user]
        self.logged_in_user = None
        return True

    def list_all_clubs(self) -> List[dict]:
        """Return a list of all clubs."""
        return [club.to_dict() for club in self.clubs.values()]

    def enroll_in_club(self, club_id: str) -> bool:
        """Enroll the logged-in user in a club."""
        if self.logged_in_user is None:
            return False
        club = self._get_club_by_id(club_id)
        if club is None:
            return False
        member = self.members[self.logged_in_user]
        if club_id in member.enrolled_clubs:
            return False
        member.enrolled_clubs.append(club_id)
        return True

    def deenroll_from_club(self, club_id: str) -> bool:
        """Remove the logged-in user from a club."""
        if self.logged_in_user is None:
            return False
        club = self._get_club_by_id(club_id)
        if club is None:
            return False
        member = self.members[self.logged_in_user]
        if club_id not in member.enrolled_clubs:
            return False
        member.enrolled_clubs.remove(club_id)
        return True

    def list_enrolled_clubs(self) -> Optional[List[dict]]:
        """Return clubs the logged-in user is enrolled in."""
        if self.logged_in_user is None:
            return None
        member = self.members[self.logged_in_user]
        enrolled = []
        for club_id in member.enrolled_clubs:
            club = self._get_club_by_id(club_id)
            if club:
                enrolled.append(club.to_dict())
        return enrolled

    def list_not_enrolled_clubs(self) -> Optional[List[dict]]:
        """Return clubs the logged-in user is not enrolled in."""
        if self.logged_in_user is None:
            return None
        member = self.members[self.logged_in_user]
        not_enrolled = []
        for club_id, club in self.clubs.items():
            if club_id not in member.enrolled_clubs:
                not_enrolled.append(club.to_dict())
        return not_enrolled

    def add_interest_in_club(self, club_id: str) -> bool:
        """Add a club to the logged-in user's interested clubs."""
        if self.logged_in_user is None:
            return False
        club = self._get_club_by_id(club_id)
        if club is None:
            return False
        member = self.members[self.logged_in_user]
        if club_id in member.interested_clubs:
            return False
        member.interested_clubs.append(club_id)
        return True

    def remove_interest_in_club(self, club_id: str) -> bool:
        """Remove a club from the logged-in user's interested clubs."""
        if self.logged_in_user is None:
            return False
        club = self._get_club_by_id(club_id)
        if club is None:
            return False
        member = self.members[self.logged_in_user]
        if club_id not in member.interested_clubs:
            return False
        member.interested_clubs.remove(club_id)
        return True

    def list_interested_clubs(self) -> Optional[List[dict]]:
        """Return clubs the logged-in user is interested in."""
        if self.logged_in_user is None:
            return None
        member = self.members[self.logged_in_user]
        interested = []
        for club_id in member.interested_clubs:
            club = self._get_club_by_id(club_id)
            if club:
                interested.append(club.to_dict())
        return interested

    def list_not_interested_clubs(self) -> Optional[List[dict]]:
        """Return clubs the logged-in user is not interested in."""
        if self.logged_in_user is None:
            return None
        member = self.members[self.logged_in_user]
        not_interested = []
        for club_id, club in self.clubs.items():
            if club_id not in member.interested_clubs:
                not_interested.append(club.to_dict())
        return not_interested

    def calculate_portfolio_summary(self) -> Optional[dict]:
        """Calculate portfolio summary for the logged-in user."""
        if self.logged_in_user is None:
            return None
        member = self.members[self.logged_in_user]
        total_value, profit_loss = member.calculate_portfolio_summary()
        return {
            'total_value': total_value,
            'profit_loss': profit_loss
        }


# Example usage and testing
if __name__ == "__main__":
    print("Testing MACCenter module...")
    mac = MACCenter()
    # Register a member
    portfolio = {
        'initial_deposit': 1000.0,
        'current_value': 1200.0,
        'holdings': {"Stock A": 10}
    }
    success = mac.register(
        name="John Doe",
        email="john@example.com",
        password="pass123",
        confirm_password="pass123",
        phone_number="1234567890",
        address="123 Main St",
        gender="Male",
        occupation="Engineer",
        portfolio=portfolio,
        interests=["AI", "Finance"]
    )
    print(f"Registration successful: {success}")
    # Login
    login_success = mac.login("john@example.com", "pass123")
    print(f"Login successful: {login_success}")
    # View profile
    profile = mac.view_profile()
    print(f"Profile: {profile}")
    # Enroll in a club
    mac.enroll_in_club("club_2")
    # List enrolled clubs
    enrolled = mac.list_enrolled_clubs()
    print(f"Enrolled clubs: {enrolled}")
    # Portfolio summary
    summary = mac.calculate_portfolio_summary()
    print(f"Portfolio summary: {summary}")
    # Logout
    mac.logout()
    print("Test completed.")