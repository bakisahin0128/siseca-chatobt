# <div align="center">Şişecam PoC - API</div>

---

##  Description

This project is a FastAPI web application built using the Model-View-Controller (MVC) architecture. The code is organized into separate directories for models, controllers, and routes, promoting separation of concerns and maintainability.

---

## Project Code Structure:

```
.
├── controllers/
│   └── ... (controller files)
├── models/
│   └── ... (model files)
├── routes/
│   └── ... (route files)
├── main.py
├── config.py
├── indexer.py
├── dockerfile
└── requirements.txt

```
- **controllers/**: This directory consists of FastAPI controllers that handle incoming API requests. Controllers interact with models to retrieve, create, update, or delete data. They also handle request validation and response formatting.
- **models/**: This directory contains Python classes representing the data model of your application. These classes typically define the attributes and logic related to your data entities.
- **routes/**: This directory defines the API endpoints for your application. Each endpoint maps to a specific controller method, providing a clear separation between routing logic and controller implementation.
- **main.py**: This file is the application entry point. It creates the FastAPI application instance and configures it with necessary settings.
- **indexer.py**: This file contains the logic for ingesting PDF Files into Azure AI Search index in order to be able to perform RAG later.
- **dockerfile**: This file defines the instructions for building a Docker image for your application.
- **requirements.txt**: This file lists the required Python dependencies for the project.


---

##  Running the FastAPI Application:

### Using Docker:

#### 1. Clone the repository:

```sh
git clone https://github.com/itelligencetr/ds-sisecam-poc.git
```

#### 2. Navigate to the App Directory:

```sh
cd Backend
```

#### 3. Build the Docker image:

```sh
docker build -t <YOUR-IMAGE-NAME> .
```

#### 4. Run the container:
```sh
docker run -p 8000:8000 <YOUR-IMAGE-NAME>
```

This will start the FastAPI application inside the container and map port 8000 inside the container to port 8000 on your host machine.

- Note: Replace `<YOUR-IMAGE-NAME>` with the actual name you assign to your Docker image during build.

### Using Virtual Environment:

#### 1. Clone the repository:

```sh
git clone https://github.com/itelligencetr/ds-sisecam-poc.git
```

#### 2. Navigate to the App Directory:

```sh
cd Backend
```

#### 3. Create the virtual environment:

1. Using `venv`:
    ```sh
    python -m venv venv
    ```

2. Using `virtualenv` (if installed):
    ```sh
    virtualenv venv
    ```

3. Using `conda` (if installed):
    ```sh
    conda create -n fastapi-env python=3.9
    ```

#### 4. Activate the virtual environment:
   1. Using `venv` or `virtualenv`:
   
      1. MacOs/Linux:
          ```sh
          source venv/bin/activate
          ```
      2. Windows:
          ```sh
          venv\Scripts\activate
          ```

   2. Using `conda`:
      ```sh
      conda activate fastapi-env
      ```

#### 5. Install dependencies:

1. Using `pip`:
   ```sh
   pip install -r requirements.txt
   ```
   
2. Using `conda`:
    ```sh
    conda install -c conda-forge -f requirements.txt
    ```

#### 6. Run the development server:

Once you have installed all the required dependencies, you can run the FastAPI app in the development mode by typing the following command in the built-in Terminal:

```sh
uvicorn main:app --reload
```

Or you can run the file `main.py` directly.

---

## Using the API:
The specific API endpoints and their functionalities will be documented within the `routes.py` file. This documentation typically includes details on:

- HTTP methods supported (GET, POST, PUT, DELETE)
- Path parameters and query string arguments
- Request body format (if applicable)
- Expected response format
