"""
ufile
~~~~~~~~~

MIT License

Copyright (c) 2021 GautamKumar <https://github.com/gautamajay52>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

from typing import Any, Dict, List

from aiohttp import ClientSession

from .exception import ServerError
from .file import File
from .folder import Folder


class Ufile(File, Folder):
    """
    ufile.io
    ~~~~~~~~
    Ufile API Class

    Parameters:
        api_key (`str`, optional):
            Ufile.io API Key
    """

    API: str = "https://up.ufile.io/v1/"
    session = ClientSession

    def __init__(self, api_key=None) -> None:
        self.fuid: str = ""
        self.api_key = api_key

    async def upload_file(
        self, file: str, file_name: str = "", folder_id: str = ""
    ) -> Dict[str, Any]:
        """Upload a file to Ufile.io

        Args:
            file (`str`): Path to the file to be uploaded
            file_name (`str`, optional): file name to be seen on ufile. Defaults to Original Name.
            folder_id (`str`, optional): Folder id where you wanted to upload file. Defaults to Root Folder.

        Returns:
            dict: file information
        """
        return self.parse_response(
            *await self._upload(file=file, file_name=file_name, folder_id=folder_id)
        )

    async def download_file(self, url: str) -> str:
        """
        Parameters:
            url:
                url of the file to be downloaded
        """
        return self.parse_response(*await self._download(url))

    async def delete_file(self, file_id: int) -> str:
        """
        Parameters:
            file_id:
                file id
        """
        return self.parse_response(*await self._delete_file(file_id=file_id))

    async def get_file(self, file_id: int) -> Dict[str, Any]:
        """Dict of file information

        Args:
            file_id (`int`): file id

        Returns:
            dict: file information
        """
        return self.parse_response(*await self._get_file(file_id=file_id))

    async def list_file(
        self,
        query: str = "",
        filter: str = "",
        limit: int = 100,
        sort: str = "datecreated",
        order: str = "DESC",
        archived: int = 0,
        deleted: int = 0,
        days: str = "",
        expired: int = 0,
        offset: int = 0,
        active: int = 0,
        banned: int = 0,
        folder_id: str = "",
    ) -> List[Dict[str, Any]]:
        """List files

        Args:
            query (`str`, optional): Search the filename e.g - "my-file"
            filter (`str`, optional): Filter the file type e.g - "video"
            limit (`int`, optional): Response limit (max 100)
            sort (`str`, optional): Sort by field e.g - "id", "datecreated", "size"
            order (`str`, optional): Order direction e.g - "DESC", "ASC"
            archived (`int`, optional):  Return archived files
            deleted (`int`, optional): Return deleted files
            days (`str`, optional): Limit by file age in days e.g - "30"
            expired (`int`, optional): Return expired files
            offset (`int`, optional): Response offset e.g - 100 (to return results from 100 - 200)
            active (`int`, optional): Only return active files
            banned (`int`, optional): Include banned files
            folder_id (`str`, optional): Define folder ID to search

        Returns:
            Union[Dict[str, Union[str, int]], str]: [description]
        """
        result, statuscode = await self._list_file(
            query=query,
            limit=limit,
            offset=offset,
            active=active,
            deleted=deleted,
            days=days,
            expired=expired,
            filter=filter,
            banned=banned,
            folder_id=folder_id,
            sort=sort,
            order=order,
            archived=archived,
        )
        return self.parse_response(result, statuscode)

    async def create_folder(
        self, name: str = "", folder_id: str = "", public: bool = False
    ) -> Dict[str, Any]:
        """Create a folder

        Args:
            name (`str`, optional): name of the folder. Defaults to "".
            folder_id (`str`, optional): folder id. Defaults to "".
            public (`bool`, optional): public or private. Defaults to True.

        Returns:
            dict: folder information
        """
        return self.parse_response(
            *await self._create_folder(name=name, folder_id=folder_id, public=public)
        )

    async def get_folder(self, folder_id: int) -> Dict[str, Any]:
        """get information of a folder

        Args:
            folder_id (`int`): folder id
        """
        return self.parse_response(*await self._get_folder(folder_id=folder_id))

    async def delete_folder(self, folder_id: int) -> str:
        """Delete a folder

        Args:
            folder_id (`int`, optional): folder id.

        Returns:
            `str`: sucess message or error message
        """
        return self.parse_response(*await self._delete_folder(folder_id=folder_id))

    async def list_folder(self, folder_id: int = 0) -> Dict[str, Any]:
        """List folders

        Args:
            folder_id (`int`, optional): Folder id to list its folders. Defaults to None.
        """
        return self.parse_response(*await super()._list_folder(folder_id))

    @staticmethod
    def parse_response(response: str, status: int) -> Dict[str, Any]:
        """parse the response from the api"""
        if status == 200:
            return response
        if isinstance(response, dict):
            raise ServerError(response.get("error", "Unknown error"))
        raise ServerError(response)
