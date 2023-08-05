# coding: utf-8
#
# Copyright 2022 :Barry-Thomas-Paul: Moss
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http: // www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Enum Class
# this is a auto generated file generated by Cheetah
# Namespace: com.sun.star.ucb
# Libre Office Version: 7.3
from typing_extensions import Literal
from enum import Enum


class WebDAVHTTPMethod(Enum):
    """
    Enum Class

    

    See Also:
        `API WebDAVHTTPMethod <https://api.libreoffice.org/docs/idl/ref/namespacecom_1_1sun_1_1star_1_1ucb.html#a3c143367536e0c519b25183505ae3ed7>`_
    """
    CONNECT: Literal['CONNECT']
    """
    HTTP request method as defined in RFC 2616: Hypertext Transfer Protocol – HTTP/1.1
    """
    COPY: Literal['COPY']
    """
    Copy the source to the target folder.
    
    WebDAV methods as defined in HTTP Extensions for Web Distributed Authoring and Versioning (WebDAV)
    """
    DELETE: Literal['DELETE']
    """
    HTTP request method as defined in RFC 2616: Hypertext Transfer Protocol – HTTP/1.1
    """
    GET: Literal['GET']
    """
    Get a list of all folders.
    
    HTTP request method as defined in RFC 2616: Hypertext Transfer Protocol – HTTP/1.1
    """
    HEAD: Literal['HEAD']
    """
    HTTP request method as defined in RFC 2616: Hypertext Transfer Protocol – HTTP/1.1
    """
    LOCK: Literal['LOCK']
    """
    WebDAV methods as defined in HTTP Extensions for Web Distributed Authoring and Versioning (WebDAV)
    """
    MKCOL: Literal['MKCOL']
    """
    WebDAV methods as defined in HTTP Extensions for Web Distributed Authoring and Versioning (WebDAV)
    """
    MOVE: Literal['MOVE']
    """
    Move the source to the target folder.
    
    WebDAV methods as defined in HTTP Extensions for Web Distributed Authoring and Versioning (WebDAV)
    """
    OPTIONS: Literal['OPTIONS']
    """
    HTTP request method as defined in RFC 2616: Hypertext Transfer Protocol – HTTP/1.1
    """
    PATCH: Literal['PATCH']
    """
    HTTP request method as defined in RFC 5789: PATCH Method for HTTP
    """
    POST: Literal['POST']
    """
    HTTP request method as defined in RFC 2616: Hypertext Transfer Protocol – HTTP/1.1
    """
    PROPFIND: Literal['PROPFIND']
    """
    WebDAV methods as defined in HTTP Extensions for Web Distributed Authoring and Versioning (WebDAV)
    """
    PROPPATCH: Literal['PROPPATCH']
    """
    WebDAV methods as defined in HTTP Extensions for Web Distributed Authoring and Versioning (WebDAV)
    """
    PUT: Literal['PUT']
    """
    HTTP request method as defined in RFC 2616: Hypertext Transfer Protocol – HTTP/1.1
    """
    TRACE: Literal['TRACE']
    """
    HTTP request method as defined in RFC 2616: Hypertext Transfer Protocol – HTTP/1.1
    """
    UNLOCK: Literal['UNLOCK']
    """
    WebDAV methods as defined in HTTP Extensions for Web Distributed Authoring and Versioning (WebDAV)
    """

