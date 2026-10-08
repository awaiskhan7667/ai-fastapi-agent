from fastapi import APIRouter
from services.api_services import ask_ai,stream_ai
from services.rag_service import rag_answer, build_index, pdf_rag_answer
from services.ai_services import ask_with_tool
from models.ai import AIRequest, AIResponse
from fastapi.responses import StreamingResponse

router = APIRouter(tags=["AI"])
knowledge_base = [
    "FastAPI is a Python framework for building APIs.",
    "RAG retrieves relevant information before generating an answer.",
    "FAISS is used for similarity search over vectors.",
    "LangGraph is used to build stateful AI workflows."
]

rag_index, rag_chunks = build_index(knowledge_base)



@router.post("/", response_model=AIResponse, description="Send a question to the AI for a specific user.")
def ask_question(request:AIRequest):
    return ask_ai(request.question,  request.history)

@router.post("/stream")
def stream_question(request: AIRequest):
    return StreamingResponse(stream_ai(request.question),media_type="text/event-stream")

@router.post("/rag")
def rag_question(request: AIRequest):
    answer = rag_answer(
        request.question,
        rag_index,
        rag_chunks
    )

    return {
        "question": request.question,
        "answer": answer
    }

@router.post("/pdf-rag")
def pdf_rag_question(request: AIRequest):

    answer = pdf_rag_answer(
        request.question,
        "documents/Profile.pdf"
    )

    return {
        "question": request.question,
        "answer": answer
    }

@router.post("/tool")
def tool_question(request: AIRequest):
    answer = ask_with_tool(request.question)

    return {
        "question": request.question,
        "answer": answer
    }