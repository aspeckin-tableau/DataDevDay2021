
import argparse
import getpass

import tableauserverclient as TSC


def main():

    metadata_query = """
    {
      workbooksConnection(first: 3) {
        nodes {
          name
          id
          sheets {
            name
          }
          dashboards {
            name
          }
        }
      }
    }
    """

    parser = argparse.ArgumentParser(description="Query Tableau Server Metadata API")
    parser.add_argument('--server', '-s', required=True, help='tableau server url')
    parser.add_argument('--username', '-u', required=True, help='username of tableau server user')
    parser.add_argument('--password', '-p', required=False, help='password of tableau server user')
    parser.add_argument('--site', '-n', default='', required=False, help='url namespace of tableau server site')

    args = parser.parse_args()

    if not args.password:
        password = getpass.getpass(f'{args.username} Password: ')
    else:
        password = args.password

    tableau_auth = TSC.TableauAuth(args.username, password, args.site)
    server = TSC.Server(args.server)
    server.add_http_options({'verify': False})
    server.version = '3.5'
    workbooks = {}

    with server.auth.sign_in(tableau_auth):

        results = server.metadata.query(metadata_query)

    for node in results['data']['workbooksConnection']['nodes']:

        if node['name'] not in workbooks:
            workbooks[node['name']] = {}
            workbooks[node['name']]['Dashboards'] = []
            workbooks[node['name']]['Worksheets'] = []

        for sheet in node['sheets']:

            if sheet['name'] not in workbooks[node['name']]['Worksheets']:
                workbooks[node['name']]['Worksheets'].append(sheet['name'])

        for dashboard in node['dashboards']:

            if dashboard['name'] not in workbooks[node['name']]['Dashboards']:
                workbooks[node['name']]['Dashboards'].append(dashboard['name'])

    print(workbooks)


if __name__ == '__main__':
    main()
