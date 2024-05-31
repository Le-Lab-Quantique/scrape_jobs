from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
from typing import List, Optional
import re
from lib.send_job_to_llq import post_with_token, Job


@dataclass
class JobItem:
    title: str
    company: str
    description: str
    location: str
    pub_date: str
    guid: str
    link: str
    image_url: Optional[str]


AQORA_JB_RSS_URL = "https://jobs.aqora.io/rss/jobs"


def fetch_rss_feed(url: str) -> Optional[bytes]:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(e)
        return None


def parse_rss_feed(xml_content: bytes) -> List[JobItem]:
    soup = BeautifulSoup(xml_content, "xml")
    items = soup.find_all("item")
    job_items = []

    for item in items:
        if re.search(r"Le Lab Quantique", item.get_text(), re.IGNORECASE):
            continue

        title = item.find("title").text if item.find("title") else ""
        company = item.find("company").text if item.find("company") else ""
        description = item.find("description").text if item.find("description") else ""
        location = item.find("location").text if item.find("location") else ""
        pub_date = item.find("pubDate").text if item.find("pubDate") else ""
        guid = item.find("guid").text if item.find("guid") else ""
        link = item.find("link").text if item.find("link") else ""
        image_url = item.find("image").text if item.find("image") else None

        job_item = JobItem(
            title=title,
            company=company,
            description=description,
            location=location,
            pub_date=pub_date,
            guid=guid,
            link=link,
            image_url=image_url,
        )

        job_items.append(job_item)

    return job_items


def main():
    xml_content = fetch_rss_feed(AQORA_JB_RSS_URL)
    if xml_content:
        job_items = parse_rss_feed(xml_content)
        for job in job_items:
            mapped_job = Job(
                job_title_=job.title,
                job_description_=job.description,
                job_localization_=job.location,
                job_type_of_contract_=["Unknown"],
                job_type_of_post_=["Unknown"],
                job_presence_=["Unknown"],
                job_compagny_name_=job.company,
                job_apply_link=job.link,
            )
            res = post_with_token(
                "/wp-json/wp/v2/job", mapped_job, job.guid, job.pub_date
            )
            print(res)


if __name__ == "__main__":
    main()
