import requests
from .exceptions import GetJobsFromGraphQLException
from .utils import base_url
import logging
import re

GET_JOB_TITLES = """
    query ($first: Int) {
      jobs(first: $first) {
        nodes {
          jobs {
            jobTitle
          }
        }
      }
    }
"""

variables = {"first": 120}


def get_titles() -> list[str]:
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        f"{base_url}/graphql",
        json={"query": GET_JOB_TITLES, "variables": variables},
        headers=headers,
    )

    if response.status_code in [200, 201]:
        data = response.json()
        return [
            re.sub(r"[^A-Za-z0-9\s]", "", job["jobs"]["jobTitle"])
            for job in data["data"]["jobs"]["nodes"]
        ]
    else:
        logging.error(
            f"Error in jobsTitle query : \n variables : {variables} \n headers : {headers}"
        )
        raise GetJobsFromGraphQLException(
            f"Error in jobsTitle query : \n variables : {variables} \n headers : {headers}"
        )
