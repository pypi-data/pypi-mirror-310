import os
import sys
import requests
import argparse
import json
from collections import Counter

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

EX_CONFIG = 78

# Set vars for connection
url = os.getenv('FORTIFY_URL') or eprint('FORTIFY_URL not set')
token = os.getenv('FORTIFY_TOKEN') or eprint('FORTIFY_TOKEN not set')

if url is None or token is None or url == "" or token == "":
    eprint('FORTIFY_URL or FORTIFY_TOKEN not set')
    sys.exit(EX_CONFIG)

default_id = "d4e30a50-d849-4ca4-bcd3-8415b7d586be"  # NOT A SECRET VALUE, SIMPLY A STATIC ID

def get_application_ids(app_name: str) -> list:
    response = requests.get(f"{url}/api/v1/projects", params={'q': f"name:\"*{app_name}*\""},
                            headers={'Authorization': f'FortifyToken {token}'})
    return [ (app['id'], app['name']) for app in response.json()['data']]

def get_version_id(app_id: int, version_name: str) -> int:
    response = requests.get(f"{url}/api/v1/projects/{app_id}/versions/", params={'q': f"name:\"{version_name}\""},
                            headers={'Authorization': f'FortifyToken {token}'})
    return [version['id'] for version in response.json()['data']]

def get_issues(version_id: int,severity: str) -> list:
    # TODO: consider making the list of reasons to ignore a parameter (not yet done as to prevent abuse in first rollout)
    reasons_to_ignore = ['Not an Issue (false positive)', 'Ignore (non-project file)']
    response = requests.get(f"{url}/api/v1/projectVersions/{version_id}/issues",params={'q': f"[fortify priority order]:{severity}", 'qm': 'issues'},
                            headers={'Authorization': f'FortifyToken {token}'})
    return [issue for issue in response.json()['data'] if issue['primaryTag'] not in reasons_to_ignore]

# TODO: right now results are tied to a particular representation (slack blocks). Generalize to txt, slack, html, etc.
def collate_results(app_prefix, version_name) -> json:
    session = requests.Session()
    session.headers.update({'Content-Type': 'application/json'})
    results = [ {"type": "section", "text": {"type": "mrkdwn", "text":"*Fortify Findings*"}}]
    kingdoms = []
    all_versions_as_mkdown = ""
    all_kingdoms_as_mkdown = ""
    num_critical = 0
    num_high = 0
    app_names = [app[1] for app in get_application_ids(app_prefix)]
    longest_name_len = len(max(app_names,key=len, default=""))

    for app in get_application_ids(app_prefix):
        for version_id in get_version_id(app[0], version_name):
            high_issues = get_issues(version_id,'high')
            kingdoms.extend([issue['kingdom'] for issue in high_issues])
            num_high += len(high_issues)

            critical_issues = get_issues(version_id,'critical')
            kingdoms.extend([issue['kingdom'] for issue in critical_issues])
            num_critical += len(critical_issues)

            padding = longest_name_len - len(app[1]) + 1
            if len(high_issues) + len(critical_issues) > 0:
                all_versions_as_mkdown += f"<{url}/html/ssc/version/{version_id}/audit?filterset=1305a447-8d82-4971-a830-f94b2f0f190f&orderby=friority&viewTab=code|{app[1]}>" + " " * padding + f"{len(critical_issues):>2} critical {len(high_issues):>3} high" + "\n"

    kingdoms_counter = Counter(kingdoms)
    for i in kingdoms_counter:
        all_kingdoms_as_mkdown += f"{kingdoms_counter[i]} {i}\n"
    results.append({"type": "section", "text": {"type": "mrkdwn", "text": all_versions_as_mkdown}})
    results.append({"type": "section", "text": {"type": "mrkdwn", "text": all_kingdoms_as_mkdown}})

    return json.dumps(results,indent=2), num_critical+num_high > 0

def cli():
    """
    Parse command line arguments and invoke get_or_create_application_version
    """
    jid_desc = "PDG_XXXXXX - identifier added to version description, used to synchronized with dashboard. Please set manually if not set upon creation. Consult #rdsec with this message if needed."
    parser = argparse.ArgumentParser(
        description="""Print Fortify application and version ids of given fortify application name and version names. Create version and application if they don't exist.
        Requires environment variables 'FORTIFY_TOKEN' and 'FORTIFY_URL' to be set.  
        FORTIFY_TOKEN must be an token for a (service) account capable of searching across all projects, otherwise results will be limited.
        FORTIFY_URL is the base url for the fortify service (e.g. https://codescan-ssc.mycompany.com/ssc) . It does not include the path to the api endpoing e.g. 'api/v1'. 
        """)
    parser.add_argument("app_prefix", help="application search prefix")
    parser.add_argument("version_prefix", help="version search prefix")
    args = parser.parse_args()
    try:
        results, should_output = collate_results(args.app_prefix, args.version_prefix)
        if should_output:
            print(results)
        else:
            eprint("No critical or high issues found. Not outputting results to stdin")
    except Exception as e:
        eprint(e)
        sys.exit(EX_CONFIG)

if __name__ == '__main__':
    cli()
