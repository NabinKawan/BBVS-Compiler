import click
from datetime import datetime, timedelta
import json
import ast


def load_json():
    with open("contract_data.json") as f:
        return json.load(f)


def write_json(new_data, key, file_name="contract_data.json"):
    with open(file_name, 'r+') as file:
        file_data = json.load(file)
        file_data[key].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)
        file.close()


# initialize votecount of each candidate
def initialize_votecount():
    with open("contract_data.json", 'r+') as file:
        file_data = json.load(file)

        for i in range(len(file_data['candidates'])):
            cand_id = file_data['candidates'][i]['candidate_id']
            votes_count = {cand_id: 0}  # in dict form
            # file_data['votes_count'][cand_id] = 0
            file_data['votes_count'].update(votes_count)

        file_data["total_votes"] = 0
        file.truncate(0)
        file.seek(0)
        json.dump(file_data, file, indent=4)


def set_voter_status():
    with open("contract_data.json", 'r+') as file:
        file_data = json.load(file)

        for i in range(len(file_data["voters"])):
            file_data["voters"][i]["has_voted"] = False
            file_data["total_votes"] = 0
            file_data["voters"][i]["voted_to"] = []

        file.truncate(0)
        file.seek(0)
        json.dump(file_data, file, indent=4)


def is_voter_available(voter_id):
    status = False
    file_data = load_json()
    for i in range(len(file_data["voters"])):
        if (file_data["voters"][i]["voter_id"] == voter_id):
            status = True
            break
    if status:
        return True
    else:
        print(f"Voter_id: {voter_id} not available")
        raise Exception(f"Voter_id: {voter_id} not available")


def is_candidate_available(candidate_ids):
    list_candidate_ids = candidate_ids.strip('][').split(',' or ', ')
    status = False

    file_data = load_json()
    for cand_id in list_candidate_ids:

        for i in range(len(file_data["candidates"])):
            if (file_data["candidates"][i]["candidate_id"] == cand_id):
                status = True
                break
            else:
                status = False
            # print(f"{cand_id}: {status}")

        if status == False:
            print(f"Candidate_id: {cand_id} not available")
            raise Exception(f"Candidate_id: {cand_id} not available")
            # break

    if status:
        return True


def has_already_voted(voter_id):
    status = False
    file_data = load_json()
    for i in range(len(file_data["voters"])):
        if (file_data["voters"][i]["voter_id"] == voter_id):
            if (file_data["voters"][i]["has_voted"] == False):
                status = True
                break
    if status == True:
        return True
    else:
        print("Voter has already voted")
        raise Exception("Voter has already voted")


# check to start election, if candidates and voters are available or not
def are_members_available():
    file_data = load_json()
    if (len(file_data['candidates']) != 0 and len(file_data['voters']) != 0):
        return True
    else:
        if len(file_data['candidates']) == 0:
            print("Candidates are not available")
            raise Exception("Candidates are not available")
        elif len(file_data['voters']) == 0:
            print("Voters are not available")
            raise Exception("Voters are not available")


def voting_line_open():
    file_data = load_json()
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    voting_end_time = datetime.strptime(file_data["voting_end_time"], date_format)
    if datetime.now() < voting_end_time:
        return True
    else:
        print("Voting session is closed")
        raise Exception("Voting session is closed")
        # return False


def spliter(str_param):
    return str_param.split(",")


def cleaner(list_element):
    member_list = []

    for element in list_element:
        new_val = element.replace("[[", "")
        new_val = new_val.replace("]]", "")

        if new_val.lower() == "true":
            new_val = True
        elif new_val.lower == "false":
            new_val = False

        try:
            new_val = ast.literal_eval(new_val)
        except:
            pass

        member_list.append(new_val)
    return member_list


def initialize_candidates(candidates):
    # print(f"candidate_list:", candidate_list)
    with open("contract_data.json", 'r+') as file:
        for element in candidates:
            candidate_detail = {"candidate_id": element[0], "name": element[1], "image_url": element[2],
                                "post": element[3], "logo": element[4]}

            write_json(candidate_detail, 'candidates')


