# README.md
# LinkForge - AI Co-founder Platform

LinkForge is an AI-powered platform designed to act as an intelligent co-founder and mentor for entrepreneurs. It assists from the ideation and validation phases through to traction and ecosystem connection.

## Features

*   **Intelligent Idea Validation:** Analyze market potential, identify risks, and suggest pivots.
*   **Automated Canvas Generation:** Create Lean Canvas and Business Model Canvas based on AI interactions.
*   **Strategic Guidance:** Provide data-driven insights and actionable next steps.

## Getting Started

### Prerequisites

*   Python 3.9+
*   Docker (optional, but recommended for development)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd linkforge
    ```

2.  **Install dependencies using Poetry:**
    ```bash
    poetry install
    ```

3.  **Run the FastAPI application:**
    ```bash
    poetry run uvicorn linkforge.main:app --reload
    ```

The API will be available at `http://localhost:8000`. You can access the interactive API documentation at `http://localhost:8000/docs`.

### API Endpoints

*   **POST `/validate-idea`**: Submit an idea for AI-driven validation.
    *   **Request Body:**
        ```json
        {
          "idea": "Your business idea description"
        }
        ```
    *   **Response Body:**
        ```json
        {
          "market_analysis": {
            "tam": "Total Addressable Market",
            "sam": "Serviceable Available Market",
            "som": "Serviceable Obtainable Market"
          },
          "potential_pivots": ["Pivot suggestion 1", "Pivot suggestion 2"],
          "next_steps": ["Action item 1", "Action item 2"]
        }
        ```
*   **GET `/`**: Root endpoint for API health check.

## Project Structure

```
linkforge/
├── __init__.py
├── main.py       # FastAPI application entry point
# models.py     # Pydantic models (currently integrated into main.py for simplicity)
pyproject.toml    # Poetry project configuration
README.md         # This file
Dockerfile        # Docker configuration for production deployment
.gitignore        # Git ignore file
```

## Contributing

Contributions are welcome! Please refer to the `CONTRIBUTING.md` file (to be created) for guidelines.

## License

This project is licensed under the MIT License - see the `LICENSE` file (to be created) for details.