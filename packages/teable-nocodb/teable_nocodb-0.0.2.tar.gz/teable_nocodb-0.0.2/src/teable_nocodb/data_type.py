from enum import Enum

class FieldType(Enum):
    """Enumeration of field types in NocoDB and Teable."""
    ID = ("ID", "singleLineText")
    SINGLE_LINE_TEXT = ("SingleLineText", "singleLineText")
    LONG_TEXT = ("LongText", "longText")
    USER = ("User", "user")
    ATTACHMENT = ("Attachment", "attachment")
    CHECKBOX = ("Checkbox", "checkbox")
    MULTIPLE_SELECT = ("MultiSelect", "multipleSelect")
    SINGLE_SELECT = ("SingleSelect", "singleSelect")
    DATE = ("Date", "date")
    NUMBER = ("Number", "number")
    DURATION = ("Duration", "duration")
    RATING = ("Rating", "rating")
    FORMULA = ("Formula", "formula")
    ROLLUP = ("Rollup", "rollup")
    COUNT = ("Count", "count")
    LINK = ("LinkToAnotherRecord", "link")
    CREATED_TIME = ("CreatedTime", "createdTime")
    LAST_MODIFIED_TIME = ("LastModifiedTime", "lastModifiedTime")
    CREATED_BY = ("CreatedBy", "createdBy")
    LAST_MODIFIED_BY = ("LastModifiedBy", "lastModifiedBy")
    AUTO_NUMBER = ("AutoNumber", "autoNumber")
    BUTTON = ("Button", "button")
    PHONE_NUMBER = ("PhoneNumber", "singleLineText")
    EMAIL = ("Email", "singleLineText")
    URL = ("URL", "singleLineText")
    LINKS = ("Links", "singleLineText")


    def __init__(self, nocodb_value: str, teable_value: str):
        self.nocodb_value = nocodb_value
        self.teable_value = teable_value

    @classmethod
    def from_nocodb(cls, field_type: str):
        """Convert from NocoDB field type to FieldType."""
        for f in cls:
            if f.nocodb_value == field_type:
                return f
        raise ValueError(f"No matching FieldType for NocoDB value: {field_type}")

    @classmethod
    def from_teable(cls, field_type: str):
        """Convert from Teable field type to FieldType."""
        for f in cls:
            if f.teable_value == field_type:
                return f
        raise ValueError(f"No matching FieldType for Teable value: {field_type}")

    def to_nocodb(self):
        """Get the NocoDB representation of this field type."""
        return self.nocodb_value

    def to_teable(self):
        """Get the Teable representation of this field type."""
        return self.teable_value
