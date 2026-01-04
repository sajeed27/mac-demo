#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime

from ezregistration.crew import EngineeringTeam

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

requirements = """
A simple registration system for a event.
The website should be fully functional and should be able to handle good number of users.
The system home page should display events in a grid format. When user clicks on an event, they should be redirected to a page with the event details.
The event details page should display the event name, description, date, time, and location.
The event details page should have a form for users to register for the event.
The form should have the following fields: Name, Email, Phone Number.
The form should have a button to submit the form.
The form should be validated and the user should be redirected to a success page.
The success page should display a message saying "You are registered for the event".
Following are the events:
- Event 1: Event 1: This event is for members who want to learn about AI agentic programming.
- Event 2: Event 2: This event is for members who want to learn about leadership.
- Event 3: Event 3: This event is for members who want to learn about innovation.
- Event 4: Event 4: This event is for members who want to learn about entrepreneurship.
- Event 5: Event 5: This event is for members who want to learn about community building.
- Event 6: Event 6: This event is for members who want to learn about Metaverse.
The system should allow users to enter their name, email, and phone number and click a button to register for a event.
The system should display the list of events to the user registered for.
The system should allow users to delete their account.
The system should display report with the number of users registered for each event.

"""
module_name = "event_registration.py"
class_name = "EventRegistration"
example_output = """
"""

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