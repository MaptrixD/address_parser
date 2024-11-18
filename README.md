Address Parser API
This project provides a RESTful API built with FastAPI to parse address strings into their respective components using Amazon Bedrock's large language models (LLMs).

Features
Parses a given address string into components:
POI Name
Street
Locality
Sublocality
City
State
Pincode
Category

Returns the parsed result in JSON format.
Utilizes Amazon Bedrock LLM for processing the input.
Prerequisites

Python: Python 3.10 or higher installed.
AWS Credentials: Ensure AWS credentials are set up to access Amazon Bedrock.
Dependencies: Install the required Python packages using the requirements.txt file.
Installation
1. Clone the Repository

git clone https://github.com/MaptrixD/address_parser.git
cd address_parser
2. Create and Activate a Virtual Environment

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies

pip install -r requirements.txt
Configuration
1. Update the AWS Region
Ensure the correct AWS region is specified in the REGION_NAME variable in the addressparserapi.py file:


REGION_NAME = 'ap-south-1'  # Update if required
2. Update the Model ID
Set the appropriate Amazon Bedrock model ID in the MODEL_ID variable:


MODEL_ID = 'meta.llama3-70b-instruct-v1:0'  # Update as needed
Running the API
To start the API server, run the following command:


uvicorn addressparserapi:app --host 0.0.0.0 --port 9005 --reload
The API will be accessible at: http://localhost:9005

Endpoints
1. Parse Address
URL: /parse-address/
Method: POST
Content-Type: application/json

Request Body

{
    "address_string": "123 Main Street, Downtown, New York, NY 10001"
}
Response

{
    "parsed_address": {
        "POI Name": "None",
        "Street": "123 Main Street",
        "Locality": "Downtown",
        "Sublocality": "None",
        "City": "New York",
        "State": "NY",
        "Pincode": "10001",
        "Category": "None"
    }
}
Error Handling
500 Internal Server Error: If the Bedrock model invocation fails or an unexpected error occurs, an error message will be returned in the response:
json
Copy code
{
    "detail": "Error invoking model: <error_message>"
}
Development
Hot Reload
To enable hot-reloading during development, use the --reload option:


uvicorn addressparserapi:app --host 0.0.0.0 --port 9005 --reload
Dependencies
Dependencies are managed through requirements.txt. Install them with:


pip install -r requirements.txt
