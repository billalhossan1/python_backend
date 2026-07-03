from fastapi import APIRouter, Depends, status

from app.core.schemas import StandardResponse
from app.health.dependencies import get_health_service
from app.health.schemas import HealthRecordCreate, HealthRecordResponse, HealthRecordUpdate
from app.health.service import HealthRecordService

router = APIRouter(prefix="/health", tags=["Health Records"])


@router.get("/", response_model=StandardResponse[list[HealthRecordResponse]], summary="List all health records")
def list_records(
    service: HealthRecordService = Depends(get_health_service),
) -> StandardResponse[list[HealthRecordResponse]]:
    records = service.get_all()
    records_data = [HealthRecordResponse.model_validate(r.__dict__) for r in records]
    return StandardResponse(
        success=True,
        message="Health records retrieved successfully",
        meta={"total": len(records_data)},
        data=records_data,
    )


@router.get("/{record_id}", response_model=StandardResponse[HealthRecordResponse], summary="Get a single health record")
def get_record(
    record_id: int,
    service: HealthRecordService = Depends(get_health_service),
) -> StandardResponse[HealthRecordResponse]:
    record = service.get_by_id(record_id)
    record_data = HealthRecordResponse.model_validate(record.__dict__)
    return StandardResponse(
        success=True,
        message="Health record retrieved successfully",
        data=record_data,
    )


@router.post("/", response_model=StandardResponse[HealthRecordResponse], status_code=status.HTTP_201_CREATED, summary="Create a health record")
def create_record(
    payload: HealthRecordCreate,
    service: HealthRecordService = Depends(get_health_service),
) -> StandardResponse[HealthRecordResponse]:
    record = service.create(payload)
    record_data = HealthRecordResponse.model_validate(record.__dict__)
    return StandardResponse(
        success=True,
        message="Health record created successfully",
        data=record_data,
    )


@router.patch("/{record_id}", response_model=StandardResponse[HealthRecordResponse], summary="Update a health record")
def update_record(
    record_id: int,
    payload: HealthRecordUpdate,
    service: HealthRecordService = Depends(get_health_service),
) -> StandardResponse[HealthRecordResponse]:
    record = service.update(record_id, payload)
    record_data = HealthRecordResponse.model_validate(record.__dict__)
    return StandardResponse(
        success=True,
        message="Health record updated successfully",
        data=record_data,
    )


@router.delete("/{record_id}", response_model=StandardResponse[None], summary="Delete a health record")
def delete_record(
    record_id: int,
    service: HealthRecordService = Depends(get_health_service),
) -> StandardResponse[None]:
    service.delete(record_id)
    return StandardResponse(
        success=True,
        message="Health record deleted successfully",
    )
