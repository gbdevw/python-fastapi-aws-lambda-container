from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/")
async def hello():
    return {"message": "Hello World"}