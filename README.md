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

The project follows a modular architecture with clear separation of concerns. Here's a detailed overview:

```
whosampled/                      # Root project directory
├── app.py                      # Streamlit app entry point
│   └── Imports from: → components, services, state, api, utils
│
├── requirements.txt            # Project dependencies
├── setup.py                    # Package installation
│
└── whosampled/                 # Main package directory
    ├── __init__.py            # Package initialization (version, exports)
    │
    ├── config.py              # Configuration (ACCESS_TOKEN)
    │   └── Used by: ← api/genius_client.py
    │
    ├── api/                   # API-related code
    │   ├── __init__.py
    │   │
    │   ├── genius_client.py   # Base API client
    │   │   ├── Imports: → config
    │   │   └── Used by: → get_song_info.py, search.py
    │   │
    │   ├── get_song_info.py   # Song info functions
    │   │   ├── Imports: → genius_client
    │   │   └── Used by: → app.py
    │   │
    │   └── search.py         # Search functionality
    │       ├── Imports: → genius_client
    │       └── Used by: → services/search_service.py
    │
    ├── components/            # UI components
    │   ├── __init__.py
    │   │
    │   └── search_components.py
    │       └── Used by: → app.py
    │
    ├── services/             # Business logic
    │   ├── __init__.py
    │   │
    │   └── search_service.py
    │       ├── Imports: → api/search, state/app_state
    │       └── Used by: → app.py
    │
    ├── state/               # State management
    │   ├── __init__.py
    │   │
    │   └── app_state.py
    │       └── Used by: → services/search_service.py, app.py
    │
    └── utils/              # Utility functions
        ├── __init__.py
        │
        └── graph_utils.py
            └── Used by: → app.py
```

### Key Components and Their Relationships

1. **Entry Point**:
   - `app.py` (Streamlit UI):
     - Uses components for UI rendering
     - Uses services for business logic
     - Uses state for application state management
     - Uses API for data fetching
     - Uses utils for graph visualization

2. **API Layer**:
   - `genius_client.py`: Base API client that handles all Genius API requests
   - `get_song_info.py`: Functions for fetching song details and samples
   - `search.py`: Search functionality using the Genius API

3. **UI Layer**:
   - `components/`: Contains all Streamlit UI components
   - `search_components.py`: Handles the search interface and song selection

4. **Business Logic**:
   - `services/`: Contains business logic and application rules
   - `search_service.py`: Manages search operations and state updates

5. **State Management**:
   - `state/`: Manages application state
   - `app_state.py`: Handles song selection and search state

### Data Flow

1. **Search Flow**:
   ```
   User Search
   ├── → search_components.py (UI input)
   ├── → search_service.py (process request)
   ├── → api/search.py (API call)
   ├── → genius_client.py (HTTP request)
   ├── → search_service.py (process response)
   ├── → app_state.py (update state)
   └── → search_components.py (update UI)
   ```

2. **Song Selection Flow**:
   ```
   User Selection
   ├── → search_components.py (UI selection)
   ├── → search_service.py (process selection)
   ├── → app_state.py (update state)
   └── → search_components.py (update UI)
   ```

3. **Sample Visualization Flow**:
   ```
   Sample Display
   ├── → app.py (trigger visualization)
   ├── → get_song_info.py (fetch samples)
   ├── → graph_utils.py (create visualization)
   └── → app.py (display graph and details)
   ```

### Design Principles

- **Separation of Concerns**: Each module has a specific responsibility
- **Single Entry Point**: All functionality is accessed through the Streamlit app
- **Dependency Flow**: Dependencies flow from top to bottom
- **API Layer**: All external API calls go through `genius_client.py`
- **State Management**: Centralized in `app_state.py`
- **UI Components**: Isolated in `components/`
- **Business Logic**: Contained in `services/`

## Development

// ... rest of existing content after the old project structure section ... 