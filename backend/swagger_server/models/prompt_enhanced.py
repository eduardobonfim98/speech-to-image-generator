# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class PromptEnhanced(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, prompt_enhanced_id: str=None, prompt_enhanced_content: str=None):  # noqa: E501
        """PromptEnhanced - a model defined in Swagger

        :param prompt_enhanced_id: The prompt_enhanced_id of this PromptEnhanced.  # noqa: E501
        :type prompt_enhanced_id: str
        :param prompt_enhanced_content: The prompt_enhanced_content of this PromptEnhanced.  # noqa: E501
        :type prompt_enhanced_content: str
        """
        self.swagger_types = {
            'prompt_enhanced_id': str,
            'prompt_enhanced_content': str
        }

        self.attribute_map = {
            'prompt_enhanced_id': 'promptEnhancedId',
            'prompt_enhanced_content': 'promptEnhancedContent'
        }
        self._prompt_enhanced_id = prompt_enhanced_id
        self._prompt_enhanced_content = prompt_enhanced_content

    @classmethod
    def from_dict(cls, dikt) -> 'PromptEnhanced':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PromptEnhanced of this PromptEnhanced.  # noqa: E501
        :rtype: PromptEnhanced
        """
        return util.deserialize_model(dikt, cls)

    @property
    def prompt_enhanced_id(self) -> str:
        """Gets the prompt_enhanced_id of this PromptEnhanced.


        :return: The prompt_enhanced_id of this PromptEnhanced.
        :rtype: str
        """
        return self._prompt_enhanced_id

    @prompt_enhanced_id.setter
    def prompt_enhanced_id(self, prompt_enhanced_id: str):
        """Sets the prompt_enhanced_id of this PromptEnhanced.


        :param prompt_enhanced_id: The prompt_enhanced_id of this PromptEnhanced.
        :type prompt_enhanced_id: str
        """

        self._prompt_enhanced_id = prompt_enhanced_id

    @property
    def prompt_enhanced_content(self) -> str:
        """Gets the prompt_enhanced_content of this PromptEnhanced.


        :return: The prompt_enhanced_content of this PromptEnhanced.
        :rtype: str
        """
        return self._prompt_enhanced_content

    @prompt_enhanced_content.setter
    def prompt_enhanced_content(self, prompt_enhanced_content: str):
        """Sets the prompt_enhanced_content of this PromptEnhanced.


        :param prompt_enhanced_content: The prompt_enhanced_content of this PromptEnhanced.
        :type prompt_enhanced_content: str
        """

        self._prompt_enhanced_content = prompt_enhanced_content
