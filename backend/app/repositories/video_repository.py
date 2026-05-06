from sqlalchemy.orm import Session
from app.models.video import Video
from app.schemas.video import VideoCreate
from typing import List, Optional

class VideoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_isan(self, isan: str) -> Optional[Video]:
        return self.db.query(Video).filter(Video.isan == isan).first()
    
    def get_all(self, skip: int = 0, limit: int = 20) -> List[Video]:
        return self.db.query(Video).offset(skip).limit(limit).all()
    
    def create(self, video: Video) -> Video:
        self.db.add(video)
        self.db.commit()
        self.db.refresh(video)
        return video
    
    def delete(self, video: Video) -> None:
        self.db.delete(video)
        self.db.commit()

        

    #esta clase solo habla con la base de datos.