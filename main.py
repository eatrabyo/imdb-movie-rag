import asyncio
import logging

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.routes import router
from src.api.schema import ErrorResponse, SubErrorResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="IMDB Movie RAG API",
    description="A streaming RAG API for IMDB movie data",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {str(exc)}", exc_info=True)

    if isinstance(exc, HTTPException):
        if exc.status_code == 408:
            return JSONResponse(status_code=exc.status_code, content=exc.detail)

    sub_error_response = SubErrorResponse(
        status=str(exc),
        http_status=500,
        message="An unexpected error occurred",
        step=str(exc),
    )

    error_response = ErrorResponse(detail=sub_error_response.model_dump())

    return JSONResponse(status_code=500, content=error_response.model_dump())


# Include the router
app.include_router(router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
