from fastapi import HTTPException, status


class AccountManager:
    def __init__(self) -> None:
        self.accounts = {}

    def reset(self):
        self.accounts.clear()

    def get_balance(self, account_id):
        if account_id not in self.accounts:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    
    def create(self, account_id):
        if account_id not in self.accounts:
            self.accounts[account_id] = 0

    def deposit(self, destination, amount):
        self.create(destination)
        self.accounts[destination] += amount

    def withdraw(self, origin, amount):
        if origin not in self.accounts:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
        
        if amount > self.accounts[origin]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"You do not have this value available, your balance: {self.accounts[origin]}"
            )
        
        self.accounts[origin] -= amount
        
    def transfer(self, origin, destination, amount):
        if origin not in self.accounts:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
        
        if amount > self.accounts[origin]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"You do not have this value available, your balance: {self.accounts[origin]}"
            )
        
        self.create(destination)
        self.accounts[origin] -= amount
        self.accounts[destination] += amount

        