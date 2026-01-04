import unittest
from engineering_team.output.mac_center1 import MACCenter

class TestMACCenter(unittest.TestCase):
    def setUp(self):
        self.mac_center = MACCenter()
        self.default_user = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
            "confirm_password": "password123",
            "phone_number": "1234567890",
            "address": "123 Main St",
            "gender": "Male",
            "occupation": "Engineer",
            "portfolio": {"stocks": 1000},
            "interests": ["AI Club", "Book Club"]
        }

    def test_register_member_success(self):
        result = self.mac_center.register_member(**self.default_user)
        self.assertEqual(result, "User registered successfully.")

    def test_register_member_password_mismatch(self):
        self.default_user["confirm_password"] = "wrongpassword"
        result = self.mac_center.register_member(**self.default_user)
        self.assertEqual(result, "Passwords do not match!")

    def test_register_member_email_already_registered(self):
        self.mac_center.register_member(**self.default_user)
        result = self.mac_center.register_member(**self.default_user)
        self.assertEqual(result, "Email is already registered!")

    def test_login_successful(self):
        self.mac_center.register_member(**self.default_user)
        result = self.mac_center.login(self.default_user["email"], self.default_user["password"])
        self.assertEqual(result, "Logged in successfully.")

    def test_login_invalid_email_or_password(self):
        result = self.mac_center.login("wrong@example.com", "password123")
        self.assertEqual(result, "Invalid email or password.")

    def test_logout_successful(self):
        self.mac_center.register_member(**self.default_user)
        self.mac_center.login(self.default_user["email"], self.default_user["password"])
        result = self.mac_center.logout()
        self.assertEqual(result, "Logged out successfully.")

    def test_view_profile(self):
        self.mac_center.register_member(**self.default_user)
        self.mac_center.login(self.default_user["email"], self.default_user["password"])
        profile = self.mac_center.view_profile()
        self.assertEqual(profile["email"], self.default_user["email"])

    def test_view_profile_no_login(self):
        result = self.mac_center.view_profile()
        self.assertEqual(result, "No user is currently logged in.")

    def test_edit_profile(self):
        self.mac_center.register_member(**self.default_user)
        self.mac_center.login(self.default_user["email"], self.default_user["password"])
        new_data = {"name": "Jane Doe", "address": "456 Other St"}
        result = self.mac_center.edit_profile(**new_data)
        self.assertEqual(result, "Profile updated successfully.")
        profile = self.mac_center.view_profile()
        self.assertEqual(profile["name"], "Jane Doe")
        self.assertEqual(profile["address"], "456 Other St")

    def test_delete_account(self):
        self.mac_center.register_member(**self.default_user)
        self.mac_center.login(self.default_user["email"], self.default_user["password"])
        result = self.mac_center.delete_account()
        self.assertEqual(result, "Account deleted successfully.")
        result = self.mac_center.view_profile()
        self.assertEqual(result, "No user is currently logged in.")

    def test_view_clubs(self):
        expected_clubs = set(self.mac_center.clubs.keys())
        self.assertEqual(set(self.mac_center.view_clubs()), expected_clubs)

    def test_enroll_in_club(self):
        self.mac_center.register_member(**self.default_user)
        self.mac_center.login(self.default_user["email"], self.default_user["password"])
        result = self.mac_center.enroll_in_club("AI Club")
        self.assertEqual(result, "Already enrolled in AI Club.")
        result = self.mac_center.enroll_in_club("Innovation Club")
        self.assertEqual(result, "Enrolled in Innovation Club.")

    def test_deenroll_from_club(self):
        self.mac_center.register_member(**self.default_user)
        self.mac_center.login(self.default_user["email"], self.default_user["password"])
        result = self.mac_center.deenroll_from_club("AI Club")
        self.assertEqual(result, "De-enrolled from AI Club.")
        result = self.mac_center.deenroll_from_club("Fashion Club")
        self.assertEqual(result, "Not enrolled in Fashion Club.")

    def test_view_enrolled_clubs(self):
        self.mac_center.register_member(**self.default_user)
        self.mac_center.login(self.default_user["email"], self.default_user["password"])
        self.mac_center.enroll_in_club("Innovation Club")
        enrolled_clubs = self.mac_center.view_enrolled_clubs()
        self.assertIn("AI Club", enrolled_clubs)
        self.assertIn("Innovation Club", enrolled_clubs)

    def test_view_unenrolled_clubs(self):
        self.mac_center.register_member(**self.default_user)
        self.mac_center.login(self.default_user["email"], self.default_user["password"])
        unordered_clubs = set(self.mac_center.view_unenrolled_clubs())
        expected_clubs = set(self.mac_center.clubs.keys()) - {"AI Club", "Book Club"}
        self.assertEqual(unordered_clubs, expected_clubs)

    def test_calculate_portfolio_value(self):
        self.mac_center.register_member(**self.default_user)
        self.mac_center.login(self.default_user["email"], self.default_user["password"])
        portfolio_value = self.mac_center.calculate_portfolio_value()
        self.assertAlmostEqual(portfolio_value["total_value"], 1100.0)
        self.assertAlmostEqual(portfolio_value["profit_loss"], 100.0)

if __name__ == "__main__":
    unittest.main()
