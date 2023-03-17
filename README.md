# API for Pandas Profiling Report and Uploading to Eueno
This code provides an API for generating a Pandas Profiling Report from a CSV file and uploading the report and its corresponding torrent file to Eueno. The API uses FastAPI as a web framework and pandas_profiling to generate the report.

### Endpoints
##### GET /profiling
Returns a simple string 'profiling' as a response.

##### POST /profiling
Generates a Pandas Profiling Report from a CSV file and uploads it and its corresponding torrent file to Eueno.

###### Request Body
The endpoint expects a file in the body of the request. The file should be a CSV file.

###### Response
The response will be a JSON object with details of the uploaded file in Eueno.

### Functionality
The `upload_eueno()` function is used to upload the generated report and its corresponding torrent file to Eueno. The `profiling()` function is used to generate the Pandas Profiling Report and call the `upload_eueno()` function to upload the report to Eueno.

### Dependencies
This code requires the following dependencies to be installed:

* fastapi
* pandas_profiling
* pandas
* requests
* torf
* dotenv
### Environment Variables
This code uses environment variables to load the Eueno API key. Make sure to set the environment variable `KEY_API_EUENO` to your Eueno API key.
### Running the Docker Image
To run the API in a Docker container, use the following commands:
1. Build the Docker image:
```
docker build -t api .
```
2. Run the Docker container:
```
docker run -d -p 9000:9000 --name api api
```
The API should now be running and accessible at `http://localhost:9000`