import json
import logging
import uuid
from typing import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from llama_index.core.schema import NodeWithScore

from src.api.schema import (
    ChatRequest,
    ChatResponse,
    SearchRequest,
    SearchResponse,
    SearchResult,
)
from src.config.load_config import load_config
from src.core.indexing import Indexer
from src.services.chat_engine import chat_engine

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize config and indexer
config = load_config()
indexer = Indexer(indexer_config=config.indexer_config()).get_index()


@router.post("/chat/stream")
async def stream_chat(request: ChatRequest) -> StreamingResponse:
    """
    Stream chat responses using the RAG system
    """
    try:
        # Get chat engine for the user
        engine = chat_engine(request.user_id)

        # Generate streaming response
        async def generate_response() -> AsyncGenerator[str, None]:
            try:
                # Stream the response from the chat engine
                response = engine.stream_chat(request.message)

                for token in response.response_gen:
                    # Create response object
                    chat_response = ChatResponse(
                        content=token,
                        user_id=request.user_id,
                        message_id=str(uuid.uuid4()),
                    )

                    # Send as Server-Sent Events
                    yield f"data: {json.dumps(chat_response.model_dump())}\n\n"

                # Send completion signal
                yield "data: [DONE]\n\n"

            except Exception as e:
                logger.error(f"Error in chat streaming: {str(e)}")
                error_response = {
                    "error": "An error occurred while processing your request",
                    "details": str(e),
                }
                yield f"data: {json.dumps(error_response)}\n\n"

        return StreamingResponse(
            generate_response(),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "text/event-stream",
            },
        )

    except Exception as e:
        logger.error(f"Error setting up chat stream: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error setting up chat stream: {str(e)}"
        )


@router.post("/search/stream")
async def stream_search(request: SearchRequest) -> StreamingResponse:
    """
    Stream search results from the vector database
    """
    try:

        async def generate_search_results() -> AsyncGenerator[str, None]:
            try:
                # Perform vector search
                retriever = indexer.as_retriever(similarity_top_k=request.limit)
                nodes = retriever.retrieve(request.query)

                # Convert nodes to search results
                search_results = []
                for node in nodes:
                    if isinstance(node, NodeWithScore):
                        search_result = SearchResult(
                            node_id=node.node_id,
                            text=node.text,
                            score=float(node.score),
                            metadata=node.metadata or {},
                        )
                    else:
                        search_result = SearchResult(
                            node_id=node.node_id,
                            text=node.text,
                            score=0.0,
                            metadata=node.metadata or {},
                        )
                    search_results.append(search_result)

                # Create response
                response = SearchResponse(
                    results=search_results,
                    query=request.query,
                    total_results=len(search_results),
                )

                # Stream the response
                yield f"data: {json.dumps(response.model_dump())}\n\n"
                yield "data: [DONE]\n\n"

            except Exception as e:
                logger.error(f"Error in search streaming: {str(e)}")
                error_response = {
                    "error": "An error occurred while searching",
                    "details": str(e),
                }
                yield f"data: {json.dumps(error_response)}\n\n"

        return StreamingResponse(
            generate_search_results(),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "text/event-stream",
            },
        )

    except Exception as e:
        logger.error(f"Error setting up search stream: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error setting up search stream: {str(e)}"
        )


@router.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Non-streaming chat endpoint for simple requests
    """
    try:
        engine = chat_engine(request.user_id)
        response = engine.chat(request.message)

        return ChatResponse(
            content=response.response,
            user_id=request.user_id,
            message_id=str(uuid.uuid4()),
        )

    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in chat: {str(e)}")


@router.post("/search")
async def search(request: SearchRequest) -> SearchResponse:
    """
    Non-streaming search endpoint
    """
    try:
        retriever = indexer.as_retriever(similarity_top_k=request.limit)
        nodes = retriever.retrieve(request.query)

        search_results = []
        for node in nodes:
            if isinstance(node, NodeWithScore):
                search_result = SearchResult(
                    node_id=node.node_id,
                    text=node.text,
                    score=float(node.score),
                    metadata=node.metadata or {},
                )
            else:
                search_result = SearchResult(
                    node_id=node.node_id,
                    text=node.text,
                    score=0.0,
                    metadata=node.metadata or {},
                )
            search_results.append(search_result)

        return SearchResponse(
            results=search_results,
            query=request.query,
            total_results=len(search_results),
        )

    except Exception as e:
        logger.error(f"Error in search: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in search: {str(e)}")


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "service": "imdb-movie-rag"}
