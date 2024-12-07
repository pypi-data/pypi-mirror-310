from token import OP
from typing import Any
import requests
from data_type import FieldType


class Teable:
    def __init__(self, base_url: str, api_key: str):
        self.api_url = base_url + "/api"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
        }

    def __str__(self) -> str:
        return f"Teable API at {self.api_url}"

    def __repr__(self) -> str:
        return f"Teable(base_url='{self.api_url}', api_key='***')"

    def get_tables(self, base_id: str) -> list["Table"]:
        response = requests.get(
            f"{self.api_url}/base/{base_id}/table",
            headers=self.headers,
        )
        if response.status_code == 200:
            tables = [Table(**t, teable=self) for t in response.json()]
            return tables
        else:
            raise Exception(
                f"Failed to fetch tables with status code: {response.status_code}, message: {response.text}"
            )

    def create_table(self, base_id: str, table_data: "Table") -> "Table":
        response = requests.post(
            f"{self.api_url}/base/{base_id}/table",
            json=table_data.to_dict(),
            headers=self.headers,
        )
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(
                f"Failed to create table with status code: {response.status_code}, message: {response.text}"
            )


class Table:
    def __init__(
        self,
        name: str,
        dbTableName: str,
        fields: list["Field"] | None = None,
        teable: Teable | None = None,
        id: str | None = None,
        **kwargs,
    ) -> None:
        self.teable = teable
        self.name = name
        self.dbTableName = dbTableName
        self.fields = fields or []
        self.table_id = id
        self.meta = kwargs

    def __str__(self) -> str:
        return f"Table '{self.name}' (DB Table: {self.dbTableName})"

    def __repr__(self) -> str:
        return f"Table(name='{self.name}', dbTableName='{self.dbTableName}', fields={self.fields})"

    def get_fields(self) -> list["Field"]:
        if self.teable is None:
            raise Exception("Teable instance is not provided.")

        response = requests.get(
            f"{self.teable.api_url}/table/{self.table_id}/field",
            headers=self.teable.headers,
        )
        if response.status_code == 200:
            self.fields = [
                Field(teable=self.teable, field_type=f["type"], **f)
                for f in response.json()
            ]
            return self.fields
        else:
            raise Exception(
                f"Failed to fetch table fields with status code: {response.status_code}, message: {response.text}"
            )
    
    def to_dict(self) -> dict[str, str | list[dict[str, str | dict[str, list[dict[str, str]]]]]]:
        return {
            "name": self.name,
            "dbTableName": self.dbTableName,
            "fields": [field.to_dict() for field in self.fields]
        }

class Field:
    def __init__(
        self,
        name: str,
        dbFieldName: str,
        field_type: str | FieldType,
        options: dict | list["Option"],
        notNull: bool | None = None,
        teable: Teable | None = None,
        **kwargs,
    ) -> None:
        self.teable = teable
        self.name = name
        self.dbFieldName = dbFieldName
        if isinstance(field_type, FieldType):
            self.field_type = field_type
        else:
            self.field_type = FieldType.from_teable(field_type)
        self.notNull = notNull
        self.options = options
        if self.field_type == FieldType.SINGLE_SELECT and isinstance(options, dict):
            self.options = [Option(**o) for o in options["choices"]]
        self.meta = kwargs

    def __str__(self) -> str:
        return f"Field '{self.name}' (DB Field: {self.dbFieldName})"

    def __repr__(self) -> str:
        return f"Field(name='{self.name}', dbFieldName='{self.dbFieldName}', field_type={self.field_type}, options={self.options})"

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "dbFieldName": self.dbFieldName,
            "type": self.field_type.teable_value,
            "options": {"choices": [option.to_dict() for option in self.options]} if self.options else {},
        }

class Option:
    def __init__(self, name: str, **kwargs) -> None:
        self.name = name
        self.meta = kwargs

    def __str__(self) -> str:
        return f"Options '{self.name}'"

    def __repr__(self) -> str:
        return f"Options(name='{self.name}')"

    def to_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
        }
