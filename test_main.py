from fastapi.testclient import TestClient
from main import app
import time

# Test client that can make requests to API without having to run a server.
client = TestClient(app)

def test_check_grammar_and_get_results():
    # Testing the whole asynchronous process.
    
    # 1. Request to start a grammar check.
    response = client.post("/check-grammar", json={"text": "this is a test"})

    assert response.status_code == 202

    assert "task_id" in response.json()
    task_id = response.json()["task_id"]

    # 2. Giving the background task time to finish.

    time.sleep(15)

    # 3. Sending a request to get the results using the task_id.
    response = client.get(f"/results/{task_id}")
    
    assert response.status_code == 200
    json_response = response.json()
    
    # The status of the task should be either "SUCCESS" or "FAILED".
    assert json_response["status"] in ["SUCCESS", "FAILED"]
    
    # If the task was successful, I check that the result has the correct structure.
    if json_response["status"] == "SUCCESS":
        assert "result" in json_response
        assert "errors" in json_response["result"]
    # If it failed, I check if there's an error message.
    else:
        assert "error" in json_response