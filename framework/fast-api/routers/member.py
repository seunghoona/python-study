from fastapi import APIRouter

router = APIRouter()


@router.get("/member")
def member():
    return {"message": "Member retrieved successfully"}
