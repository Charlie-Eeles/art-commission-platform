import os
import uuid

import boto3
from botocore.client import Config
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from services.portfolio.models import PortfolioImage, PortfolioSettings, PortfolioSettingsRequest, UpdatePortfolioImageRequest
from services.portfolio.query_functions import create_image_qf, delete_image_qf, get_image_by_id_qf, get_portfolio_settings_qf, get_user_images_qf, update_image_qf, save_portfolio_settings_qf

from database import DbSession
from middleware.auth import get_current_user

router = APIRouter()

S3_BUCKET = os.getenv("S3_BUCKET", "portfolio-images")
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL", "http://localhost:4566")
S3_REGION = os.getenv("AWS_DEFAULT_REGION", "eu-west-2")
S3_PUBLIC_BASE_URL = os.getenv("S3_PUBLIC_BASE_URL", f"{S3_ENDPOINT_URL}/{S3_BUCKET}")


def _get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=S3_ENDPOINT_URL,
        region_name=S3_REGION,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
        config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),
    )


@router.post("/images", response_model=PortfolioImage, status_code=status.HTTP_201_CREATED)
async def upload_image(
    db: DbSession,
    current_user=Depends(get_current_user),
    art_name: str = Form(...),
    image: UploadFile = File(...),
):
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image",
        )

    upload_id = uuid.uuid4()
    file_ext = image.filename.rsplit(".", 1)[-1].lower() if image.filename and "." in image.filename else "bin"
    object_key = f"portfolio/{current_user.id}/{upload_id}.{file_ext}"

    s3 = _get_s3_client()

    try:
        s3.upload_fileobj(
            image.file,
            S3_BUCKET,
            object_key,
            ExtraArgs={"ContentType": image.content_type},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload image",
        )

    image_url = f"{S3_PUBLIC_BASE_URL}/{object_key}"

    return create_image_qf(db=db, art_name=art_name, image_url=image_url, upload_id=upload_id, user_id=current_user.id)


@router.get("/images", response_model=list[PortfolioImage])
def get_user_images(
    db: DbSession,
    current_user=Depends(get_current_user),
):
    return get_user_images_qf(db=db, user_id=current_user.id)


@router.get("/images/{image_id}", response_model=PortfolioImage)
def get_image(
    image_id: uuid.UUID,
    db: DbSession,
    current_user=Depends(get_current_user),
):
    res = get_image_by_id_qf(db=db, image_id=image_id, user_id=current_user.id)

    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found",
        )

    return res


@router.patch("/images/{image_id}", response_model=PortfolioImage)
def update_image(
    image_id: uuid.UUID,
    payload: UpdatePortfolioImageRequest,
    db: DbSession,
    current_user=Depends(get_current_user),
):
    res = update_image_qf(db=db, image_id=image_id, user_id=current_user.id, art_name=payload.art_name)

    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found",
        )

    db.commit()

    return res


@router.delete("/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_image(
    image_id: uuid.UUID,
    db: DbSession,
    current_user=Depends(get_current_user),
):
    res = delete_image_qf(db=db, image_id=image_id, user_id=current_user.id)

    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found",
        )

    db.commit()

    image_url = res["image_url"]
    object_key = image_url.removeprefix(f"{S3_PUBLIC_BASE_URL}/")

    try:
        _get_s3_client().delete_object(
            Bucket=S3_BUCKET,
            Key=object_key,
        )
    except Exception:
        pass

    return None

@router.put("/settings", response_model=PortfolioSettings)
def save_portfolio_settings(
    payload: PortfolioSettingsRequest,
    db: DbSession,
    current_user=Depends(get_current_user),
):
    res = save_portfolio_settings_qf(
        db=db,
        user_id=current_user.id,
        description=payload.description,
        is_public=payload.is_public,
        commission_slots=payload.commission_slots
    )
    db.commit()

    return res

@router.get("/settings", response_model=PortfolioSettings)
def get_portfolio_settings(
    db: DbSession,
    current_user=Depends(get_current_user),
):
    settings = get_portfolio_settings_qf(db=db, user_id=current_user.id)

    if settings is None:
        settings = save_portfolio_settings_qf(
            db=db,
            user_id=current_user.id,
            description="",
            is_public=False,
            commission_slots=3
        )

    return settings
