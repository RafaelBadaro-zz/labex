import requests

headers = {"Authorization": "token {}"}


def run_query(query): 
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

        
# GraphQL query 
query = """
{
  search(query: "stars:>100", type: REPOSITORY, first: 100) {
    nodes {
      ... on Repository {
        nameWithOwner
        url
        createdAt
        updatedAt
        pullRequests(states: MERGED) {
          totalCount
        }
        releases {
          totalCount
        }
        primaryLanguage{
          name
        }
        numeroTotalIssues: issues {
          totalCount
        }
        numeroTotalIssuesClosed: issues(states: CLOSED) {
          totalCount
        }
      }
    }
  }
}

"""

result = run_query(query)
print(result)