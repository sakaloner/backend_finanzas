import sys
sys.path.append('..')
from fastapi import FastAPI

from task_1.algo import OrdersManager
import crud


app = FastAPI()


@app.get("/")
async def home():
    return {"message": "Esta es un prototipo de api para una entidad que procesa transacciones financiera"}

@app.post("/populated")
def populate_database(num_transactions:int=1_000_000):
    om = OrdersManager(num_transactions)
    om.save_to_json_db('db_files/transactions')
    return {"message": f"successfully created the database data with {num_transactions} transactions"}

@app.get("/transactions")
def get_transactions(offset:int=0, limit:int=1000):
    return crud.get_lines(offset=offset, limit=limit)

@app.post("/transactions/{transaction_id}")
def get_transaction_with_id(transaction_id:int):
    return crud.get_transaction_by_id(trans_id=transaction_id)