def initialize_voters(voters):
    with open("contract_data.json", 'r+') as file:
        for element in voters:
            voter_detail = {"voter_id": element[0], "name": element[1], "voted_to": element[2], "has_voted": element[3]}

            write_json(voter_detail, 'voters')


def reset():
    with open("contract_data.json", 'r+') as file:
        file_data = json.load(file)
        # print(file_data.keys())
        file_data['candidates'].clear()
        file_data["voters"].clear()
        file_data["results"].clear()
        file_data["votes_count"].clear()
        file_data["election_name"] = " "
        file_data["total_votes"] = " "
        file_data["voting_start_time"] = " "
        file_data["voting_end_time"] = " "
        file.truncate(0)
        file.seek(0)
        json.dump(file_data, file, indent=4)


@click.group()
def cli():
    pass


@cli.command()
@click.option('--election', nargs=5, help="Provide Election name, End time, candidates[], voters[], posts[]")
def start_election(election):
    election_name, end_time, candidates, voters, posts = election
    voting_start_time = datetime.now()  # current time
    voting_end_time = voting_start_time + timedelta(minutes=int(end_time))

    # convert string to list form
    cand_list = candidates.split('],[')
    cand_l = map(spliter, cand_list)
    cand_l = list(cand_l)
    # print(cand_l)
    clean_candidates = list(map(cleaner, cand_l))
    print(f"clean_candidates: {clean_candidates}")

    voter_list = voters.split('],[')
    voter_l = map(spliter, voter_list)
    voter_l = list(voter_l)
    # print(voter_l)
    clean_voters = list(map(cleaner, voter_l))
    # print(f"clean_voters: {clean_voters}")

    reset()
    initialize_candidates(clean_candidates)
    initialize_voters(clean_voters)
    initialize_votecount()
    set_voter_status()
    if are_members_available():
        with open("contract_data.json", 'r+') as file:
            file_data = json.load(file)

            file_data['voting_start_time'] = str(voting_start_time)
            file_data['voting_end_time'] = str(voting_end_time)
            file_data['election_name'] = str(election_name)
            file.truncate(0)
            file.seek(0)
            json.dump(file_data, file, indent=4)

        print(file_data['election_name'])
        print(voting_start_time)

    # timestamp = datetime.timestamp(voting_end_time)
    # print("\ntimestamp :", timestamp + 5)
    # print("current : ", datetime.fromtimestamp(timestamp + 5))


@cli.command()
def get_remaining_time():
    file_data = load_json()
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    # datetime_obj = datetime.strptime(file_data["voting_end_time"], date_format)
    remaining_time = datetime.strptime(file_data["voting_end_time"], date_format) - datetime.now()
    if (remaining_time.days >= 0):
        print(remaining_time)
        return remaining_time
    else:
        print("Voting session is closed")
        raise Exception("Voting session is closed")


@cli.command()
def get_candidate_list():
    file_data = load_json()
    candidate_list = file_data["candidates"]
    print(candidate_list)
    return candidate_list


@cli.command()
def get_voter_list():
    file_data = load_json()
    voter_list = file_data["voters"]
    print(voter_list)
    return voter_list


# @cli.command()
# @click.option('--details', nargs=5, help=' candidate_id, name, image_url, post, logo')
# def add_candidates(details):
#     candidate_id, name, image_url, post, logo = details
#     candidate_detail = {"candidate_id": candidate_id, "name": name, "image_url": image_url, "post": post,"logo":logo}
#     write_json(candidate_detail, 'candidates')
#     print("Candidate added.")


