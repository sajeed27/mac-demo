# Detailed Design for MAC Center Member Management System

## Module: `mac_center.py`

### Overview
This module implements a simple member management system for MAC Center. It includes functionality for member registration, login, logout, profile management, club enrollment, and portfolio tracking. The system is designed to be self-contained, using in-memory data structures for simplicity, but can be extended to use a database.

### Classes

#### 1. `Member`
A data class to represent a member with all required attributes.

**Attributes:**
- `name` (str): Full name of the member.
- `email` (str): Unique email address used for login.
- `password` (str): Hashed password for security.
- `phone_number` (str): Contact phone number.
- `address` (str): Physical address.
- `gender` (str): Gender (e.g., Male, Female, Other).
- `occupation` (str): Current occupation.
- `portfolio` (dict): A dictionary representing the member's portfolio. Structure: `{"initial_deposit": float, "current_value": float, "holdings": dict}` where `holdings` maps asset names to quantities.
- `interests` (list of str): List of interests (e.g., ["AI", "Finance"]).
- `enrolled_clubs` (list of str): List of club IDs the member is enrolled in.
- `interested_clubs` (list of str): List of club IDs the member is interested in.

**Methods:**
- `__init__(self, name, email, password, phone_number, address, gender, occupation, portfolio, interests)`: Initializes a member with given attributes. Sets `enrolled_clubs` and `interested_clubs` to empty lists.
- `update_profile(self, **kwargs)`: Updates member attributes based on keyword arguments (e.g., name, phone_number). Validates inputs.
- `calculate_portfolio_summary(self)`: Calculates total portfolio value and profit/loss. Returns a tuple `(total_value, profit_loss)`.

#### 2. `Club`
A data class to represent a club offered by MAC Center.

**Attributes:**
- `club_id` (str): Unique identifier for the club (e.g., "club_1").
- `name` (str): Club name (e.g., "Launch PAD").
- `description` (str): Brief description of the club.

**Methods:**
- `__init__(self, club_id, name, description)`: Initializes a club with given attributes.

#### 3. `MACCenter`
The main class that manages the system, including members, clubs, and operations.

**Attributes:**
- `members` (dict): Maps email (str) to `Member` objects for all registered members.
- `clubs` (dict): Maps club_id (str) to `Club` objects for all available clubs.
- `logged_in_user` (str or None): Email of the currently logged-in user, or `None` if no user is logged in.

**Methods:**

**Initialization and Setup:**
- `__init__(self)`: Initializes the system with empty members dict, sets `logged_in_user` to `None`, and pre-populates the clubs with the 12 specified clubs.

**Authentication:**
- `register(self, name, email, password, confirm_password, phone_number, address, gender, occupation, portfolio, interests)`: Registers a new member. Validates that email is unique, passwords match, and all fields are provided. Hashes the password before storing. Returns `True` on success, `False` on failure.
- `login(self, email, password)`: Logs in a member by verifying email and password. Sets `logged_in_user` to the email if successful. Returns `True` on success, `False` on failure.
- `logout(self)`: Logs out the current user by setting `logged_in_user` to `None`. Returns `True` if a user was logged in, `False` otherwise.

**Profile Management:**
- `view_profile(self)`: Returns the profile of the logged-in user as a dictionary. If no user is logged in, returns `None`.
- `edit_profile(self, **kwargs)`: Updates the profile of the logged-in user with provided keyword arguments (e.g., name, phone_number). Validates inputs. Returns `True` on success, `False` on failure.
- `delete_account(self, password)`: Deletes the account of the logged-in user after confirming password. Removes the member from the system and logs out. Returns `True` on success, `False` on failure.

**Club Management:**
- `list_all_clubs(self)`: Returns a list of all clubs as dictionaries.
- `enroll_in_club(self, club_id)`: Enrolls the logged-in user in a club by adding `club_id` to their `enrolled_clubs` list. Validates that the club exists and the user is not already enrolled. Returns `True` on success, `False` on failure.
- `deenroll_from_club(self, club_id)`: Removes the logged-in user from a club by removing `club_id` from their `enrolled_clubs` list. Validates that the club exists and the user is enrolled. Returns `True` on success, `False` on failure.
- `list_enrolled_clubs(self)`: Returns a list of clubs the logged-in user is enrolled in as dictionaries.
- `list_not_enrolled_clubs(self)`: Returns a list of clubs the logged-in user is not enrolled in as dictionaries.
- `add_interest_in_club(self, club_id)`: Adds a club to the logged-in user's `interested_clubs` list. Validates that the club exists and the user is not already interested. Returns `True` on success, `False` on failure.
- `remove_interest_in_club(self, club_id)`: Removes a club from the logged-in user's `interested_clubs` list. Validates that the club exists and the user is interested. Returns `True` on success, `False` on failure.
- `list_interested_clubs(self)`: Returns a list of clubs the logged-in user is interested in as dictionaries.
- `list_not_interested_clubs(self)`: Returns a list of clubs the logged-in user is not interested in as dictionaries.

**Portfolio Calculation:**
- `calculate_portfolio_summary(self)`: Calculates and returns the portfolio summary for the logged-in user: total current value and profit/loss from initial deposit. Returns a dictionary `{"total_value": float, "profit_loss": float}` or `None` if no user is logged in.

**Helper Methods:**
- `_hash_password(self, password)`: Hashes a password using a secure method (e.g., SHA-256 with salt). Returns the hashed string.
- `_verify_password(self, hashed_password, password)`: Verifies a password against its hash. Returns `True` if they match.
- `_validate_email(self, email)`: Validates email format and uniqueness. Returns `True` if valid.
- `_validate_portfolio(self, portfolio)`: Validates portfolio structure. Returns `True` if valid.
- `_get_club_by_id(self, club_id)`: Returns a `Club` object by ID, or `None` if not found.

### Data Structures
- **Members:** Stored in a dictionary `self.members` with email as key and `Member` object as value.
- **Clubs:** Stored in a dictionary `self.clubs` with club_id as key and `Club` object as value. Pre-defined with 12 clubs as per requirements.
- **Logged-in User:** Tracked via `self.logged_in_user` (email string or `None`).

### Error Handling
- Methods return `False` or `None` on failure (e.g., invalid input, user not logged in).
- Input validation is performed for all user-provided data (e.g., email format, password strength).
- Security: Passwords are hashed before storage; plain text passwords are never stored.

### Example Usage
```python
mac = MACCenter()
mac.register("John Doe", "john@example.com", "pass123", "pass123", "1234567890", "123 Main St", "Male", "Engineer", {"initial_deposit": 1000.0, "current_value": 1200.0, "holdings": {"Stock A": 10}}, ["AI", "Finance"])
mac.login("john@example.com", "pass123")
mac.enroll_in_club("club_2")  # AI Club
summary = mac.calculate_portfolio_summary()
print(summary)  # {"total_value": 1200.0, "profit_loss": 200.0}
```

This design ensures all requirements are met in a single, self-contained Python module ready for implementation and testing.