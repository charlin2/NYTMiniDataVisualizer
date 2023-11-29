import requests
import json
import datetime

def login(username: str, password: str) -> str:
    """Retrieve NYT account cookie

    Args:
        username (str): NYT account email
        password (str): NYT account password

    Raises:
        ValueError: Cookie cannot be found

    Returns:
        str: NYT-S cookie
    """
    login_resp = requests.post(
            'https://myaccount.nytimes.com/svc/ios/v2/login',
            data={
                'login': username,
                'password': password,
            },
            headers={
                'User-Agent': 'Crosswords/20191213190708 CFNetwork/1128.0.1 Darwin/19.6.0',
                'client_id': 'ios.crosswords',
            }
        )
    login_resp.raise_for_status()
    for cookie in login_resp.json()['data']['cookies']:
        if cookie['name'] == 'NYT-S':
            return cookie['cipheredValue']
    raise ValueError('NYT-S cookie not found')


def get_leaderboard_data(x: int, username=None, password=None, cookie=None) -> list:
    """Retrieves leaderboard data from the past x days

    Args:
        username (str): NYT account email
        password (str): NYT account password

    Returns:
        list: List of json objects containing leaderboard data from the past x days
    """
    dates = last_days(x)
    if cookie == None:
        cookie = login(username, password)
    leaderboard_data = {}
    for d in dates:
        resp = requests.get('https://www.nytimes.com/svc/crosswords/v6/leaderboard/mini/{date}.json'.format(date=str(d)), cookies={
                'NYT-S': cookie,
            },
        )
        json_object = json.loads(resp.text)
        leaderboard_data.update({str(d) : json_object})
    return leaderboard_data


def write_to_json(username, password, x):
    data = get_leaderboard_data(username, password, x)
    with open("./sample.json", "w") as outfile:
        json.dump(data, outfile, indent=4)


def last_days(x: int) -> list:
    """Returns a datetime list of the last x days from today

    Returns:
        list: datetime list
    """
    now = datetime.datetime.now()
    then = now - datetime.timedelta(x)
    dates = []
    for i in range(1, int((now - then).days) + 1):
        dates.append((then + datetime.timedelta(i)).date())
    return dates


def get_avg_ranks(data):
    rank_dict = {}
    num_occurrences = {}
    for key in data.keys():
        solvers = data[key]["data"]
        last_rank = 1
        for solver in solvers:
            rank_dict.setdefault(solver["name"], 0)
            num_occurrences.setdefault(solver["name"], 1)
            if "score" in solver.keys():
                if "rank" not in solver.keys():
                    rank_dict[solver["name"]] += int(last_rank)
                    num_occurrences[solver["name"]] += 1
                else:
                    rank_dict[solver["name"]] += int(solver["rank"])
                    num_occurrences[solver["name"]] += 1
                    last_rank = solver["rank"]
    for solver in rank_dict.keys():
        num_occurrences[solver] -= 1
        if num_occurrences[solver] != 0:
            rank_dict[solver] /= num_occurrences[solver]
    sorted_by_place = dict(sorted(num_occurrences.items(), key=(lambda x:x[1]), reverse=True))
    for solver in sorted_by_place.keys():
        print("Average place for " + solver + ": " + str(rank_dict[solver]) + "\n Minis completed: " + str(num_occurrences[solver]))
        if rank_dict[solver] != 0:
            print("Completed to Rank ratio: " + str(num_occurrences[solver]/rank_dict[solver]))
        else:
            print("This solver has not completed any puzzles this month!")
