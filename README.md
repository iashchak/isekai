
# Isekai Project

Welcome to the **Isekai** project! This repository is a FastAPI-based backend designed for generating randomized "isekai" scenarios. It leverages datasets and algorithms to create imaginative settings, characters, and attributes.

## Features

- **Dynamic API Endpoints**: Versioned API endpoints (`v1`, `v2`) for generating scenarios.
- **Customizable Data**: Scenarios are generated from CSV datasets, making it easy to expand or customize.
- **Authentication**: Basic HTTP authentication for API endpoints.

---

## API Overview

### Endpoints

- `/api/health`: Returns the health status of the server.
- `/api/privacy`: Displays the privacy agreement in plain text.
- `/api/v1/generate`: Generates random isekai scenarios using the `v1` dataset.
  - Parameters:
    - `k`: Number of selections per attribute (default: 3).
    - `p_zero`: Probability of excluding attributes (default: 0.4).
- `/api/v2/generate`: Generates scenarios using the `v2` dataset with metadata-driven selection logic.
  - Parameters:
    - `k`: Scaling factor for selections (default: 1).
    - `n`: Number of items to select per attribute (default: 1).
    - `p_zero`: Probability of excluding attributes (default: 0.4).

### Example Usage

1. **Health Check**
   ```bash
   curl http://localhost:8000/api/health
   ```

2. **Generate Scenarios (v1)**
   ```bash
   curl -u user:password "http://localhost:8000/api/v1/generate?k=3&p_zero=0.4"
   ```

3. **Generate Scenarios (v2)**
   ```bash
   curl -u user:password "http://localhost:8000/api/v2/generate?k=2&n=1&p_zero=0.3"
   ```

---

## Datasets

The project includes the following data files (under `data/v2/`):
{chr(10).join([f"- `{key}`: {', '.join(value['columns'])}" for key, value in analysis['data_overview'].items()])}

---

## Installation

### Prerequisites

- Python 3.8+
- Docker (optional)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/iashchak/isekai.git
   cd isekai
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the application:
   ```bash
   python main.py
   ```

---

## Deployment

### Using Docker

1. Build the image:
   ```bash
   docker build -t isekai-app .
   ```

2. Run the container:
   ```bash
   docker run -p 8080:8080 isekai-app
   ```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

See [LICENSE.md](LICENSE.md) for details.
