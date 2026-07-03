from fastapi import APIRouter, Depends, status

from app.core.schemas import StandardResponse
from app.equipment.dependencies import get_equipment_service
from app.equipment.schemas import EquipmentCreate, EquipmentResponse, EquipmentUpdate
from app.equipment.service import EquipmentService

router = APIRouter(prefix="/equipment", tags=["Equipment"])


@router.get("/", response_model=StandardResponse[list[EquipmentResponse]], summary="List all equipment")
def list_equipment(
    service: EquipmentService = Depends(get_equipment_service),
) -> StandardResponse[list[EquipmentResponse]]:
    items = service.get_all()
    items_data = [EquipmentResponse.model_validate(e.__dict__) for e in items]
    return StandardResponse(
        success=True,
        message="Equipment retrieved successfully",
        meta={"total": len(items_data)},
        data=items_data,
    )


@router.get("/{equipment_id}", response_model=StandardResponse[EquipmentResponse], summary="Get a single equipment")
def get_equipment(
    equipment_id: int,
    service: EquipmentService = Depends(get_equipment_service),
) -> StandardResponse[EquipmentResponse]:
    equipment = service.get_by_id(equipment_id)
    equipment_data = EquipmentResponse.model_validate(equipment.__dict__)
    return StandardResponse(
        success=True,
        message="Equipment retrieved successfully",
        data=equipment_data,
    )


@router.post("/", response_model=StandardResponse[EquipmentResponse], status_code=status.HTTP_201_CREATED, summary="Create equipment")
def create_equipment(
    payload: EquipmentCreate,
    service: EquipmentService = Depends(get_equipment_service),
) -> StandardResponse[EquipmentResponse]:
    equipment = service.create(payload)
    equipment_data = EquipmentResponse.model_validate(equipment.__dict__)
    return StandardResponse(
        success=True,
        message="Equipment created successfully",
        data=equipment_data,
    )


@router.patch("/{equipment_id}", response_model=StandardResponse[EquipmentResponse], summary="Update equipment")
def update_equipment(
    equipment_id: int,
    payload: EquipmentUpdate,
    service: EquipmentService = Depends(get_equipment_service),
) -> StandardResponse[EquipmentResponse]:
    equipment = service.update(equipment_id, payload)
    equipment_data = EquipmentResponse.model_validate(equipment.__dict__)
    return StandardResponse(
        success=True,
        message="Equipment updated successfully",
        data=equipment_data,
    )


@router.delete("/{equipment_id}", response_model=StandardResponse[None], summary="Delete equipment")
def delete_equipment(
    equipment_id: int,
    service: EquipmentService = Depends(get_equipment_service),
) -> StandardResponse[None]:
    service.delete(equipment_id)
    return StandardResponse(
        success=True,
        message="Equipment deleted successfully",
    )
