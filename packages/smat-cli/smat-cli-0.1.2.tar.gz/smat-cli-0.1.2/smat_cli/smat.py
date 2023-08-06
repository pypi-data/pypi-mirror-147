"""
SMAT API access.
"""

from datetime import datetime
from typing import Iterator

import requests


class SmatError(Exception):
    pass


class InvalidSiteError(SmatError):
    pass


class InvalidIntervalError(SmatError):
    pass


class FailedRequestError(SmatError):
    pass


class Smat:
    """
    Class to handle SMAT API calls.
    """

    def __init__(self):
        self.base_url = "https://api.smat-app.com"
        self.sites = [
            "telegram",
            "rumble_video",
            "rumble_comment",
            "bitchute_video",
            "bitchute_comment",
            "lbry_video",
            "lbry_comment",
            "8kun",
            "4chan",
            "gab",
            "parler",
            "win",
            "poal",
            "kiwifarms",
            "gettr",
            "wimkin",
            "mewe",
            "minds",
            "vk",
        ]
        self.intervals = [
            "hour",
            "day",
            "week",
            "month",
            "year",
        ]

    def content(
        self,
        term: str,
        limit: int,
        site: str,
        since: datetime,
        until: datetime,
        esquery: bool = True,
        sortdesc: bool = False,
    ) -> dict:
        """
        Query the /content endpoint of the SMAT API and return results as a dict of the JSON response.

        :param term: str
        :param limit: int
        :param site: str
        :param since: datetime.datetime
        :param until: datetime.datetime
        :param esquery: bool
        :param sortdesc: bool
        :return: dict
        """
        validated_site = self.validate_site(site)
        endpoint = "/content"
        response = requests.get(
            self.base_url + endpoint,
            params={
                "term": term,
                "limit": limit,
                "site": validated_site,
                "since": since,
                "until": until,
                "esquery": esquery,
                "sortdesc": sortdesc,
            },
        )
        return self._handle_response(response)

    def timeseries(
        self,
        term: str,
        interval: str,
        site: str,
        since: datetime,
        until: datetime,
        esquery: bool = True,
        changepoint: bool = False,
    ) -> dict:
        """
        Query the /timeseries endpoint of the SMAT API and return results as a dict of the JSON response. Note:
        currently can not do changepoints.

        :param term: str
        :param interval: str
        :param site: str
        :param since: datetime.datetime
        """
        # TODO: implement a way to do changepoints

        validated_site = self.validate_site(site)
        validated_interval = self.validate_interval(interval)
        endpoint = "/timeseries"
        response = requests.get(
            self.base_url + endpoint,
            params={
                "term": term,
                "interval": validated_interval,
                "site": validated_site,
                "since": since,
                "until": until,
                "esquery": esquery,
                "changepoint": changepoint,
            },
        )
        return self._handle_response(response)

    def activity(
        self,
        term: str,
        agg_by: str,
        site: str,
        since: datetime,
        until: datetime,
        esquery: bool = True,
    ) -> dict:
        """
        Query the /activity endpoint of the SMAT API and return results as a dict of the JSON response.

        :param term: str
        :param agg_by: str
        :param site: str
        :param since: datetime.datetime
        :param until: datetime.datetime
        :param esquery: bool
        :return: dict
        """
        validated_site = self.validate_site(site)
        endpoint = "/activity"
        response = requests.get(
            self.base_url + endpoint,
            params={
                "term": term,
                "agg_by": agg_by,
                "site": validated_site,
                "since": since,
                "until": until,
                "esquery": esquery,
            },
        )
        return self._handle_response(response)

    def validate_site(self, site: str) -> str:
        """
        Raises exception if the provided site does not exist in the list of valid sites, otherwise return the site
        provided.

        :param site: str
        :return: str
        """
        if site not in self.sites:
            raise InvalidSiteError(
                f"{site} is an invalid site. Valid sites are: {', '.join(sorted(self.sites))}"
            )
        return site

    def validate_interval(self, interval):
        """
        Raises exception if the provided interval does not exist in the list of valid intervals, otherwise return the
        interval provided.

        :param interval: str
        :return: str
        """
        if interval not in self.intervals:
            raise InvalidIntervalError(
                f"{interval} is an invalid interval. Valid intervals are: {', '.join(sorted(self.intervals))}"
            )
        return interval

    def _handle_response(self, response):
        if response.status_code == 200:
            return response.json()
        else:
            raise FailedRequestError(
                f"Failed request [{response.status_code}]: {response.text}"
            )
