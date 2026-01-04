#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime

from mycoder.crew import Coder

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

assignment = 'Write a python program to that will generate a random 50 number between 1 and 10000 and calculate the average, sum, and print max and minimu of the numbers'

def run():
    """
    Run the crew.
    """
    inputs = {
        'assignment': assignment,
    }
    
    result = Coder().crew().kickoff(inputs=inputs)
    print(result.raw)




