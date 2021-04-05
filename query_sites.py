
import argparse
import getpass
import requests

from xml.etree import ElementTree as ET

NAMESPACE = {'t': 'http://tableau.com/api'}


def main():

    parser = argparse.ArgumentParser(description="Query Sites on a Tableau Server")
    parser.add_argument('--server', '-s', required=True, help='tableau server url')
    parser.add_argument('--version', '-v', required=True, help='tableau server api version')
    parser.add_argument('--username', '-u', required=False, help='username of tableau server user')
    parser.add_argument('--token', '-t', required=False, help='personal access token name')
    parser.add_argument('--https_cert', '-c', required=False, help='path to HTTPS cert')

    args = parser.parse_args()

    if not args.username and not args.token:
        raise ValueError('Either username or token must be defined in command line')

    auth_value, auth_secret, auth_method, auth_token = None, None, None, None

    if args.username:
        auth_value = args.username
        auth_secret = getpass.getpass(f'{args.username} Password: ')
        auth_method = 'CLASSIC'

    if args.token:
        auth_value = args.token
        auth_secret = getpass.getpass(f'{args.token} Value: ')
        auth_method = 'TOKEN'

    if args.https_cert:
        verify_ssl = args.https_cert
    else:
        verify_ssl = False

    api_url = f'{args.server}/api/{args.version}'

    try:
        auth_token = api_sign_in(api_url, auth_method, auth_value, auth_secret,
                                 '', verify_ssl)
        sites = api_query_sites(api_url, auth_token, verify_ssl)

        for site in sites:
            print(f'{sites[site]}\n')

    except Exception as e:
        print(e)

    finally:
        api_sign_out(api_url, auth_token, '', verify_ssl)


def api_query_sites(server_url: str, auth_token: str, verify_ssl: str) -> dict:
    """Query all the sites on a Tableau Server.

    Args:
        server_url (str): Tableau Server API URL.
        auth_token (str): REST API credentials token.
        verify_ssl (str): Path to HTTPS cert. False if HTTP Request will be sent.

    Returns:
          dict: Nested dictionary of Tableau Server Sites.

    """
    page_size = 100
    page_number = 1
    total_returned = 0
    sites = {}

    while True:

        sites_url = (
            f'{server_url}/sites/?pageSize={page_size}&pageNumber={page_number}'
        )

        api_response = requests.get(sites_url,
                                    headers={"X-tableau-auth": auth_token},
                                    verify=verify_ssl)

        if api_response.status_code != 200:
            error_code, summary, detail = format_error(
                ET.fromstring(api_response.content))
            raise Exception(
                "Error querying Tableau Server Sites"
                f"Error: {error_code}\nSummary: {summary}\nDetail: {detail}")

        else:
            total_available = ET.fromstring(api_response.content).find(
                './/t:pagination', namespaces=NAMESPACE).attrib['totalAvailable']

            total_available = int(total_available)

            page_number += 1
            total_returned += page_size

            site_elements = ET.fromstring(api_response.content).findall(
                './/t:site', namespaces=NAMESPACE)

            for site in site_elements:

                sites[site.attrib['name']] = {}
                sites[site.attrib['name']]['Name'] = site.attrib['name']
                sites[site.attrib['name']]['Luid'] = site.attrib['id']
                sites[site.attrib['name']]['Url Namespace'] = site.attrib['contentUrl']
                sites[site.attrib['name']]['State'] = site.attrib['state']

            if total_returned >= total_available:
                break

    return sites


def api_sign_in(server_url: str, auth_method: str, auth_value, auth_secret: str,
                site_url_namespace: str, verify_ssl: str) -> str:
    """Authenticate with a Site on the Tableau Server.

    Args:
        server_url (str): Tableau Server API URL.
        auth_method (str): Token or Classic.
        auth_value (str): Name of the Token or User.
        auth_secret (str): Token Value or Password.
        site_url_namespace (str): Tableau Server Site name as it appears in
            the URL.
        verify_ssl (str): Path to HTTPS cert. False if HTTP Request will be sent.

    Returns:
        str: Token used for API authentication.

    """
    if auth_method.upper() not in ['TOKEN', 'CLASSIC']:
        raise ValueError(
            f'Auth Method {auth_method} is not supported. Please use TOKEN or CLASSIC')

    credentials_element = None
    sign_in_url = f'{server_url}/auth/signin'

    api_request = ET.Element('tsRequest')

    if auth_method.upper() == 'CLASSIC':
        credentials_element = ET.SubElement(api_request, 'credentials',
                                            name=auth_value,
                                            password=auth_secret)
    elif auth_method.upper() == 'TOKEN':
        credentials_element = ET.SubElement(api_request, 'credentials',
                                            personalAccessTokenName=auth_value,
                                            personalAccessTokenSecret=auth_secret)

    ET.SubElement(credentials_element, 'site', contentUrl=site_url_namespace)
    api_request = ET.tostring(api_request)

    api_response = requests.post(sign_in_url,
                                 data=api_request,
                                 verify=verify_ssl)

    if api_response.status_code != 200:
        error_code, summary, detail = format_error(
            ET.fromstring(api_response.content))
        raise Exception(
            f"Error signing into site '{site_url_namespace}\n"
            f"Error: {error_code}\nSummary: {summary}\nDetail: {detail}")

    else:
        auth_token = ET.fromstring(api_response.content).find(
            './/t:credentials', namespaces=NAMESPACE).attrib['token']

        return auth_token


def api_sign_out(server_url: str, auth_token: str, site_url_namespace: str,
                 verify_ssl: str):
    """Sign out of the Tableau Server Site.

    Args:
        server_url (str): Tableau Server API URL.
        auth_token (str): REST API credentials token.
        site_url_namespace (str): Tableau Server Site name as it appears
            in the URL.
        verify_ssl (str): Path to HTTPS cert. False if HTTP Request will be sent.

    """
    sign_out_url = f"{server_url}/auth/signout"

    api_response = requests.post(sign_out_url,
                                 headers={'x-tableau-auth': auth_token},
                                 verify=verify_ssl)

    if api_response.status_code != 204:
        error_code, summary, detail = format_error(
            ET.fromstring(api_response.content))
        raise Exception(
            f"Error signing out of site '{site_url_namespace}\n"
            f"Error: {error_code}\nSummary: {summary}\nDetail: {detail}")


def format_error(response: object) -> tuple:
    """Format the error body of a failed API call.

    Args:
        response (object): Response body of failed API call.

    Returns:
        tuple: Error Code, Error Summary, Error Details

    """
    error_element = response.find('.//t:error', namespaces=NAMESPACE)

    code = error_element.attrib['code']
    summary = error_element.find('.//t:summary', namespaces=NAMESPACE).text
    detail = error_element.find('.//t:detail', namespaces=NAMESPACE).text

    return code, summary, detail


if __name__ == '__main__':
    main()
