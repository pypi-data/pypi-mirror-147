from sqlalchemy import Column, Integer, Identity, TEXT
from sqlmodel import Field

from sql_models.SQLCamelModel import SQLCamelModel
from sql_models.manufacturer.NewManufacturer import NewManufacturer
from sql_models.shared.visibility.RoleVisibility import RoleVisibility


class ManufacturerEntity(RoleVisibility, SQLCamelModel, table=True):
    __tablename__ = 'manufacturer'

    id: int = Field(
        primary_key=True,
        sa_column=Column('id', Integer, Identity(start=0, cycle=True)),
    )

    name: str = Field(
        sa_column=Column(TEXT)
    )

    image_width: int | None
    image_height: int | None

    def __init__(
            self,
            **data,
    ):
        super().__init__(**data)

    @classmethod
    def from_new_manufacturer(cls, new_manufacturer: NewManufacturer):
        manufacturer = cls(
            **(new_manufacturer.dict()),
        )

        manufacturer.id = manufacturer.name.replace(" ", "-").lower()
        manufacturer.name = manufacturer.name.title()

        return manufacturer
