# FastAPI Logs Archive API

### This API provides functionalities to upload, archive, and search logs.

## Getting Started

###  Configuration

Before running the application, configuration is necessary.

    Rename the .env.sample file to .env:

```shell
mv .env.sample .env   # On Windows, use: rename .env.sample .env
```

Edit the .env file and replace YOUR_SECRET_KEY with a strong secret key for JWT token encoding/decoding. Tools like RandomKeygen can generate strong keys.

### Running the App via Docker🐳:
    
    Ensure you have Docker and Docker-compose installed on your machine.
    Clone this repository:

```shell
  git clone [repository-url]
  cd [repository-name]
   ```

### Build and start the app:

   ```shell
   docker-compose build
   docker-compose up
   ```

The API will be accessible at http://localhost:8000.

Database Persistence via Docker container

Please note that the database exists only within the Docker container. As such, once the container is stopped or removed, all stored data will be lost. However, upon the first run, the app will automatically seed the database with 10 logs from the past, allowing users to immediately test the search functionality.
Uploading and Searching Logs

### Running the App Locally

If you have Python installed and your interpreter is correctly configured, you can also run the app locally:

    Clone the repository:

```shell
  git clone [repository-url]
  cd [repository-name]
```

(Optional) Create and activate a virtual environment:

```shell
  python3 -m venv venv
  source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

Install the required dependencies and run the Uvicorn server::

```shell
  pip install -r requirements.txt
  uvicorn main:app --reload
```

Upon starting the app, a SQLite database (app_db.db) will be created in your project directory. You can manually seed this database with initial data by running the init.sql script.
User Interaction and Authentication

### To easily interact with the API, navigate to the Swagger UI at http://localhost:8000/docs.

To utilize endpoints related to searching and uploading logs, you must be registered and authenticated.

    Register a new user by making a POST request to the api/auth/register endpoint.
    When logging in, use the email you registered with in the username field and your password in the password field. This applies both when using Swagger UI and tools like Postman (where you would use x-www-form-urlencoded for the request body).
    For subsequent requests, use the token you obtained during login for authentication. In Postman, set the header Authorization with the value bearer <your_auth_token>. If you're using the ModHeader browser extension, you can set the authorization header in a similar manner.


### Sample log files (logs_template.txt and logs_zip_test.zip) are provided in the project directory. You can use these for testing log uploads via the logs/upload endpoint in the Swagger UI.

To search for logs:

    By Content: You may assume any word as a keyword. So, just simply input a word or phrase in the 'content' parameter.
    By Timestamp: Use the format YYYY-MM-DDTHH:MM:SSZ (e.g., 2023-08-05T10:00:00Z). The date precedes the T character, followed by the time. You have the ability to input start_datetime and end_datetime to apply the diapazone.