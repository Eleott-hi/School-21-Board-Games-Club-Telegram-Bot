from pydantic import BaseModel, EmailStr


class EmailInfo(BaseModel):
    email: EmailStr
    subject: str
    message: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "laptev18vv@gmail.com",
                    "subject": "Test email",
                    "message": "Hello, world!",
                }
            ]
        }
    }
