#----- Connecting to a Scratch account

import json
import re
import requests

import ._user
import ._cloud
import ._project

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    "x-csrftoken": "a",
    "x-requested-with": "XMLHttpRequest",
    "referer": "https://scratch.mit.edu",
}

class Session():

    def __init__(self, session_id):

        self.session_id = session_id
        self._headers = headers
        self._cookies = {
            "scratchsessionsid" : self.session_id,
            "scratchcsrftoken" : "a",
            "scratchlanguage" : "en",
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        self._get_xtoken()

    def _get_csrftoken(self):
        r = requests.get("https://scratch.mit.edu/csrf_token/").headers
        print(r)
        csrftoken = r["Set-Cookie"].split("scratchcsrftoken=")[1].split(";")[0]
        self._headers["x-csrftoken"] = csrftoken
        self._cookies["scratchcsrftoken"] = csrftoken

    def _get_xtoken(self):

        # this will fetch the account token
        response = json.loads(requests.post(
            "https://scratch.mit.edu/session",
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
                "x-csrftoken": "a",
                "x-requested-with": "XMLHttpRequest",
                "referer": "https://scratch.mit.edu",
            },
            cookies = {
                "scratchsessionsid" : self.session_id,
                "scratchcsrftoken" : "a",
                "scratchlanguage" : "en"
            }
        ).text)

        self.xtoken = response['user']['token']
        self._headers["X-Token"] = self.xtoken
        self.email = response["user"]["email"]
        self.new_scratcher = response["permissions"]["new_scratcher"]
        self.mute_status = response["permissions"]["mute_status"]
        self._username = response["user"]["username"]

    def get_linked_user(self):

        #this will fetch the user who is associated to the session
        if not "_user" in self.__dict__:
            self._user = _user.get_user(self._username)
        return self._user

    def mystuff_projects(self, keyword, *, page=1, sort_by=""):

        targets = requests.get(
            f"https://scratch.mit.edu/site-api/projects/{keyword}/?page={page}&ascsort=&descsort={sort_by}",
            headers = headers,
            cookies = self._cookies,
        ).json()
        projects = []
        for target in targets:
            projects.append(
                dict(
                    author = self._username,
                    created = target["fields"]["datetime_created"],
                    last_modified = target["fields"]["datetime_modified"],
                    share_date = target["fields"]["datetime_shared"],
                    shared = target["fields"]["isPublished"],
                    id = target["pk"],
                    thumbnail_url = "https://uploads.scratch.mit.edu"+target["fields"]["uncached_thumbnail_url"][1:],
                    favorites = target["fields"]["favorite_count"],
                    loves = target["fields"]["love_count"],
                    remixes = target["fields"]["remixers_count"],
                    views = target["fields"]["view_count"],
                    thumbnail_name = target["fields"]["thumbnail"],
                    title = target["fields"]["title"],
                    url = "https://scratch.mit.edu/projects/" + str(target["pk"]),
                    comment_count = target["fields"]["commenters_count"],
                )
            )
        return projects

    def messages(self, *, limit=40, offset=0):

        return requests.get(
            f"https://api.scratch.mit.edu/users/{self._username}/messages?limit={limit}&offset={offset}",
            headers = self._headers,
            cookies = self._cookies,
        ).json()

    def clear_messages(self):

        return requests.post(
            "https://scratch.mit.edu/site-api/messages/messages-clear/",
            headers = self._headers,
            cookies = self._cookies,
        ).text

    def message_count(self):

        return json.loads(requests.get(f"https://api.scratch.mit.edu/users/{self._username}/messages/count/", headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.3c6 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',}).text)["count"]


    def connect_cloud(self, *, project_id):

        return _cloud.CloudConnection(username = self._username, session_id = self.session_id, project_id = int(project_id))


    def connect_user(self, username):
        try:
            user = _user.User(username=username, _session=self)
            user.update()
            return user
        except KeyError:
            return None

    def connect_project(self, project_id):
        try:
            project = _project.Project(id=int(project_id), _session=self)
            if not project.update():
                project = _project.PartialProject(id=int(project_id))
            return project
        except KeyError:
            return None


# ------ #

def login(username, password):
    data = json.dumps({"username": username, "password": password})
    request = requests.post(
        "https://scratch.mit.edu/login/", data=data, headers=headers
    )

    return Session(re.search('"(.*)"', request.headers["Set-Cookie"]).group())
