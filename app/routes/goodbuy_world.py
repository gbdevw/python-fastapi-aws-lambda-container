from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/")
async def goodbye():
    return {"message": "Goodbye World"}