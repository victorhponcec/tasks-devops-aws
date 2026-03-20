from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Lookup Service")

@app.get("/urlinfo/1/{hostname_and_port}/{path:path}")
async def check_url(
    hostname_and_port: str, 
    path: str, 
    db: Session = Depends(get_db)
):
    #check url
    full_url_lookup = f"{hostname_and_port}/{path}"
    
    record = db.query(models.MalwareURL).filter(
        models.MalwareURL.url_identifier == full_url_lookup
    ).first()

    if record:
        return {
            "url": full_url_lookup,
            "is_safe": False,
            "threat_type": "malware",
            "detail": "This URL is present in the malware database."
        }
    
    return {
        "url": full_url_lookup,
        "is_safe": True,
        "threat_type": None,
        "detail": "URL not found in malware database."
    }

@app.post("/admin/add-malware/")
async def add_malware(url: str, db: Session = Depends(get_db)):
    new_entry = models.MalwareURL(url_identifier=url, is_malware=True)
    db.add(new_entry)
    db.commit()
    return {"message": f"Added {url} to blacklist"}