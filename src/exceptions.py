from fastapi import status, HTTPException

class NotFoundException(HTTPException):
    def __init__(self, message: str = "Not Found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)
        
