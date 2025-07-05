from fastapi import FastAPI, APIRouter, HTTPException, Depends, Header, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timedelta
import aiohttp
import asyncio
from enum import Enum
import requests
import json

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="Challenge Tracker Platform", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Security
security = HTTPBearer()

# Models
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    name: str
    picture: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
class Session(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    session_token: str
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ChallengeStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"

class ProjectStatus(str, Enum):
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DEPLOYED = "deployed"

class Challenge(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    title: str
    description: str
    goals: List[str] = []
    rules: List[str] = []
    duration_days: Optional[int] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    status: ChallengeStatus = ChallengeStatus.ACTIVE
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Project(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    challenge_id: str
    user_id: str
    title: str
    description: str
    repository_url: Optional[str] = None
    demo_url: Optional[str] = None
    tech_stack: List[str] = []
    status: ProjectStatus = ProjectStatus.PLANNING
    progress_percentage: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_url_check: Optional[datetime] = None
    url_status: Dict[str, Any] = {}

class ChallengeCreate(BaseModel):
    title: str
    description: str
    goals: List[str] = []
    rules: List[str] = []
    duration_days: Optional[int] = None

class ProjectCreate(BaseModel):
    title: str
    description: str
    repository_url: Optional[str] = None
    demo_url: Optional[str] = None
    tech_stack: List[str] = []
    status: ProjectStatus = ProjectStatus.PLANNING

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    repository_url: Optional[str] = None
    demo_url: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    status: Optional[ProjectStatus] = None
    progress_percentage: Optional[int] = None

# Auth functions
async def get_current_user(authorization: HTTPAuthorizationCredentials = Depends(security)):
    token = authorization.credentials
    
    # Check if session exists and is valid
    session = await db.sessions.find_one({"session_token": token})
    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")
    
    # Check if session is expired
    if datetime.utcnow() > session["expires_at"]:
        await db.sessions.delete_one({"session_token": token})
        raise HTTPException(status_code=401, detail="Session expired")
    
    # Get user
    user = await db.users.find_one({"id": session["user_id"]})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return User(**user)

# URL monitoring background task
async def check_url_status(url: str) -> Dict[str, Any]:
    """Check if URL is accessible and return status info"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                return {
                    "url": url,
                    "status_code": response.status,
                    "accessible": response.status < 400,
                    "response_time": response.headers.get("X-Response-Time", "N/A"),
                    "checked_at": datetime.utcnow().isoformat()
                }
    except Exception as e:
        return {
            "url": url,
            "status_code": None,
            "accessible": False,
            "error": str(e),
            "checked_at": datetime.utcnow().isoformat()
        }

async def monitor_project_urls(project_id: str):
    """Background task to monitor project URLs"""
    project = await db.projects.find_one({"id": project_id})
    if not project:
        return
    
    url_status = {}
    
    # Check repository URL
    if project.get("repository_url"):
        status = await check_url_status(project["repository_url"])
        url_status["repository"] = status
    
    # Check demo URL
    if project.get("demo_url"):
        status = await check_url_status(project["demo_url"])
        url_status["demo"] = status
    
    # Update project with URL status
    await db.projects.update_one(
        {"id": project_id},
        {
            "$set": {
                "url_status": url_status,
                "last_url_check": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        }
    )

# Auth Routes
@api_router.post("/auth/profile")
async def get_user_profile(x_session_id: str = Header(...)):
    """Get user profile from Emergent Auth"""
    try:
        headers = {"X-Session-ID": x_session_id}
        response = requests.get(
            "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data",
            headers=headers
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid session")
        
        user_data = response.json()
        
        # Check if user exists
        existing_user = await db.users.find_one({"email": user_data["email"]})
        
        if not existing_user:
            # Create new user
            user = User(
                email=user_data["email"],
                name=user_data["name"],
                picture=user_data.get("picture")
            )
            await db.users.insert_one(user.dict())
        else:
            user = User(**existing_user)
        
        # Create session
        session = Session(
            user_id=user.id,
            session_token=user_data["session_token"],
            expires_at=datetime.utcnow() + timedelta(days=7)
        )
        await db.sessions.insert_one(session.dict())
        
        return {
            "user": user,
            "session_token": user_data["session_token"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Challenge Routes
@api_router.post("/challenges", response_model=Challenge)
async def create_challenge(
    challenge_data: ChallengeCreate,
    current_user: User = Depends(get_current_user)
):
    challenge = Challenge(
        user_id=current_user.id,
        title=challenge_data.title,
        description=challenge_data.description,
        goals=challenge_data.goals,
        rules=challenge_data.rules,
        duration_days=challenge_data.duration_days,
        start_date=datetime.utcnow()
    )
    
    if challenge_data.duration_days:
        challenge.end_date = challenge.start_date + timedelta(days=challenge_data.duration_days)
    
    await db.challenges.insert_one(challenge.dict())
    return challenge

@api_router.get("/challenges", response_model=List[Challenge])
async def get_challenges(current_user: User = Depends(get_current_user)):
    challenges = await db.challenges.find({"user_id": current_user.id}).to_list(1000)
    return [Challenge(**challenge) for challenge in challenges]

@api_router.get("/challenges/{challenge_id}", response_model=Challenge)
async def get_challenge(
    challenge_id: str,
    current_user: User = Depends(get_current_user)
):
    challenge = await db.challenges.find_one({"id": challenge_id, "user_id": current_user.id})
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    return Challenge(**challenge)

@api_router.put("/challenges/{challenge_id}", response_model=Challenge)
async def update_challenge(
    challenge_id: str,
    challenge_data: ChallengeCreate,
    current_user: User = Depends(get_current_user)
):
    challenge = await db.challenges.find_one({"id": challenge_id, "user_id": current_user.id})
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    update_data = challenge_data.dict()
    update_data["updated_at"] = datetime.utcnow()
    
    await db.challenges.update_one(
        {"id": challenge_id, "user_id": current_user.id},
        {"$set": update_data}
    )
    
    updated_challenge = await db.challenges.find_one({"id": challenge_id, "user_id": current_user.id})
    return Challenge(**updated_challenge)

# Project Routes
@api_router.post("/challenges/{challenge_id}/projects", response_model=Project)
async def create_project(
    challenge_id: str,
    project_data: ProjectCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    # Verify challenge exists and belongs to user
    challenge = await db.challenges.find_one({"id": challenge_id, "user_id": current_user.id})
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    project = Project(
        challenge_id=challenge_id,
        user_id=current_user.id,
        title=project_data.title,
        description=project_data.description,
        repository_url=project_data.repository_url,
        demo_url=project_data.demo_url,
        tech_stack=project_data.tech_stack,
        status=project_data.status
    )
    
    await db.projects.insert_one(project.dict())
    
    # Start URL monitoring in background
    if project.repository_url or project.demo_url:
        background_tasks.add_task(monitor_project_urls, project.id)
    
    return project

@api_router.get("/challenges/{challenge_id}/projects", response_model=List[Project])
async def get_challenge_projects(
    challenge_id: str,
    current_user: User = Depends(get_current_user)
):
    # Verify challenge exists and belongs to user
    challenge = await db.challenges.find_one({"id": challenge_id, "user_id": current_user.id})
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    projects = await db.projects.find({"challenge_id": challenge_id, "user_id": current_user.id}).to_list(1000)
    return [Project(**project) for project in projects]

@api_router.get("/projects/{project_id}", response_model=Project)
async def get_project(
    project_id: str,
    current_user: User = Depends(get_current_user)
):
    project = await db.projects.find_one({"id": project_id, "user_id": current_user.id})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return Project(**project)

@api_router.put("/projects/{project_id}", response_model=Project)
async def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    project = await db.projects.find_one({"id": project_id, "user_id": current_user.id})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    update_data = {k: v for k, v in project_data.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    await db.projects.update_one(
        {"id": project_id, "user_id": current_user.id},
        {"$set": update_data}
    )
    
    # Re-monitor URLs if they were updated
    if "repository_url" in update_data or "demo_url" in update_data:
        background_tasks.add_task(monitor_project_urls, project_id)
    
    updated_project = await db.projects.find_one({"id": project_id, "user_id": current_user.id})
    return Project(**updated_project)

@api_router.delete("/projects/{project_id}")
async def delete_project(
    project_id: str,
    current_user: User = Depends(get_current_user)
):
    result = await db.projects.delete_one({"id": project_id, "user_id": current_user.id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}

# Dashboard Routes
@api_router.get("/dashboard")
async def get_dashboard(current_user: User = Depends(get_current_user)):
    # Get user's challenges
    challenges = await db.challenges.find({"user_id": current_user.id}).to_list(1000)
    
    # Get user's projects
    projects = await db.projects.find({"user_id": current_user.id}).to_list(1000)
    
    # Calculate stats
    total_challenges = len(challenges)
    active_challenges = len([c for c in challenges if c["status"] == "active"])
    completed_challenges = len([c for c in challenges if c["status"] == "completed"])
    
    total_projects = len(projects)
    completed_projects = len([p for p in projects if p["status"] == "completed"])
    
    # Calculate overall progress
    if total_projects > 0:
        total_progress = sum(p.get("progress_percentage", 0) for p in projects)
        overall_progress = total_progress / total_projects
    else:
        overall_progress = 0
    
    # Get tech stack distribution
    tech_stack_counts = {}
    for project in projects:
        for tech in project.get("tech_stack", []):
            tech_stack_counts[tech] = tech_stack_counts.get(tech, 0) + 1
    
    return {
        "user": current_user,
        "stats": {
            "total_challenges": total_challenges,
            "active_challenges": active_challenges,
            "completed_challenges": completed_challenges,
            "total_projects": total_projects,
            "completed_projects": completed_projects,
            "overall_progress": round(overall_progress, 1)
        },
        "recent_challenges": challenges[-5:] if challenges else [],
        "recent_projects": projects[-5:] if projects else [],
        "tech_stack_distribution": tech_stack_counts
    }

# Health check
@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()