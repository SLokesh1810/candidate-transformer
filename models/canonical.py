from typing import List, Optional

from pydantic import BaseModel, Field


class Location(BaseModel):
    city: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None


class Links(BaseModel):
    github: Optional[str] = None
    linkedin: Optional[str] = None
    portfolio: Optional[str] = None
    other: List[str] = Field(default_factory=list)


class Skill(BaseModel):
    name: str
    confidence: float
    sources: List[str] = Field(default_factory=list)


class Experience(BaseModel):
    company: Optional[str] = None
    title: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class Education(BaseModel):
    institution: Optional[str] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    end_year: Optional[int] = None


class Provenance(BaseModel):
    field: str
    source: str
    method: str


class CanonicalCandidate(BaseModel):
    candidate_id: Optional[str] = None
    full_name: Optional[str] = None
    emails: List[str] = Field(default_factory=list)
    phones: List[str] = Field(default_factory=list)
    location: Location = Field(default_factory=Location)
    links: Links = Field(default_factory=Links)
    headline: Optional[str] = None
    years_experience: Optional[float] = None
    skills: List[Skill] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    provenance: List[Provenance] = Field(default_factory=list)
    overall_confidence: Optional[float] = None