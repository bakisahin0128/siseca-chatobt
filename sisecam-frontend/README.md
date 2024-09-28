# <div align="center">Şişecam PoC - Frontend Streamlit UI for RAG System</div>

---

##  Running the Streamlit Application:

### Using Docker:

#### 1. Clone the repository:

```sh
git clone https://github.com/itelligencetr/ds-sisecam-poc.git
```

#### 2. Navigate to the App Directory:

```sh
cd Frontend
```

#### 3. Build the Docker image:

```sh
docker build -t <YOUR-IMAGE-NAME> .
```

#### 4. Run the container:
```sh
docker run -p 8000:8000 <YOUR-IMAGE-NAME>
```

This will start the Streamlit application inside the container and map port 8000 inside the container to port 8000 on your host machine.

- Note: Replace `<YOUR-IMAGE-NAME>` with the actual name you assign to your Docker image during build.

### Using Virtual Environment:

#### 1. Clone the repository:

```sh
git clone https://github.com/itelligencetr/ds-sisecam-poc.git
```

#### 2. Navigate to the App Directory:

```sh
cd Frontend
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
    conda create -n streamlit-env python=3.9
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
      conda activate streamlit-env
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

Once you have installed all the required dependencies, you can run the Streamlit app in the development mode by typing the following command in the built-in Terminal:

```sh
python -m streamlit run main.py
```

Or you can run the file `main.py` directly.
