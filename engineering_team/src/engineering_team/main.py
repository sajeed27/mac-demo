#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime

from engineering_team.crew import EngineeringTeam

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

requirements = """
A simple member management system MAC center for a managing member registration and member login and logout.
Member registration should include:
- Name
- Email
- Password
- Confirm Password
- Phone Number
- Address
- Gender
- Occupation
- Portfolio
- Interests
The system should allow users to create an account, register with the email and password.
The system should allow users to login with the email and password.
The system should allow users to logout.
The system should allow users to view their profile.
The System should have following clubs:
- Club 1: Launch PAD: This club is for members who want to launch their own startup.
- Club 2: AI Club: This club is for members who want to learn about AI.
- Club 3: Book Club: This club is for members who want to read and discuss books.
- Club 4: Cybersecurity Club: This club is for members who want to learn about cybersecurity.
- Club 5: Data Science Club: This club is for members who want to learn about data science.
- Club 6: Finance Club: This club is for members who want to learn about finance.
- Club 7: Marketing Club: This club is for members who want to learn about marketing.
- Club 8: Sales Club: This club is for members who want to learn about sales.
- Club 9: Entrepreneurship Club: This club is for members who want to learn about entrepreneurship.
- Club 10: Leadership Club: This club is for members who want to learn about leadership.
- Club 11: Innovation Club: This club is for members who want to learn about innovation.
- Club 12: Entrepreneurship Club: This club is for members who want to learn about entrepreneurship.
The system should allow users to edit their profile.
The system should allow users to delete their account.
The system should allow users to view the list of clubs offered by MAC.
The system should allow users to enroll in a club.
The System should allow members toselect to enroll in different club offered by MAC.
The system should allow users to enroll and deenroll from a club.
The system should allow users to view the list of clubs they are enrolled in.
The system should allow users to view the list of clubs they are not enrolled in.
The system should allow users to view the list of clubs they are interested in.
The system should allow users to view the list of clubs they are not interested in.
The system should allow users to view the list of clubs they are not interested in.
The system should calculate the total value of the user's portfolio, and the profit or loss from the initial deposit.

"""
module_name = "mac_center.py"
class_name = "MACCenter"


def run():
    """
    Run the research crew.
    """
    inputs = {
        'requirements': requirements,
        'module_name': module_name,
        'class_name': class_name
    }

    # Create and run the crew
    result = EngineeringTeam().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()