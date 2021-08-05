"""
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

import os
import re
from typing import Any, Dict, List, Tuple
from urllib.parse import urljoin

from aiohttp import ClientSession

from .exception import NotAuthenticated


class File:
    """File methods

    Raises:
        ValueError: if file is not a file
        NotAuthenticated: if the client is not authenticated
        TypeError: if url is not a valid ufile link
    """

    async def __get_fuid(self, file: str) -> str:
        """get special id from server

        Args:
            file (`str`): file to upload

        Returns:
            `str`: special fuid
        """
        size = os.stat(file).st_size
        url = urljoin(self.API, "upload/create_session")
        data = {"file_size": size}
        headers = {}
        if self.api_key:
            headers = {"X-API-KEY": self.api_key}

        async with self.session() as session:
            async with session.post(url, data=data, headers=headers) as resp:
                result = await resp.json()
            self.fuid = result["fuid"]
        return self.fuid

    async def __finalise(
        self,
        session: ClientSession,
        total_chunks: int,
        file: str,
        file_name: str,
        folder_id: str,
    ) -> Tuple[Dict[str, Any], int]:
        """Finalise the upload

        Args:
            session (`ClientSession`): aiohttp session
            total_chunks (`int`): total chunks
            file (`str`): file to upload
            file_name (`str`): file name if passed else base name
            folder_id (`str`): folder id where file should get uploaded

        Returns:
            dict: file metadata or error message
        """

        if not file_name:
            file_name = os.path.basename(file)

        _, file_type = os.path.splitext(file_name)
        data = {
            "fuid": self.fuid,
            "file_name": file_name,
            "file_type": file_type or "txt",
            "total_chunks": total_chunks,
        }
        if folder_id:
            data["folder_id"] = folder_id
        url = urljoin(self.API, "upload/finalise")
        async with session.post(url, data=data) as resp:
            result = await resp.json()
            return result, resp.status

    async def _upload(
        self, file: str, file_name: str, folder_id: str
    ) -> Tuple[Dict[str, Any], int]:
        """Upload a file

        Args:
            file (`str`): file to upload
            file_name (`str`): file name if passed else base name
            folder_id (`str`): folder id where file should get uploaded

        Raises:
            ValueError: if file is not a file

        Returns:
            dict: file metadata or error message
        """

        if not os.path.isfile(file):
            raise ValueError("this is not a file")

        await self.__get_fuid(file)

        url = urljoin(self.API, "upload/chunk")

        async with self.session() as session:
            with open(file, "rb") as _file:
                data = {"chunk_index": "1", "fuid": self.fuid, "file": _file}
                await session.post(url, data=data)
            return await self.__finalise(session, "1", file, file_name, folder_id)

    async def _download(self, url: str) -> Tuple[str, int]:
        """Generate a download link

        Once you have the direct file URL, you can download the contents using your preferred method (E.G - wget, cURL etc.)

        `>> Generated file links will be valid for 1 hour, and only available to your IP address`

        Args:
            url (`str`): url to download

        Raises:
            NotAuthenticated: if the client is not authenticated
            TypeError: if url is not a valid ufile link

        Returns:
            `str`: download link
        """
        if not self.api_key:
            raise NotAuthenticated("You need to pass an API key")

        reg = re.compile(r"https:\/\/ufile.io\/(.+)")
        match = reg.match(url)
        if match:
            slug = match.group(1)
        else:
            raise TypeError("Require a valid ufile link")
        headers = {"X-API-KEY": self.api_key}
        url = urljoin(self.API, f"download/{slug}")
        async with self.session() as session:
            response = await session.get(url, headers=headers)
            result = await response.text()
            return result.replace("\\", "").replace('"', ""), response.status

    async def _get_file(self, file_id: int) -> Tuple[Dict[str, Any], int]:
        """get file info

        Args:
            file_id (`int`): file id

        Raises:
            NotAuthenticated: if the client is not authenticated

        Returns:
            dict: file metadata or error message
        """
        if not self.api_key:
            raise NotAuthenticated("You need to pass an API key")
        url = urljoin(self.API, f"files/{file_id}")
        headers = {"X-API-KEY": self.api_key}
        async with self.session() as session:
            async with session.get(url, headers=headers) as resp:
                result = await resp.json()
                return result, resp.status

    async def _list_file(
        self,
        query: str,
        filter: bool,
        limit: int,
        sort: str,
        order: str,
        archived: int,
        deleted: int,
        days: bool,
        expired: int,
        offset: int,
        active: int,
        banned: int,
        folder_id: int,
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        List files
        """
        if not self.api_key:
            raise NotAuthenticated("You need to pass an API key")

        url = urljoin(self.API, f"files/")
        headers = {"X-API-KEY": self.api_key}
        kwargs = {
            "query": query,
            "filter": filter,
            "limit": limit,
            "sort": sort,
            "order": order,
            "archived": archived,
            "deleted": deleted,
            "days": days,
            "expired": expired,
            "offset": offset,
            "active": active,
            "banned": banned,
            "folder_id": folder_id,
        }
        params = self.serialize(**kwargs)
        async with self.session() as session:
            async with session.get(url, headers=headers, params=params) as resp:
                result = await resp.json()
                return result, resp.status

    async def _delete_file(self, file_id: int) -> Tuple[str, int]:
        """To delete a file from the ufile cloud

        Args:
            file_id (`int`): file id

        Raises:
            NotAuthenticated: if the client is not authenticated
        """

        if not self.api_key:
            raise NotAuthenticated("You need to pass an API key")

        async with self.session() as session:
            url = urljoin(self.API, f"files/{file_id}")
            headers = {"X-API-KEY": self.api_key}
            async with session.delete(url, headers=headers) as resp:
                result = await resp.json()
                return result, resp.status

    @staticmethod
    def serialize(**kwargs) -> Dict[str, str]:
        """Serialize kwargs to a dict

        Returns:
            dict: serialized kwargs
        """
        data = {}
        for k, v in kwargs.items():
            if k == "query" and v:
                data[k] = str(v)
            elif k == "filter" and v:
                data[k] = str(v)
            elif k == "limit" and v:
                data[k] = str(v)
            elif k == "sort" and v:
                data[k] = str(v)
            elif k == "order" and v:
                data[k] = str(v)
            elif k == "archived" and v:
                data[k] = str(v)
            elif k == "deleted" and v:
                data[k] = str(v)
            elif k == "days" and v:
                data[k] = str(v)
            elif k == "expired" and v:
                data[k] = str(v)
            elif k == "offset" and v:
                data[k] = str(v)
            elif k == "active" and v:
                data[k] = str(v)
            elif k == "banned" and v:
                data[k] = str(v)
            elif k == "folder_id" and v:
                data[k] = str(v)
        return data
