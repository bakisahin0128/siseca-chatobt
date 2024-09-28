from pydantic import BaseModel


class SiteRequest(BaseModel):
    website_name: str