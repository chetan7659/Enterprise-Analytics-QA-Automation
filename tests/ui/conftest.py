import subprocess
import time
import pytest
import requests

@pytest.fixture(scope="session", autouse=True)
def live_server():
    """Starts the FastAPI application in the background for UI tests."""
    # Start the server using the virtual environment's uvicorn
    process = subprocess.Popen(
        ["venv\\Scripts\\uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for the server to be ready
    for _ in range(30):
        try:
            response = requests.get("http://127.0.0.1:8000/")
            if response.status_code == 200:
                break
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
    else:
        process.terminate()
        process.wait()
        raise RuntimeError("Could not start live server for UI tests.")
    
    yield "http://127.0.0.1:8000"
    
    # Teardown: stop the server
    process.terminate()
    process.wait()
