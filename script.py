import requests
import time
import csv

headers = {"Authorization": "token "}

endCursor = "null"  # Proxima pagina
nodes = []  # Resultados da query


def run_query(query):
    request = requests.post('https://api.github.com/graphql',
                            json={'query': query}, headers=headers)
    while (request.status_code == 502):
        time.sleep(2)
        request = requests.post(
            'https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(
            request.status_code, query))


for x in range(50):
    # GraphQL query
    query = """
  {
  search(query: "stars:>100", type: REPOSITORY, first: 20, after:%s) {
    pageInfo {
      endCursor
    }
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
  """ % (endCursor)

    # O resultado da query que contem a proxima pagina e os nodes
    queryResult = run_query(query)
    querySize = len(queryResult['data']['search']['nodes'])
    for y in range(querySize):
        # Salva os nodes no array de nodes
        nodes.append(queryResult["data"]["search"]["nodes"][y])
        # Pega o endCursor aka proxima pagina
        endCursor = '"{}"'.format(
            queryResult["data"]["search"]["pageInfo"]["endCursor"])


# print(nodes)

# Escreve em um arquivo csv
with open("/Users/Rafael/Desktop/labex/repos.csv", 'w') as new_file:

    fnames = [
        'name_with_owner',
        'url',
        'created_at',
        'updated_at',
        'merged_pull_requests',
        'releases',
        'primary_language',
        'total_issues',
        'total_issues_closed']

    csv_writer = csv.DictWriter(new_file, fieldnames=fnames)
    csv_writer.writeheader()
    for node in nodes:
        csv_writer.writerow(
            {
                'name_with_owner': node['nameWithOwner'],
                'url': node['url'],
                'created_at': node['createdAt'],
                'updated_at': node['updatedAt'],
                'merged_pull_requests': node['pullRequests']['totalCount'],
                'releases': node['releases']['totalCount'],
                'primary_language': node['primaryLanguage']['name'] if node['primaryLanguage']!= None else 'null',
                'total_issues': node['numeroTotalIssues']['totalCount'],
                'total_issues_closed': node['numeroTotalIssuesClosed']['totalCount'],
            })

    print('Arquivo csv gerado com sucesso!')
