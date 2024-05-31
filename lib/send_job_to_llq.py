import requests
from .utils import base_url, WordPressPostStatus
from .get_llq_token import get_token
from .exceptions import PostJobToLLQException
from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class Job:
    job_title_: str
    job_description_: str
    job_localization_: str
    job_type_of_contract_: list[str]
    job_type_of_post_: list[str]
    job_presence_: list[str]
    job_compagny_name_: str
    job_contact_email: Optional[str] = None
    job_apply_link: Optional[str] = None
    job_compagny_logo: Optional[int] = 1447  # ID in LLQ DB.


def post_with_token(endpoint: str, job: Job, slug: str, publish_date: str) -> dict:
    data = {
        "title": job.job_title_,
        "status": WordPressPostStatus.DRAFT,
        "slug": slug,
        "date": publish_date,
        "acf": asdict(job),
    }
    token = get_token()
    url = f"{base_url}{endpoint}"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code in [200, 201]:
        return response.json()
    else:
        raise PostJobToLLQException(
            f"Failed to post data. Status code: {response.status_code}, Response: {response.text}"
        )
