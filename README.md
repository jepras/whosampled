# Who Sampled

This project allows users to search for songs using the Genius API and visualize the relationships between songs and the songs that sample them.

## Features

- Search for songs via the Genius API.
- Select a song from the search results.
- (Future) Fetch information about songs that sample the selected song.
- (Future) Visualize the sampling relationships as a graph.
- Simple web interface built with Streamlit.

## Setup

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd whosampled
    ```

2.  **Set up a Python virtual environment:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**

    Make sure you have `requirements.txt` in the project root with all necessary packages listed (e.g., `streamlit`, `requests`, `python-dotenv`, `networkx`, `plotly`). If not, you can generate it using:

    ```bash
    pip freeze > requirements.txt
    ```

    Then install:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Get a Genius API Access Token:**

    *   Go to the Genius API website and create an account and an API client.
    *   Generate an Access Token.

5.  **Create a `.env` file:**

    In the project root directory, create a file named `.env` and add your Genius API Access Token:

    ```dotenv
    GENIUS_ACCESS_TOKEN=YOUR_ACCESS_TOKEN_HERE
    ```
    Replace `YOUR_ACCESS_TOKEN_HERE` with your actual token.

## Running the Application

1.  **Activate your virtual environment (if not already active):**

    ```bash
    source .venv/bin/activate
    ```

2.  **Run the Streamlit application:**

    From the project root directory, run:

    ```bash
    streamlit run app.py
    ```

3.  The application will open in your web browser, usually at `http://localhost:8501`.

## Project Structure

```
whosampled/
├── app.py              # Streamlit web application entry point
├── main.py             # (Optional) Command-line entry point
├── requirements.txt    # Project dependencies
├── config.py           # Configuration loading (e.g., API key)
├── search.py           # Song search functionality
├── get_song_info.py    # Function to get song details and samples
├── .env                # Environment variables (API key)
├── .gitignore          # Specifies intentionally untracked files
└── whosampled/         # Python package directory
    ├── api/
    │   └── genius_client.py # Helper for API calls
    └── utils/
        └── graph_utils.py # Graph building and visualization utilities
``` 