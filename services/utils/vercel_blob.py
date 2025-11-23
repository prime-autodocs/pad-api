"""Vercel Blob utility"""
import base64
from io import BytesIO
import requests

UPLOAD_IMAGE_URL = "https://vercel-blob-gateway.vercel.app/api/upload"

class VercelBlobError(Exception):
    """Domain-specific error for Vercel Blob operations."""


class VercelBlob:
    """Class for Vercel Blob"""

    @classmethod
    def upload_with_delete(cls, image_base64: str, image_name: str) -> str:
        """Upload image to Vercel Blob"""
        del_response = requests.delete(
            url=UPLOAD_IMAGE_URL,
            data={"pathname": image_name},
            timeout=10,
        )
        if del_response.status_code != 200:
            raise VercelBlobError(f"Error deleting blob '{image_name}': {del_response.text}")

        # remove prefixo caso venha assim: data:image/png;base64,xxxx
        if image_base64.startswith("data:image"):
            image_base64 = image_base64.split(",")[1]

        # decodifica SOMENTE UMA VEZ
        image_bytes = base64.b64decode(image_base64)

        files = {
            "file": (image_name, BytesIO(image_bytes), "image/png"),
        }

        response = requests.post(
            url=UPLOAD_IMAGE_URL,
            files=files,
            timeout=10,
        )

        if response.status_code != 200:
            raise VercelBlobError(f"Error uploading blob '{image_name}': {response.text}")

        return response.json()["url"]
