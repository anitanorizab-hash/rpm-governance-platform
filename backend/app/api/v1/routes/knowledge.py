"""Knowledge / RAG API (A6 G10) — CP14. JWT; admin manages sources; all query. No operational writes."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.audit import get_audit_context
from app.core.dependencies import get_current_user, require_roles
from app.db.session import get_db
from app.repositories.knowledge_repository import KnowledgeRepository
from app.schemas.knowledge import (
    KnowledgeSourceCreateIn, KnowledgeSourceOut, LiveLinkCreateIn, QueryIn, QueryOut,
)
from app.services.knowledge_service import KnowledgeService
from app.services.live_link_service import LiveLinkService
from app.services.rag_service import RAGService

router = APIRouter(prefix="/knowledge", tags=["knowledge"])
ADMIN = ("super_admin", "jpn_admin")


@router.post("/sources", response_model=KnowledgeSourceOut, status_code=201)
def create_source(body: KnowledgeSourceCreateIn, request: Request,
                  admin=Depends(require_roles(*ADMIN)), db: Session = Depends(get_db)):
    s = KnowledgeService(db).create_source(actor_id=admin.id, data=body.model_dump(),
                                           context=get_audit_context(request))
    return KnowledgeSourceOut.from_model(s)


@router.get("/sources", response_model=list[KnowledgeSourceOut])
def list_sources(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return [KnowledgeSourceOut.from_model(s) for s in KnowledgeService(db).list_sources()]


@router.get("/sources/{source_id}", response_model=KnowledgeSourceOut)
def get_source(source_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    s = KnowledgeService(db).get_source(source_id)
    if not s:
        raise HTTPException(status_code=404, detail="Knowledge source not found")
    return KnowledgeSourceOut.from_model(s)


@router.post("/sources/{source_id}/process")
def process_source(source_id: str, request: Request,
                   admin=Depends(require_roles(*ADMIN)), db: Session = Depends(get_db)):
    res = KnowledgeService(db).process_source(actor_id=admin.id, source_id=source_id,
                                              context=get_audit_context(request))
    if res is None:
        raise HTTPException(status_code=404, detail="Knowledge source not found")
    return res


@router.post("/live-links", status_code=201)
def create_live_link(body: LiveLinkCreateIn, request: Request,
                     admin=Depends(require_roles(*ADMIN)), db: Session = Depends(get_db)):
    return LiveLinkService(db).register(actor_id=admin.id, data=body.model_dump(),
                                        context=get_audit_context(request))


@router.post("/live-links/{link_id}/validate")
def validate_live_link(link_id: str, request: Request,
                       admin=Depends(require_roles(*ADMIN)), db: Session = Depends(get_db)):
    res = LiveLinkService(db).validate(actor_id=admin.id, link_id=link_id,
                                       context=get_audit_context(request))
    if res is None:
        raise HTTPException(status_code=404, detail="Live link not found")
    return res


@router.post("/query", response_model=QueryOut)
def query(body: QueryIn, request: Request,
          current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return RAGService(db).query(query=body.query, actor_id=current_user.id, top_k=body.top_k,
                                context=get_audit_context(request))


@router.get("/chunks/{chunk_id}")
def get_chunk(chunk_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    c = KnowledgeRepository(db).get_chunk(chunk_id)
    if not c:
        raise HTTPException(status_code=404, detail="Chunk not found")
    return {"id": c.id, "source_id": c.source_id, "text": c.text, "position": c.position}
