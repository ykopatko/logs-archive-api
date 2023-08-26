import io
import zipfile

from fastapi import UploadFile, File


async def extract_zip(file: UploadFile = File(...)) -> list:
    """
    Extract a zip file and return a list of contained files' contents.
    """
    contents = []
    with zipfile.ZipFile(io.BytesIO(await file.read())) as z:
        for filename in z.namelist():
            with z.open(filename) as f:
                file_content = f.read().decode()
                for line in file_content.splitlines():
                    contents.append(line.strip())
    return contents
