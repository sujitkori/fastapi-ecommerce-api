from pathlib import Path
import shutil
import uuid
from fastapi import UploadFile, HTTPException, status


MAX_FILE_SIZE = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}

def validate_image(image:UploadFile):
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only image files are allowed."
        )
    
    extension = Path(image.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only jpg, jpeg, png and webp are allowed.")
    
    image.file.seek(0, 2) # Think of file as a long tape with a cursor. seek() simply moves the cursor/pointer inside the uploaded file
                                    #     keyboard.jpg

                                    #   Bytes:
                                    #   A B C D E F G H I J
                                    #   ^
                                    #   Cursor starts here

                                    # It's syntax is file.seek(offset, whence). offset → how far to move. whence → where to start counting from

    size = image.file.tell()

    image.file.seek(0)

    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Maximum allowed size is {MAX_FILE_SIZE // (1024 * 1024)} MB.")
        

async def save_image(image:UploadFile) -> str:
    extension = Path(image.filename).suffix
    filename = f"{uuid.uuid4().hex}{extension}"

    media_folder = Path("media/products") # Path is not a string. It's an object that represents a filesystem path. If we simply write "media/products/" it's just a string. we cannot do things like folder.mkdir() Now python know, Oh, this represents an actual folder on disk."

    media_folder.mkdir(parents=True, exist_ok=True) # We have wrote this because if media/product doesn't exist in your Folder structure then the code crashes . And if it doesn't there then it will create automatically
                                                    # Now python says, "Go to the path represented by this Path object and create the directory if needed. Only this line actually interacts with the filesystem.
                                                    # use oarents=True if you are creating folder inside folder

    file_path = media_folder / filename  # Path("media/products") does NOT create or access the folder. It only creates a Python object that represents that path. Think of it like writing an address on a piece of paper.

    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer) # image.file is a python file object. If you do content = image.file.read() then content is of type bytes.

    return f"media/products/{filename}" # Here instead of using media_folder we wrote manually f"media/products" because to be consistent. Because in linux it might use backward slash (\) so.




# NOTE:
# Good question. "image/" is not something we invented for FastAPI. It comes from the MIME type / media type standard used for HTTP files.

# When a browser uploads a file, the request includes a Content-Type for that file.

# For images, the MIME types look like:

# image/jpeg
# image/png
# image/webp
# image/gif
# image/svg+xml

# So when we write, image.content_type.startswith("image/")
# we are asking:

# "Does the uploaded file's content type belong to the image category?"

# Example
# For a JPEG:
# image.content_type might be "image/jpeg",
# then, image.startswith("image/") 
# returns True

# seek Explanation
# The general syntax is:

# file.seek(offset, whence)

# where whence tells Python where to start counting from.

# The three common whence values
# 0 → beginning of file
# 1 → current position
# 2 → end of file

# So:

# seek(0, 0)

# means:

# Start from beginning, move 0 bytes.

# seek(0, 2)

# means:

# Start from end, move 0 bytes.

# seek(-10, 2)

# means:

# Start from end, move backward 10 bytes.

# What if you want the middle?

# Suppose the file is 100 bytes.

# You could do:

# file.seek(50, 0)

# That means:

# Start at the beginning and move 50 bytes.