# Signavio.NEXT Challenge: Grammar Checker Backend

This project is a backend for a grammar checker that uses the Google Gemini API to identify and correct errors in a given text. The backend is built with Python and FastAPI, and it uses FastAPI's built-in 'BackgroundTasks' for asynchronous processing of long-running tasks.


## Features

- Grammar Checking: Identifies and corrects grammatical errors, spelling mistakes, and capitalization issues.
- Asynchronous Processing: Uses 'BackgroundTasks' to handle long-running requests without blocking the client.
- API Documentation: Automatically generated API documentation available at '/docs'.
- Error Handling: Handles errors from the LLM and other parts of the system.


## Design Choices

- FastAPI: A web framework for building APIs with Python based on standard Python type hints. It provides automatic data validation, serialization, and documentation.
- BackgroundTasks: FastAPI's built-in support for background tasks is a simple and effective way to handle long-running operations without the need for external dependencies like Celery and Redis.
- Google Gemini: A powerful, multimodal model from Google that provides a simple and effective API for a variety of tasks, including grammar correction.

## Evaluation

To evaluate the effectiveness and reliability of the grammar checker backend, the following approach can be used:

1. Accuracy Testing:
   - Prepare a curated dataset of sentences with known grammatical, spelling, and capitalization errors.
   - Submit these sentences to the API and compare the returned corrections and error types against the expected results.
   - Calculate metrics such as precision, recall, and F1-score for error detection and correction.

2. Performance Testing:
   - Measure the response time for grammar check requests, both for single and batch submissions.

3. Robustness and Error Handling:
   - Submit ambiguous input to verify that the system handles errors without any issue and returns informative error messages.

4. Usability:
   - Review the API documentation and test the endpoints using tools like Swagger UI (`/docs`) or Postman.
   - Ensure the asynchronous workflow (task submission and result retrieval) is intuitive for users.

5. Extensibility:
   - Assess how easily the backend can be adapted to support other LLMs or additional features (e.g., batch processing, persistent storage).


## Requirements (pip install)
fastapi
uvicorn[standard]
pydantic
pytest
requests
google-generativeai


## Setup and Installation

1. Clone the repository:
    git clone <repository-url>
    cd grammar-checker-backend

2. Add Gemini API Key in main.py or load it using dotenv while having the API key stored in a .env file

3. Create and activate a virtual environment:
    python -m venv venv
    venv\Scripts\activate

## Running the Application

**Start the FastAPI server**:
Open a terminal and run the following command to ensure you are using the Python interpreter from your virtual environment:
.\venv\Scripts\python -m uvicorn main:app --reload


The API will be available at `http://127.0.0.1:8000`.


## API Endpoints

-   'POST /check-grammar': Asynchronously starts a grammar check task and returns a task ID.
-   'GET /results/{task_id}': Retrieves the status and result of a grammar check task.

You can find detailed API documentation at `http://127.0.0.1:8000/docs`.


## Testing

To run the tests, use the following command:
pytest

## Challenges Faced and How I Overcame Them

During development, I explored using both Zephyr 7B (via Hugging Face) and OpenAI's GPT models as the backend LLM. I encountered several challenges:

- Zephyr 7B Model Access: Initially, I attempted to use Zephyr 7B through the Hugging Face Inference API. However, I received 500 Internal Server Errors because Zephyr 7B does not support public inference via the API. After reviewing the model documentation and Hugging Face forums, I confirmed that Zephyr 7B can only be used locally or via custom deployment, not through the hosted API.

- OpenAI API Quota Limits: When switching to OpenAI's GPT models, I ran into quota and usage limits on my API key, resulting in further 500 errors. This required me to review my OpenAI account plan and usage, and ultimately I decided to proceed with Google Gemini, which provided a more reliable and accessible API for this project.

These challenges required me to brush up on the latest LLM API offerings and their limitations. By carefully reading documentation and error messages, I was able to adapt my approach and select a model that fit the requirements and constraints of the coding

Additionally, while the integration with the LLM itself was straightforward, I found myself needing to brush up on the implementation details of RESTful API endpoints, specifically the differences and usage of POST and GET methods in FastAPI. Revisiting these concepts helped me ensure that the asynchronous workflow and result retrieval were implemented correctly and followed best practices.

## Future Improvements

- WebSocket Support: Implement WebSockets to provide real-time updates on the status of grammar check tasks.
- More Sophisticated Error Handling: Improve the error handling to provide more specific feedback when the LLM fails or returns an unexpected response.
- Evaluation Framework: Develop an evaluation framework to measure the accuracy and performance of the grammar checker. This could involve a curated dataset of texts with known errors and a set of metrics to track performance.
- Batch Processing: Allow users to submit multiple texts for grammar checking in a single request.
- Persistent Storage: Store the results of grammar checks in a database so they can be retrieved later.
