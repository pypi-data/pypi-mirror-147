"""
General info of repository
"""
from typing import List, Optional

from pydantic import BaseModel, Field


class GeneralInfo(BaseModel):
    """
    Model for general information about the repository
    """

    title: Optional[str] = Field(None, description="Title project")
    author: Optional[str] = Field(None, description="Name author")
    author_contacts: Optional[List[str]] = Field(None, description="Contacts author")
    release: Optional[str] = Field(None, description="Version release")
    repository_main_url: Optional[str] = Field(None, description="Url to repository")
