#
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. ALL RIGHTS RESERVED.
#
# This software product is a proprietary product of Nvidia Corporation and its affiliates
# (the "Company") and all right, title, and interest in and to the software
# product, including all associated intellectual property rights, are and
# shall remain exclusively with the Company.
#
# This software product is governed by the End User License Agreement
# provided with the software product.
#

from ngcbpc.transformer import BaseSearchTransformer
from ngccli.data.api.StorageResource import StorageResource


class WorkspaceSearchTransformer(StorageResource, BaseSearchTransformer):

    SEARCH_RESOURCE_KEY_MAPPING = {"createdByUserName": "creatorUserName", "size": "sizeInBytes"}
    SEARCH_RESOURCE_TOP_KEY_MAPPING = {"dateCreated": "createdDate", "dateModified": "updatedDate", "resourceId": "id"}

    def __init__(self, search_response):
        BaseSearchTransformer.__init__(self, search_response)
        StorageResource.__init__(self, self._resources)
