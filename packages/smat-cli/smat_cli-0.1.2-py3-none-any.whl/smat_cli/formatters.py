"""
Formatters for SMAT API responses.
"""
import json
from abc import ABC, abstractmethod
from typing import Iterable


class ResponseFormatter(ABC):
    """
    Abstract base class for a formatter.

    Subclasses should override content, timeseries, and activity methods and should return iterables of strings.
    """

    def __init__(self, data: dict) -> None:
        self.data = data

    @abstractmethod
    def content(self) -> Iterable[str]:
        raise NotImplementedError

    @abstractmethod
    def timeseries(self) -> Iterable[str]:
        raise NotImplementedError

    @abstractmethod
    def activity(self, agg_by) -> Iterable[str]:
        raise NotImplementedError


class NdjsonFormatter(ResponseFormatter):
    """
    Ndjson formatter.
    """

    def content(self) -> Iterable[str]:
        results = []
        for hit in self.data["hits"]["hits"]:
            results.append(json.dumps(hit["_source"]))
        return results

    def timeseries(self) -> Iterable[str]:
        results = []
        for hit in self.data["aggregations"]["date"]["buckets"]:
            results.append(json.dumps(hit))
        return results

    def activity(self, agg_by) -> Iterable[str]:
        results = []
        for hit in self.data["aggregations"][agg_by]["buckets"]:
            results.append(json.dumps(hit))
        return results


class JsonFormatter(ResponseFormatter):
    """
    Json formatter.
    """

    def content(self) -> Iterable[str]:
        results = []
        for hit in self.data["hits"]["hits"]:
            results.append(hit["_source"])
        return [json.dumps(dict(results=results))]

    def timeseries(self) -> Iterable[str]:
        results = []
        for hit in self.data["aggregations"]["date"]["buckets"]:
            results.append(hit)
        changepoint = self.data["aggregations"].get("changepoint", {})
        return [json.dumps(dict(results=results, changepoint=changepoint))]

    def activity(self, agg_by) -> Iterable[str]:
        results = []
        for hit in self.data["aggregations"][agg_by]["buckets"]:
            results.append(hit)
        return [json.dumps(dict(results=results))]
