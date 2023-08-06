"""
Label queries
"""

from typing import Generator, List, Optional, Union
import warnings

from typeguard import typechecked
import pandas as pd


from ...helpers import Compatible, format_result, fragment_builder
from ..asset import QueriesAsset
from ..project import QueriesProject
from .queries import gql_labels, GQL_LABELS_COUNT
from ...constants import NO_ACCESS_RIGHT
from ...types import Label as LabelType
from ...orm import Label
from ...utils import row_generator_from_paginated_calls


class QueriesLabel:
    """
    Set of Label queries
    """
    # pylint: disable=too-many-arguments,too-many-locals

    def __init__(self, auth):
        """
        Initializes the subclass

        Parameters
        ----------
        - auth : KiliAuth object
        """
        self.auth = auth

    # pylint: disable=dangerous-default-value
    @Compatible(['v1', 'v2'])
    @typechecked
    def labels(self,
               asset_id: Optional[str] = None,
               asset_status_in: Optional[List[str]] = None,
               asset_external_id_in: Optional[List[str]] = None,
               author_in: Optional[List[str]] = None,
               created_at: Optional[str] = None,
               created_at_gte: Optional[str] = None,
               created_at_lte: Optional[str] = None,
               fields: list = ['author.email', 'author.id', 'id',
                               'jsonResponse', 'labelType', 'secondsToLabel', 'skipped'],
               first: Optional[int] = None,
               honeypot_mark_gte: Optional[float] = None,
               honeypot_mark_lte: Optional[float] = None,
               id_contains: Optional[List[str]] = None,
               json_response_contains: Optional[List[str]] = None,
               label_id: Optional[str] = None,
               project_id: Optional[str] = None,
               skip: int = 0,
               skipped: Optional[bool] = None,
               type_in: Optional[List[str]] = None,
               user_id: Optional[str] = None,
               disable_tqdm: bool = False,
               as_generator: bool = False,
               ) -> Union[List[dict], Generator[dict, None, None]]:
        # pylint: disable=line-too-long
        """
        Gets a label list or a label generator from a project based on a set of criteria

        Parameters
        ----------
        - asset_id : str, optional (default = None)
            Identifier of the asset.
        - asset_status_in : list of str, optional (default = None)
            Returned labels should have a status that belongs to that list, if given.
            Possible choices : {'TODO', 'ONGOING', 'LABELED', 'REVIEWED'}
        - asset_external_id_in : list of str, optional (default = None)
            Returned labels should have an external id that belongs to that list, if given.
        - author_in : list of str, optional (default = None)
            Returned labels should have a label whose status belongs to that list, if given.
        - created_at : string, optional (default = None)
            Returned labels should have a label whose creation date is equal to this date.
            Formatted string should have format : "YYYY-MM-DD"
        - created_at_gt : string, optional (default = None)
            Returned labels should have a label whose creation date is greater than this date.
            Formatted string should have format : "YYYY-MM-DD"
        - created_at_lt : string, optional (default = None)
            Returned labels should have a label whose creation date is lower than this date.
            Formatted string should have format : "YYYY-MM-DD"
        - fields : list of string, optional (default = ['author.email', 'author.id',
            'id', 'jsonResponse', 'labelType', 'secondsToLabel', 'skipped'])
            All the fields to request among the possible fields for the labels.
            See [the documentation](https://cloud.kili-technology.com/docs/python-graphql-api/graphql-api/#label) for all possible fields.
        - first : int, optional (default = None)
            Maximum number of labels to return.
        - honeypot_mark_gt : float, optional (default = None)
            Returned labels should have a label whose honeypot is greater than this number.
        - honeypot_mark_lt : float, optional (default = None)
            Returned labels should have a label whose honeypot is lower than this number.
        - id_contains : list of str, optional (default = None)
            Filters out labels not belonging to that list. If empty, no filtering is applied.
        - json_response_contains : list of str, optional (default = None)
            Returned labels should have a substring of the jsonResponse that belongs
            to that list, if given.
        - label_id : str
            Identifier of the label.
        - project_id : str
            Identifier of the project.
        - skip : int, optional (default = None)
            Number of labels to skip (they are ordered by their date of creation, first to last).
        - skipped : bool, optional (default = None)
            Returned labels should have a label which is skipped
        - type_in : list of str, optional (default = None)
            Returned labels should have a label whose type belongs to that list, if given.
        - user_id : str
            Identifier of the user.
        - disable_tqdm : bool, (default = False)
        - as_generator: bool, (default = False)
            If True, a generator on the labels is returned.


        Returns
        -------
        - a result object which contains the query if it was successful, else an error message.

        Examples
        -------
        >>> kili.labels(project_id=project_id, fields=['jsonResponse', 'labelOf.externalId']) # returns a list of all labels of a project and their assets external ID
        >>> kili.labels(project_id=project_id, fields=['jsonResponse'], as_generator=True) # returns a generator of all labels of a project
        """
        if as_generator is False:
            warnings.warn("From 2022-05-18, the default return type will be a generator. Currently, the default return type is a list. \n"
                          "If you want to force the query return to be a list, you can already call this method with the argument as_generator=False",
                          DeprecationWarning)

        saved_args = locals()
        count_args = {
            k: v
            for (k, v) in saved_args.items()
            if k
            not in [
                'as_generator',
                'disable_tqdm',
                'fields',
                'first',
                'id_contains',
                'self',
                'skip',
            ]
        }

        # using tqdm with a generator is messy, so it is always disabled
        disable_tqdm = disable_tqdm or as_generator

        payload_query = {
            'where': {
                'id': label_id,
                'asset': {
                    'id': asset_id,
                    'externalIdIn': asset_external_id_in,
                    'statusIn': asset_status_in,
                },
                'project': {
                    'id': project_id,
                },
                'user': {
                    'id': user_id,
                },
                'createdAt': created_at,
                'createdAtGte': created_at_gte,
                'createdAtLte': created_at_lte,
                'authorIn': author_in,
                'honeypotMarkGte': honeypot_mark_gte,
                'honeypotMarkLte': honeypot_mark_lte,
                'idIn': id_contains,
                'jsonResponseContains': json_response_contains,
                'skipped': skipped,
                'typeIn': type_in,
            },
        }

        labels_generator = row_generator_from_paginated_calls(
            skip,
            first,
            self.count_labels,
            count_args,
            self._query_labels,
            payload_query,
            fields,
            disable_tqdm
        )

        if as_generator:
            return labels_generator
        return list(labels_generator)

    def _query_labels(self,
                      skip: int,
                      first: int,
                      payload: dict,
                      fields: List[str]):

        payload.update({'skip': skip, 'first': first})
        _gql_labels = gql_labels(fragment_builder(fields, LabelType))
        result = self.auth.client.execute(_gql_labels, payload)
        return format_result('data', result, Label)

    @staticmethod
    def parse_json_response_for_single_classification(json_response):
        """
        Parameters
        -------
        - json_response : dict
            A valid JSON response

        Returns
        -------
        - the names of categories from a json_response, for a single-class classification task
        """
        categories = QueriesLabel.parse_json_response_for_multi_classification(
            json_response)
        if len(categories) == 0:
            return []

        return categories[0]

    @staticmethod
    def parse_json_response_for_multi_classification(json_response):
        """
        Parameters
        -------
        - json_response : dict
            A valid JSON response

        Returns
        -------
        - the names of categories from a json_response, for a multi-class classification task
        """
        # pylint: disable=eval-used
        formatted_json_response = eval(
            json_response)
        if 'categories' not in formatted_json_response:
            return []
        categories = formatted_json_response['categories']
        return list(map(lambda category: category['name'], categories))

    @staticmethod
    def parse_json_response(json_response, interface_category):
        """
        Parameters
        -------
        - json_response : dict
            A valid JSON response
        - interface_category: str
            A valid interface category

        Returns
        -------
        - the names of categories from a json_response
        """
        if interface_category == 'SINGLECLASS_TEXT_CLASSIFICATION':
            return QueriesLabel.parse_json_response_for_single_classification(json_response)
        if interface_category == 'MULTICLASS_TEXT_CLASSIFICATION':
            return QueriesLabel.parse_json_response_for_multi_classification(json_response)

        return json_response

    # pylint: disable=dangerous-default-value
    @typechecked
    def export_labels_as_df(self,
                            project_id: str,
                            fields: list = [
                                'author.email',
                                'author.id',
                                'createdAt',
                                'id',
                                'labelType',
                                'skipped'
                            ],
                            asset_fields: list = [
                                'externalId'
                            ]):
        # pylint: disable=line-too-long
        """
        Get the labels of a project as a pandas DataFrame

        Parameters
        ----------
        - project_id : str
        - fields : list of string, optional (default = ['author.email', 'author.id',
            'id', 'jsonResponse', 'labelType', 'secondsToLabel', 'skipped'])
            All the fields to request among the possible fields for the labels.
            See [the documentation](https://cloud.kili-technology.com/docs/python-graphql-api/graphql-api/#label) for all possible fields.
        - asset_fields : list of string, optional (default = ['external_id'])
            All the fields to request among the possible fields for the assets.
            See [the documentation](https://cloud.kili-technology.com/docs/python-graphql-api/graphql-api/#asset) for all possible fields.

        Returns
        -------
        - labels_df : pandas DataFrame containing the labels.
        """
        projects = QueriesProject(self.auth).projects(project_id)
        assert len(projects) == 1, NO_ACCESS_RIGHT
        project = projects[0]
        if 'interfaceCategory' not in project:
            return pd.DataFrame()

        interface_category = project['interfaceCategory']
        assets = QueriesAsset(self.auth).assets(
            project_id=project_id, fields=asset_fields + ['labels.' + field for field in fields])
        labels = [dict(label, **dict((f'asset_{key}', asset[key]) for key in asset if key != 'labels'))
                  for asset in assets for label in asset['labels']]
        labels_df = pd.DataFrame(labels)
        if 'jsonResponse' in labels_df.columns:
            labels_df['jsonResponse'] = labels_df['jsonResponse'].apply(
                lambda json_response: QueriesLabel.parse_json_response(json_response, interface_category))
        return labels_df

    @Compatible(['v1', 'v2'])
    @typechecked
    def count_labels(self,
                     asset_id: Optional[str] = None,
                     asset_status_in: Optional[List[str]] = None,
                     asset_external_id_in: Optional[List[str]] = None,
                     author_in: Optional[List[str]] = None,
                     created_at: Optional[str] = None,
                     created_at_gte: Optional[str] = None,
                     created_at_lte: Optional[str] = None,
                     honeypot_mark_gte: Optional[float] = None,
                     honeypot_mark_lte: Optional[float] = None,
                     json_response_contains: Optional[List[str]] = None,
                     label_id: Optional[str] = None,
                     project_id: Optional[str] = None,
                     skipped: Optional[bool] = None,
                     type_in: Optional[List[str]] = None,
                     user_id: Optional[str] = None):
        # pylint: disable=line-too-long
        """
        Get the number of labels for the given parameters

        Parameters
        ----------
        - asset_id : str
            Identifier of the asset.
        - asset_status_in : list of str, optional (default = None)
            Returned labels should have a status that belongs to that list, if given.
            Possible choices : {'TODO', 'ONGOING', 'LABELED', 'REVIEWED'}
        - asset_external_id_in : list of str, optional (default = None)
            Returned labels should have an external id that belongs to that list, if given.
        - author_in : list of str, optional (default = None)
            Returned labels should have a label whose status belongs to that list, if given.
        - created_at : string, optional (default = None)
            Returned labels should have a label whose creation date is equal to this date.
            Formatted string should have format : "YYYY-MM-DD"
        - created_at_gt : string, optional (default = None)
            Returned labels should have a label whose creation date is greater than this date.
            Formatted string should have format : "YYYY-MM-DD"
        - created_at_lt : string, optional (default = None)
            Returned labels should have a label whose creation date is lower than this date.
            Formatted string should have format : "YYYY-MM-DD"
        - fields : list of string, optional (default = ['author.email', 'author.id',
            'id', 'jsonResponse', 'labelType', 'secondsToLabel', 'skipped'])
            All the fields to request among the possible fields for the labels.
            See [the documentation](https://cloud.kili-technology.com/docs/python-graphql-api/graphql-api/#asset) for all possible fields.
        - honeypot_mark_gt : float, optional (default = None)
            Returned labels should have a label whose honeypot is greater than this number.
        - honeypot_mark_lt : float, optional (default = None)
            Returned labels should have a label whose honeypot is lower than this number.
        - json_response_contains : list of str, optional (default = None)
            Returned labels should have a substring of the jsonResponse that
            belongs to that list, if given.
        - label_id : str
            Identifier of the label.
        - project_id : str
            Identifier of the project.
        - skipped : bool, optional (default = None)
            Returned labels should have a label which is skipped
        - type_in : list of str, optional (default = None)
            Returned labels should have a label whose type belongs to that list, if given.
        - user_id : str
            Identifier of the user.


        Returns
        -------
        - the number of labels with the parameters provided
        """
        variables = {
            'where': {
                'id': label_id,
                'asset': {
                    'id': asset_id,
                    'externalIdIn': asset_external_id_in,
                    'statusIn': asset_status_in,
                },
                'project': {
                    'id': project_id,
                },
                'user': {
                    'id': user_id,
                },
                'createdAt': created_at,
                'createdAtGte': created_at_gte,
                'createdAtLte': created_at_lte,
                'authorIn': author_in,
                'honeypotMarkGte': honeypot_mark_gte,
                'honeypotMarkLte': honeypot_mark_lte,
                'jsonResponseContains': json_response_contains,
                'skipped': skipped,
                'typeIn': type_in,
            }
        }
        result = self.auth.client.execute(GQL_LABELS_COUNT, variables)
        count = format_result('data', result)
        return count
