import uvicorn
from fastapi import FastAPI, HTTPException, status, Response
from fastapi.responses import JSONResponse
from .models import EventData
from .manager import AccountManager

app = FastAPI()

accounts_manager = AccountManager()

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    if exc.status_code == status.HTTP_404_NOT_FOUND:
        return JSONResponse(content=0, status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.post("/reset")
async def reset():
    accounts_manager.reset()
    return Response("OK", status_code=status.HTTP_200_OK)


@app.get("/balance")
async def get_balance(account_id: str):
    accounts_manager.get_balance(account_id)   
    return accounts_manager.accounts[account_id]


@app.post("/event", status_code=status.HTTP_201_CREATED)
async def create_account_or_deposit(event: EventData):
    match event.type:
        case "deposit":
            accounts_manager.deposit(event.destination, event.amount)
            return {"destination": {"id": event.destination, "balance": accounts_manager.accounts[event.destination]}}
        case "withdraw":
            accounts_manager.withdraw(event.origin, event.amount)
            return {"origin": {"id": event.origin, "balance": accounts_manager.accounts[event.origin]}}
        case "transfer":
            accounts_manager.transfer(event.origin, event.destination, event.amount)
            return {
                "origin": {"id": event.origin, "balance": accounts_manager.accounts[event.origin]}, 
                "destination": {"id": event.destination, "balance": accounts_manager.accounts[event.destination]}
            }
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid event type")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)