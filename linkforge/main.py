# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI(
    title="LinkForge API",
    description="API for the LinkForge AI Co-founder Platform",
    version="1.0.0",
)

class IdeaInput(BaseModel):
    idea: str

class ValidationOutput(BaseModel):
    market_analysis: dict
    potential_pivots: list
    next_steps: list

@app.post("/validate-idea", response_model=ValidationOutput)
async def validate_idea(idea_input: IdeaInput):
    """
    Validates a business idea using mock AI logic.
    In a real implementation, this endpoint would interact with advanced AI models
    to perform market analysis, suggest pivots, and outline next steps.
    """
    idea = idea_input.idea.lower()
    
    # Mock data generation based on the input idea
    mock_analysis = {
        "tam": "Global market for AI-powered business tools",
        "sam": "Market for entrepreneurship support platforms",
        "som": "Niche market for AI co-founders for early-stage startups"
    }
    
    mock_pivots = []
    if "social media" in idea:
        mock_pivots.append("Focus on B2B SaaS for social media analytics")
    if "e-commerce" in idea:
        mock_pivots.append("Integrate with major e-commerce platforms for deeper insights")
    mock_pivots.append("Pivot towards a specific industry vertical")
        
    mock_next_steps = [
        "Conduct user interviews with target audience.",
        "Develop a Lean Canvas for the core idea.",
        "Research competitor landscape in detail.",
        "Build a basic landing page to gauge interest."
    ]
    
    # Specific mock response for "LinkForge" idea
    if "linkforge" in idea:
        mock_analysis = {"tam": "Global AI Co-founder Market", "sam": "Entrepreneurship Support Platforms", "som": "AI Mentorship for Link School of Business"}
        mock_pivots = ["Expand to other business schools", "Offer B2B SaaS for accelerators"]
        mock_next_steps = ["Onboard first 100 Link School users", "Gather feedback for MVP refinement", "Develop automated Lean Canvas feature"]

    return ValidationOutput(
        market_analysis=mock_analysis,
        potential_pivots=mock_pivots,
        next_steps=mock_next_steps
    )

@app.get("/")
async def read_root():
    """Root endpoint for API health check."""
    return {"message": "Welcome to the LinkForge API!"}

if __name__ == "__main__":
    # This allows running the app directly using `python main.py`
    # For production, use `uvicorn linkforge.main:app --host 0.0.0.0 --port 8000`
    uvicorn.run(app, host="0.0.0.0", port=8000)
