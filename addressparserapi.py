import boto3
import json
import re
from fastapi import FastAPI, HTTPException  
from pydantic import BaseModel
import uvicorn
# Set your region and model ID
REGION_NAME = 'ap-south-1'
#MODEL_ID = 'meta.llama3-8b-instruct-v1:0'  # Update with your model ID
MODEL_ID = 'meta.llama3-70b-instruct-v1:0'

client = boto3.client('bedrock-runtime', region_name=REGION_NAME)

# FastAPI app instance
app = FastAPI()

# Input model for address data
class AddressInput(BaseModel):
    address_string: str

# Function to invoke Bedrock model
def invoke_model(client, model_id, address_string):
    prompt = f"""
    Task: Parse the following address string into the specified components. Provide the output strictly in JSON format with keys for each component.

    Components to output:
    - POI Name
    - Street
    - Locality
    - Sublocality
    - City
    - State
    - Pincode
    - Category

    Address string: "{address_string}"

    Ensure that if a component is not present, the value should be "None".
    Do not include any additional explanations or code. Just provide the JSON output.

    Output format example: {{ "POI Name": "value", "Street": "value", "Locality": "value", "Sublocality": "value", "City": "value", "State": "value", "Pincode": "value", "Category": "value" }}
    """

    max_gen_len = 512
    temperature = 0.5
    top_p = 0.9

    try:
        # Call the model
        response = client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "prompt": prompt,
                "max_gen_len": max_gen_len,
                "temperature": temperature,
                "top_p": top_p
            })
        )

        if 'body' in response:
            response_body = response['body']

            # If the response body is a byte stream, decode it
            if hasattr(response_body, 'read'):
                result = json.loads(response_body.read().decode('utf-8'))
            else:
                result = json.loads(response_body)

            generation_output = result['generation']

            if isinstance(generation_output, str):
                try:
                    parsed_output = json.loads(generation_output)
                    return parsed_output
                except json.JSONDecodeError:
                    # Fallback to regex parsing if the output is not valid JSON
                    pattern = r'"([^"]+)":\s*"([^"]*)"'
                    matches = re.findall(pattern, generation_output)
                    result_dict = {key: value for key, value in matches}
                    return result_dict
            else:
                return generation_output
        else:
            raise HTTPException(status_code=500, detail="No body found in the response")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error invoking model: {str(e)}")

# FastAPI endpoint
@app.post("/parse-address/")
async def parse_address(address_input: AddressInput):
    address_string = address_input.address_string
    try:
        parsed_result = invoke_model(client, MODEL_ID, address_string)
        return {"parsed_address": parsed_result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


if __name__ == "__main__":
    # Run the app with uvicorn
    uvicorn.run("addressparserapi:app", host="0.0.0.0", port=9005, reload=True)
