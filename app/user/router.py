import uuid
from fastapi import APIRouter, Depends, status

from app.core.schemas import StandardResponse
from app.user.schemas import UserProfileResponse, UserProfileCreate
from app.user.service import UserService
from app.user.dependencies import get_user_service

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/", response_model=StandardResponse[list[UserProfileResponse]], summary="List all users")
async def list_records(
    service: UserService = Depends(get_user_service),
) -> StandardResponse[list[UserProfileResponse]]:
    records = await service.get_all()
    records_data = [UserProfileResponse.model_validate(r.__dict__) for r in records]
    return StandardResponse(
        success=True,
        message="User records retrieved successfully",
        meta={"total": len(records_data)},
        data=records_data,
    )


@router.get("/{record_id}", response_model=StandardResponse[UserProfileResponse], summary="Get a single user profile")
async def get_record(
    record_id: uuid.UUID,
    service: UserService = Depends(get_user_service),
) -> StandardResponse[UserProfileResponse]:
    record = await service.get_by_id(record_id)
    record_data = UserProfileResponse.model_validate(record.__dict__)
    return StandardResponse(
        success=True,
        message="User profile retrieved successfully",
        data=record_data,
    )


@router.post("/", response_model=StandardResponse[UserProfileResponse], status_code=status.HTTP_201_CREATED, summary="Create a user profile")
async def create_record(
    payload: UserProfileCreate,
    service: UserService = Depends(get_user_service),
) -> StandardResponse[UserProfileResponse]:
    record = await service.create(payload)
    record_data = UserProfileResponse.model_validate(record.__dict__)
    return StandardResponse(
        success=True,
        message="User profile created successfully",
        data=record_data,
    )


@router.patch("/{record_id}", response_model=StandardResponse[UserProfileResponse], summary="Update a user profile")
async def update_record(
    record_id: uuid.UUID,
    payload: UserProfileCreate,
    service: UserService = Depends(get_user_service),
) -> StandardResponse[UserProfileResponse]:
    record = await service.update(record_id, payload)
    record_data = UserProfileResponse.model_validate(record.__dict__)
    return StandardResponse(
        success=True,
        message="User profile updated successfully",
        data=record_data,
    )


@router.delete("/{record_id}", response_model=StandardResponse[None], summary="Delete a user profile")
async def delete_record(
    record_id: uuid.UUID,
    service: UserService = Depends(get_user_service),
) -> StandardResponse[None]:
    await service.delete(record_id)
    return StandardResponse(
        success=True,
        message="User profile deleted successfully",
    )
