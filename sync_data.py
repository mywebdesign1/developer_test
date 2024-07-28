import requests
import schedule
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setup_db import Pool

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

UNISWAP_SUBGRAPH_URL = "https://gateway-arbitrum.network.thegraph.com/api/5fd299b87186a191321be76cc1c61ecc/subgraphs/id/5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV"

def fetch_data():
    query = """
    {
      pools {
        id
        token0 {
          id
        }
        token1 {
          id
        }
      }
    }
    """
    response = requests.post(UNISWAP_SUBGRAPH_URL, json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed with status code {response.status_code}")

def store_data(data):
    session = SessionLocal()
    try:
        pools = data.get('data', {}).get('pools', [])
        for pool in pools:
            pool_id = pool.get('id')
            token0_id = pool.get('token0', {}).get('id')
            token1_id = pool.get('token1', {}).get('id')

            # Check if pool already exists
            existing_pool = session.query(Pool).filter_by(pool=pool_id).first()
            if existing_pool:
                # Update existing pool
                existing_pool.token0 = token0_id
                existing_pool.token1 = token1_id
            else:
                # Create new pool
                new_pool = Pool(pool=pool_id, token0=token0_id, token1=token1_id)
                session.add(new_pool)
        
        session.commit()
        print("Data stored successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()

def job():
    print("Fetching and storing data...")
    data = fetch_data()
    store_data(data)
    print("Data has been fetched and stored successfully.")

schedule.every(30).minutes.do(job)

if __name__ == "__main__":
    print("Running initial data fetch...")
    job()
    
    while True:
        schedule.run_pending()
        time.sleep(1)
