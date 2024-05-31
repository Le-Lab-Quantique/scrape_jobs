import requests
from exceptions import GetJobsFromGraphQLException
from utils import base_url

GET_JOB_TITLES = """
    query ($last: Int) {
      jobs(last: $last) {
        nodes {
          jobTitle
        }
      }
    }
"""

variables = {"last": 50}


def get_titles() -> list[str]:
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        f"{base_url}/graphql",
        json={"query": GET_JOB_TITLES, "variables": variables},
        headers=headers,
    )

    if response.status_code in [200, 201]:
        data = response.json()

        return [job["jobTitle"] for job in data["data"]["jobs"]["nodes"]]
    else:
        raise GetJobsFromGraphQLException(
            f"Error in jobsTitle query : \n variables : {variables} \n headers : {headers}"
        )
