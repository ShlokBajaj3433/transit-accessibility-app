# backend/main.py
# FastAPI Application Entry Point for Transit Accessibility App

# Purpose: Provides REST API endpoints for:
#   - Route planning with accessibility considerations
#   - Eco-friendly transit impact tracking
#   - Accessibility alerts and information
#   - User engagement through gamification (points/badges)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers from route modules
from routes import health, climate, accessibility, routing, users


# FastAPI Application Initialization

app = FastAPI(
    title="Inclusive Transit API",
    description="Accessibility-first transit API supporting wheelchair users, visually impaired, and hearing impaired individuals",
    version="1.0.0"
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict to frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register Routers

# Health check endpoints
app.include_router(health.router)

# Climate impact and gamification endpoints
app.include_router(climate.router)

# Accessibility information endpoints
app.include_router(accessibility.router)

# Route planning endpoints
app.include_router(routing.router)

# User engagement endpoints
app.include_router(users.router)

# Main Entry Point

if __name__ == "__main__":
    import uvicorn
    
    # Run the application with: uvicorn main:app --reload
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )
