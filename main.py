from fastapi import FastAPI
from data.call_meta_paper import *
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

pc = PaperCaller()

"""
KEYWORD_SEARCH_GET_LIMIT

MAX: 100


PAPER_IDS_POST_LIMIT

MAX: 500


REFERENCE_PAPERS_GET_LIMIT = 500

MAX: 500
"""

KEYWORD_SEARCH_GET_LIMIT = 20

PAPER_IDS_POST_LIMIT = 20

REFERENCE_PAPERS_GET_LIMIT = 20

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/paper/{keyword}")
async def get_papers_by_keyword(keyword: str, offset: str, api_key: str = "None"):
    if api_key != "NOne":
        papers = pc.get_papers_by_keyword(api_key=api_key, keyword=keyword, limit=KEYWORD_SEARCH_GET_LIMIT)
    else:
        papers = pc.get_papers_by_keyword(api_key=api_key, keyword=keyword, limit=KEYWORD_SEARCH_GET_LIMIT)
    return {"data": papers}

@app.get("/reference/{paper_id}")
async def get_reference_by_paper_id(paper_id: str, offset: str, api_key: str = "None"):
    main_data = pc.get_paper_by_paperId(paper_id, api_key)
    reference_paperIds = pc.get_reference_papers_ids_by_main_paper_id(paper_id, api_key, REFERENCE_PAPERS_GET_LIMIT)
    papers_data = pc.get_papers_by_paperIds(reference_paperIds, api_key, limit=PAPER_IDS_POST_LIMIT)

    return {"main_paper": main_data, "reference_papers": papers_data}