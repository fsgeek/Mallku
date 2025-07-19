from pydantic import BaseModel, Extra


class ModelConfig(BaseModel):
    """A base model with a reusable config."""

    class Config:
        """Pydantic config."""

        extra = Extra.allow
        use_enum_values = True
        arbitrary_types_allowed = True
