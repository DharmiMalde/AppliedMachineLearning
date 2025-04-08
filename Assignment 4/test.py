import os
import requests
import time

def test_docker():
    # Step 1: Build Docker image
    os.system('docker build -t flask-assignment3 .')

    # Step 2: Run Docker container
    os.system('docker run -d -p 5000:5000 --name flask_app flask-assignment3')

    # Wait for app to be up
    time.sleep(5)

    # Step 3: Send request
    url = 'http://localhost:5000/score'
    data = {"text": "sample text"}

    try:
        response = requests.post(url, json=data)
        print("Response:", response.text)
        assert response.status_code == 200
        assert "expected_response_part" in response.text  # Customize this line
    finally:
        # Step 4: Clean up container
        os.system('docker stop flask_app')
        os.system('docker rm flask_app')
        