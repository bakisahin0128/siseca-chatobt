from fastapi import APIRouter, HTTPException
from models.site_request import SiteRequest
from indexer import main

router = APIRouter()

@router.post("/process-site/")
def process_site(request: SiteRequest):
    allowed_sites = ["ECHA", "eur_lex", "resmigazete", "all"]
    if request.website_name not in allowed_sites:
        raise HTTPException(status_code=400, detail="Invalid website name")

    if request.website_name == "all":
        for site in allowed_sites[:-1]:  # "all" haricindeki siteleri işlemek için
            main(site.lower())
        return {"message": "Processing started for all websites"}
    else:
        main(request.website_name.lower())
        return {"message": f"Processing started for {request.website_name}"}
