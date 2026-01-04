class MACCenter:
    def __init__(self):
        self.users = []
        self.clubs = {
            "Launch PAD": "This club is for members who want to launch their own startup.",
            "AI Club": "This club is for members who want to learn about AI.",
            "Book Club": "This club is for members who want to read and discuss books.",
            "Cybersecurity Club": "This club is for members who want to learn about cybersecurity.",
            "Data Science Club": "This club is for members who want to learn about data science.",
            "Finance Club": "This club is for members who want to learn about finance.",
            "Marketing Club": "This club is for members who want to learn about marketing.",
            "Sales Club": "This club is for members who want to learn about sales.",
            "Entrepreneurship Club": "This club is for members who want to learn about entrepreneurship.",
            "Leadership Club": "This club is for members who want to learn about leadership.",
            "Innovation Club": "This club is for members who want to learn about innovation."
        }
        self.current_user = None

    def register_member(self, name, email, password, confirm_password, phone_number, address, gender, occupation, portfolio, interests):
        if password != confirm_password:
            return "Passwords do not match!"

        for user in self.users:
            if user['email'] == email:
                return "Email is already registered!"

        new_user = {
            "name": name,
            "email": email,
            "password": password,
            "phone_number": phone_number,
            "address": address,
            "gender": gender,
            "occupation": occupation,
            "portfolio": portfolio,
            "interests": interests,
            "enrolled_clubs": []
        }
        self.users.append(new_user)
        return "User registered successfully."

    def login(self, email, password):
        for user in self.users:
            if user['email'] == email and user['password'] == password:
                self.current_user = email
                return "Logged in successfully."
        return "Invalid email or password."

    def logout(self):
        self.current_user = None
        return "Logged out successfully."

    def view_profile(self):
        if self.current_user is None:
            return "No user is currently logged in."

        for user in self.users:
            if user['email'] == self.current_user:
                return user
        return "User not found."

    def edit_profile(self, **kwargs):
        if self.current_user is None:
            return "No user is currently logged in."

        for user in self.users:
            if user['email'] == self.current_user:
                user.update(kwargs)
                return "Profile updated successfully."
        return "User not found."

    def delete_account(self):
        if self.current_user is None:
            return "No user is currently logged in."

        for i, user in enumerate(self.users):
            if user['email'] == self.current_user:
                del self.users[i]
                self.current_user = None
                return "Account deleted successfully."
        return "User not found."

    def view_clubs(self):
        return self.clubs.keys()

    def enroll_in_club(self, club_name):
        if self.current_user is None:
            return "No user is currently logged in."

        if club_name not in self.clubs:
            return "Club does not exist."

        for user in self.users:
            if user['email'] == self.current_user:
                if club_name not in user['enrolled_clubs']:
                    user['enrolled_clubs'].append(club_name)
                    return f"Enrolled in {club_name}."
                else:
                    return f"Already enrolled in {club_name}."
        return "User not found."

    def deenroll_from_club(self, club_name):
        if self.current_user is None:
            return "No user is currently logged in."

        for user in self.users:
            if user['email'] == self.current_user:
                if club_name in user['enrolled_clubs']:
                    user['enrolled_clubs'].remove(club_name)
                    return f"De-enrolled from {club_name}."
                else:
                    return f"Not enrolled in {club_name}."
        return "User not found."

    def view_enrolled_clubs(self):
        if self.current_user is None:
            return "No user is currently logged in."

        for user in self.users:
            if user['email'] == self.current_user:
                return user['enrolled_clubs']
        return "User not found."

    def view_unenrolled_clubs(self):
        if self.current_user is None:
            return "No user is currently logged in."

        for user in self.users:
            if user['email'] == self.current_user:
                return [club for club in self.clubs if club not in user['enrolled_clubs']]
        return "User not found."

    def view_interested_clubs(self):
        if self.current_user is None:
            return "No user is currently logged in."

        for user in self.users:
            if user['email'] == self.current_user:
                return [club for club in user['interests'] if club in self.clubs]
        return "User not found."

    def view_not_interested_clubs(self):
        if self.current_user is None:
            return "No user is currently logged in."

        for user in self.users:
            if user['email'] == self.current_user:
                return [club for club in self.clubs if club not in user['interests']]
        return "User not found."

    def calculate_portfolio_value(self):
        if self.current_user is None:
            return "No user is currently logged in."

        for user in self.users:
            if user['email'] == self.current_user:
                portfolio = user['portfolio']
                initial_deposit = sum(portfolio.values())  # Assuming this as initial deposit
                current_value = sum([value + (0.1 * value) for value in portfolio.values()])  # Let's assume 10% increase for the example
                return {
                    "total_value": current_value,
                    "profit_loss": current_value - initial_deposit
                }
        return "User not found."

# Example usage
mac_center = MACCenter()
print(mac_center.register_member("John Doe", "john@example.com", "password123", "password123", "1234567890", "123 Main St", "Male", "Engineer", {"stocks": 1000}, ["AI Club", "Book Club"]))
print(mac_center.login("john@example.com", "password123"))
print(mac_center.view_profile())
print(mac_center.enroll_in_club("AI Club"))
print(mac_center.view_enrolled_clubs())
print(mac_center.calculate_portfolio_value())
print(mac_center.logout())
