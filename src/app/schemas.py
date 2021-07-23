from typing import List

from pydantic import BaseModel

class TextSample(BaseModel):
    text: str

class RequestBody(BaseModel):
    samples: List[TextSample]

    def to_array(self):
        return [sample.text for sample in self.samples]

class ResponseBody(BaseModel):
    List[str]

class Music(BaseModel):
    id: int
    title: str
    predictions: str

    class Config:
        orm_mode = True