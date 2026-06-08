from pydantic import BaseModel, ConfigDict, Field, field_validator

class ProfileSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    bio: str = Field(..., examples=["Biograph text..."]) 

    @field_validator("bio")
    @classmethod
    def validate_positive_values(cls, value):
        if value is None or len(value.strip()) <= 0:
            raise ValueError(
                "Missing required fields"
            )

        return value
    
