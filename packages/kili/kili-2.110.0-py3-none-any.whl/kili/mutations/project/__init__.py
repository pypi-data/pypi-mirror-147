"""
Project mutations
"""

from json import dumps
from typing import Optional

from typeguard import typechecked

from ...helpers import Compatible, format_result
from ...queries.asset import QueriesAsset
from ...queries.project import QueriesProject
from .helpers import verify_argument_ranges
from .queries import (GQL_APPEND_TO_ROLES,
                      GQL_CREATE_PROJECT,
                      GQL_DELETE_FROM_ROLES,
                      GQL_DELETE_PROJECT,
                      GQL_PROJECT_DELETE_ASYNCHRONOUSLY,
                      GQL_MAKE_PROJECT_PUBLIC,
                      GQL_GQL_UPDATE_PROPERTIES_IN_PROJECT_USER,
                      GQL_UPDATE_PROPERTIES_IN_PROJECT,
                      GQL_UPDATE_PROPERTIES_IN_ROLE)


class MutationsProject:

    """
    Set of Project mutations
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

    @Compatible(['v1', 'v2'])
    @typechecked
    def append_to_roles(self, project_id: str, user_email: str, role: str = 'LABELER'):
        """
        Add a user to a project

        If the user does not exist in your organization, he/she is invited and added
        both to your organization and project. This function can also be used to change
        the role of the user in the project.

        Parameters
        ----------
        - project_id : str
            Id of the project.
        - user_email : str
            The email of the user. This email is used as the unique identifier of the user.
        - role : str, optional (default = 'LABELER')
            One of {"ADMIN", "TEAM_MANAGER", "REVIEWER", "LABELER"}.

        Returns
        -------
        - a result object which indicates if the mutation was successful, or an error message else.

        Examples
        -------
        >>> kili.append_to_roles(project_id=project_id, user_email='john@doe.com')
        """
        variables = {
            'data': {'role': role,
                     'userEmail': user_email},
            'where': {'id': project_id}
        }
        result = self.auth.client.execute(GQL_APPEND_TO_ROLES, variables)
        return format_result('data', result)

    @Compatible(['v1', 'v2'])
    @typechecked
    def update_properties_in_project(self, project_id: str,
                                     consensus_mark: Optional[float] = None,
                                     consensus_tot_coverage: Optional[int] = None,
                                     description: Optional[str] = None,
                                     honeypot_mark: Optional[float] = None,
                                     instructions: Optional[str] = None,
                                     interface_category: str = 'IV2',
                                     input_type: Optional[str] = None,
                                     json_interface: Optional[dict] = None,
                                     min_consensus_size: Optional[int] = None,
                                     number_of_assets: Optional[int] = None,
                                     number_of_assets_with_empty_labels: Optional[int] = None,
                                     number_of_remaining_assets: Optional[int] = None,
                                     number_of_reviewed_assets: Optional[int] = None,
                                     review_coverage: Optional[int] = None,
                                     should_relaunch_kpi_computation: Optional[bool] = None,
                                     title: Optional[str] = None,
                                     use_honeypot: Optional[bool] = None):
        """
        Update properties of a project

        Parameters
        ----------
        - project_id : str
            Identifier of the project
        - consensus_mark : float, optional (default = None)
            Should be between 0 and 1
        - consensus_tot_coverage : int, optional (default = None)
            Should be between 0 and 100. It is the percentage of the dataset
            that will be annotated several times.
        - description : str, optional (default = None)
        - honeypot_mark : float, optional (default = None)
            Should be between 0 and 1
        - instructions : str, optional (default = None)
        - interface_category : str, optional (default = 'IV2')
            Always use 'IV2'
        - input_type : str, optional (default = None)
            Currently, one of {AUDIO, IMAGE, PDF, TEXT, URL, VIDEO, NA}
        - json_interface : dict, optional (default = None)
            The json parameters of the project, see Edit your interface.
        - min_consensus_size : int, optional (default = None)
            Should be between 1 and 10
            Number of people that will annotate the same asset, for consensus computation.
        - number_of_assets : int, optional (default = None)
            Defaults to 0
        - number_of_assets_with_empty_labels : int, optional (default = None)
            Defaults to 0
        - number_of_remaining_assets : int, optional (default = None)
            Defaults to 0
        - number_of_reviewed_assets : int, optional (default = None)
            Defaults to 0
        - review_coverage : int, optional (default = None)
            Should be between 0 and 100
            Allow to set the percentage of assets that will be queued in the review interface
        - should_relaunch_kpi_computation : bool, optional (default = None)
            Technical field, added to indicate changes in honeypot or consensus settings
        - title : str, optional (default = None)
            Title of the project
        - use_honeypot : bool, optional (default = None)
            Activate / Deactivate the use of honeypot in the project

        Returns
        -------
        - a result object which indicates if the mutation was successful, or an error message else.

        Examples
        -------
        >>> kili.update_properties_in_project(project_id=project_id, title='New title')
        """
        verify_argument_ranges(consensus_tot_coverage,
                               min_consensus_size,
                               review_coverage)

        variables = {
            'consensusMark': consensus_mark,
            'consensusTotCoverage': consensus_tot_coverage,
            'description': description,
            'honeypotMark': honeypot_mark,
            'instructions': instructions,
            'interfaceCategory': interface_category,
            'inputType': input_type,
            'jsonInterface': dumps(json_interface) if json_interface is not None else None,
            'minConsensusSize': min_consensus_size,
            'numberOfAssets': number_of_assets,
            'numberOfAssetsWithSkippedLabels': number_of_assets_with_empty_labels,
            'numberOfRemainingAssets': number_of_remaining_assets,
            'numberOfReviewedAssets': number_of_reviewed_assets,
            'projectID': project_id,
            'reviewCoverage': review_coverage,
            'shouldRelaunchKpiComputation': should_relaunch_kpi_computation,
            'title': title,
            'useHoneyPot': use_honeypot
        }
        result = self.auth.client.execute(
            GQL_UPDATE_PROPERTIES_IN_PROJECT, variables)
        return format_result('data', result)

    @Compatible(endpoints=['v2'])
    @typechecked
    def create_project(self, input_type: str, json_interface: dict,
                       title: str, description: str = '', project_type: Optional[str] = None):
        # pylint: disable=line-too-long
        """
        Create a project

        For more detailed examples on how to create projects,
        see [the recipe](https://github.com/kili-technology/kili-playground/blob/master/recipes/create_project.ipynb).

        Parameters
        ----------
        - input_type : str
            Currently, one of {AUDIO, IMAGE, PDF, TEXT, URL, VIDEO, NA}
        - json_interface: dict
            The json parameters of the project, see Edit your interface.
        - title : str
        - description : str, optional (default = '')
        - project_type: str, optional (default = None)
            Currently, one of {
                IMAGE_CLASSIFICATION_SINGLE,
                IMAGE_CLASSIFICATION_MULTI,
                IMAGE_OBJECT_DETECTION_RECTANGLE,
                IMAGE_OBJECT_DETECTION_POLYGON,
                IMAGE_OBJECT_DETECTION_SEMANTIC,
                OCR, PDF_CLASSIFICATION_SINGLE,
                PDF_CLASSIFICATION_MULTI,
                TEXT_CLASSIFICATION_SINGLE,
                TEXT_CLASSIFICATION_MULTI,
                TEXT_TRANSCRIPTION, TEXT_NER,
                VIDEO_CLASSIFICATION_SINGLE,
                VIDEO_FRAME_CLASSIFICATION,
                VIDEO_FRAME_OBJECT_TRACKING,
                SPEECH_TO_TEXT
            }

        Returns
        -------
        - a result object which indicates if the mutation was successful, or an error message else.

        Examples
        -------
        >>> kili.create_project(input_type='IMAGE', json_interface=json_interface, title='Example')
        """
        variables = {
            'data': {'description': description,
                     'inputType': input_type,
                     'jsonInterface': dumps(json_interface),
                     'projectType': project_type,
                     'title': title}
        }
        result = self.auth.client.execute(GQL_CREATE_PROJECT, variables)
        return format_result('data', result)

    @Compatible(['v2'])
    @typechecked
    def make_project_public(self, project_id: str):
        """
        Make a project public. Warning: This action is permanent and irreversible.

        Parameters
        ----------
        - project_id : str

        Returns
        -------
        - the public token to provide in the public URL
        """
        variables = {'where': {'id': project_id}}
        result = self.auth.client.execute(GQL_MAKE_PROJECT_PUBLIC, variables)
        return format_result('data', result)

    @Compatible(['v1', 'v2'])
    @typechecked
    def update_properties_in_role(self, role_id: str, project_id: str, user_id: str, role: str):
        """
        Update properties of a role

        To be able to change someone's role, you must be either of:
        - an admin
        - a team manager of the project
        - an admin of the organization

        Parameters
        ----------
        - role_id : str
            Role identifier of the user. E.g. : 'to-be-deactivated'
        - project_id : str
            Identifier of the project
        - user_id : str
            The email or identifier of the user with updated role
        - role : str
            The new role. One of "ADMIN", "TEAM_MANAGER", "REVIEWER", "LABELER"

        Returns
        -------
        - a result object which indicates if the mutation was successful, or an error message else.
        """
        variables = {
            'roleID': role_id,
            'projectID': project_id,
            'userID': user_id,
            'role': role
        }
        result = self.auth.client.execute(
            GQL_UPDATE_PROPERTIES_IN_ROLE, variables)
        return format_result('data', result)

    @Compatible(['v1', 'v2'])
    @typechecked
    def delete_from_roles(self, role_id: str):
        """
        Delete users by their role_id

        Parameters
        ----------
        - role_id : str

        Returns
        -------
        - a result object which indicates if the mutation was successful, or an error message else.
        """
        variables = {'where': {'id': role_id}}
        result = self.auth.client.execute(GQL_DELETE_FROM_ROLES, variables)
        return format_result('data', result)

    @Compatible(['v2'])
    @typechecked
    def update_properties_in_project_user(self, project_user_id: str,
                                          consensus_mark: Optional[float] = None,
                                          honeypot_mark: Optional[float] = None,
                                          number_of_labeled_assets: Optional[int] = None,
                                          starred: Optional[bool] = None,
                                          total_duration: Optional[int] = None):
        """
        Update properties of a project-user tuple

        Parameters
        ----------
        - project_user_id : str
        - consensus_mark : float, optional (default = None)
            Should be between 0 and 1.
        - honeypot_mark : float, optional (default = None)
            Should be between 0 and 1.
        - number_of_labeled_assets : int, optional (default = None)
            Number of assets the user labeled in the project.
        - starred : bool, optional (default = None)
            Whether to star the project in the project list.
        - total_duration : int, optional (default = None)
            Total time the user spent in the project.

        Returns
        -------
        - a result object which indicates if the mutation was successful, or an error message else.

        Examples
        -------
        >>> for project_user in project_users:
        ...     kili.update_properties_in_project_user(
                    project_user_id=project_user['id'],
                    honeypot_mark=0)
        """
        variables = {
            'consensusMark': consensus_mark,
            'honeypotMark': honeypot_mark,
            'numberOfLabeledAssets': number_of_labeled_assets,
            'projectUserID': project_user_id,
            'starred': starred,
            'totalDuration': total_duration,
        }
        result = self.auth.client.execute(
            GQL_GQL_UPDATE_PROPERTIES_IN_PROJECT_USER, variables)
        return format_result('data', result)

    @Compatible()
    @typechecked
    def force_project_kpis(self, project_id: str):
        """
        Compute KPIs for a project

        Parameters
        ----------
        - project_id : str

        Returns
        -------
        - None
        """
        _ = QueriesAsset(self.auth).assets(project_id=project_id)
        _ = QueriesProject(self.auth).projects(project_id=project_id)

    @Compatible(['v1', 'v2'])
    @typechecked
    def internal_delete_project(self, project_id: str):
        """
        Delete project permanently.
        WARNING: This resolver is for internal use by Kili Technology only.

        Parameters
        ----------
        - project_id : str

        Returns
        -------
        - a result object which indicates if the mutation was successful, or an error message else.
        """
        variables = {'projectID': project_id}
        result = self.auth.client.execute(GQL_DELETE_PROJECT, variables)
        return format_result('data', result)

    @Compatible(['v1', 'v2'])
    @typechecked
    def delete_project(self, project_id: str):
        """
        Delete project permanently.

        Parameters
        ----------
        - project_id : str

        Returns
        -------
        - a result object which indicates if the mutation was successful, or an error message else.
        """
        variables = {'where': {'id': project_id}}
        result = self.auth.client.execute(
            GQL_PROJECT_DELETE_ASYNCHRONOUSLY, variables)
        return format_result('data', result)