# @cli.command()
# @click.option('--details', nargs=4, help='voter_id, name, voted_to, has_voted')
# # key = {"voter_id": "020","name": "nabin","voted_to": [ candidates list ],"has_voted": ""}
# def add_voters(details):
#     voter_id, name, voted_to, has_voted = details
#
#     list_voted_to = voted_to.strip('][').split(',' or ', ')  # converting to list
#     # print("final list", list_voted_to)
#     print(list_voted_to)
#     voter_detail = {"voter_id": voter_id, "name": name, "voted_to": list_voted_to, "has_voted": has_voted}
#     write_json(voter_detail, 'voters')


@cli.command()
def get_voters_count():
    file_data = load_json()
    voter_list = file_data['voters']
    print(len(voter_list))
    return len(voter_list)


@cli.command()
def get_candidates_count():
    file_data = load_json()
    candidate_list = file_data['candidates']
    print(len(candidate_list))
    return len(candidate_list)


@cli.command()
def get_total_votes():
    file_data = load_json()
    total_votes = file_data['total_votes']
    print(total_votes)
    return total_votes


@cli.command()
def get_election_name():
    file_data = load_json()
    election_name = file_data['election_name']
    print(election_name)
    return election_name


@cli.command()
@click.option("--voter", help="provide voter_id")
def get_voter_status(voter):
    if voting_line_open():
        voter_id = voter
        file_data = load_json()
        if is_voter_available(voter_id):
            for i in range(len(file_data['voters'])):
                if file_data['voters'][i]['voter_id'] == voter_id:
                    voter_status = file_data['voters'][i]['has_voted']
                    if voter_status:
                        print(f'Voter {voter_id} already voted')
                        raise Exception("Voter already voted")
        return file_data['voters'][i]['has_voted']


@cli.command()
def get_end_time():
    file_data = load_json()
    # end_time = file_data['voting_end_time']
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    end_time = datetime.strptime(file_data["voting_end_time"], date_format)
    timestamp = datetime.timestamp(end_time)
    print(timestamp)
    return timestamp


@cli.command()
@click.option('--vote', nargs=2, help="provide: voter_id, candidate_ids[]")
def do_vote(vote):
    voter_id, candidate_ids = vote
    candidate_ids = candidate_ids.replace('"', "")
    # voting lines open
    # is eligible vote
    if (voting_line_open() and is_voter_available(voter_id) and is_candidate_available(
            candidate_ids) and has_already_voted(voter_id)):
        with open("contract_data.json", 'r+') as file:
            file_data = json.load(file)

            list_candidate_ids = candidate_ids.strip('][').split(',' or ', ')  # converting to list
            # write voted candidates list
            for i in range(len(file_data['voters'])):
                if file_data['voters'][i]['voter_id'] == voter_id:
                    file_data['voters'][i]['voted_to'] = list_candidate_ids
                    file_data['voters'][i]['has_voted'] = True

            # write votes count of each candidate
            for cand_id in list_candidate_ids:
                if cand_id == " ":
                    vote_count = file_data['votes_count'][cand_id]
                else:
                    vote_count = file_data['votes_count'][cand_id]
                    file_data['votes_count'][cand_id] = vote_count + 1

            file_data["total_votes"] = file_data["total_votes"] + 1
            file.truncate(0)
            file.seek(0)
            print(file_data)
            json.dump(file_data, file, indent=4)
            print("vote done !!")


@cli.command()
def get_results():
    if voting_line_open():
        print("Voting session is going on. Wait !!")
        raise Exception("Voting session is going on. Wait !!")
    else:
        file_data = load_json()

        for i in range(len(file_data["candidates"])):
            cand_id = file_data["candidates"][i]["candidate_id"]
            result = {
                "name": file_data["candidates"][i]["name"],
                "candidate_id": file_data["candidates"][i]["candidate_id"],
                "image_url": file_data["candidates"][i]["image_url"],
                "post": file_data["candidates"][i]["post"],
                "votecount": file_data["votes_count"][cand_id],
                "logo": file_data["candidates"][i]["logo"]
            }
            print(result)
            write_json(result, "results")
        print(file_data["results"])
        return file_data["results"]


cli()
