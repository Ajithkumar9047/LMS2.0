import subprocess
from Config import *
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

executable_path = os.getenv("Executable_path")
def run():
    try:
        # Run the executable
        subprocess.run(executable_path, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running the executable: {e}")
    except FileNotFoundError:
        print(f"Executable not found at {executable_path}")


