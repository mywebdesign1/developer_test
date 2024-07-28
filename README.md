# Uniswap Data Synchronization

## Overview

This project periodically fetches data every thirty minutes from the Uniswap subgraph and stores it in an SQLite database.

## Setup

1. **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Setup the database**:
    ```bash
    python setup_db.py
    ```

4. **Run the synchronization script**:
    ```bash
    python sync_data.py
    ```

5. **Run unit tests**:
    ```bash
    python -m unittest test_sync.py
    ```

## Usage

- The script `setup_db.py` creates an SQlite database file `test.db`.
- The script `sync_data.py` fetches data every 30 minutes and stores it in the SQLite database `test.db`.

## Configuration

- Database: `test.db`
- API Endpoint: Uniswap Subgraph
