import subprocess
# Replace 'your_executable.exe' with the path to your executable file
executable_path = "C:/TVShosurRespush/TvsLmsReport/TvsDealerUpdate/TvsDealerUpdate.exe"
def run():
    try:
        # Run the executable
        subprocess.run(executable_path, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running the executable: {e}")
    except FileNotFoundError:
        print(f"Executable not found at {executable_path}")


