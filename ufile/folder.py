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

from typing import Any, Dict, List, Tuple
from urllib.parse import urljoin

from .exception import NotAuthenticated


class Folder:
    """Folders Methods

    Raises:
        NotAuthenticated: Raised if the user is not authenticated.

    """

    async def _create_folder(
        self, name: str, folder_id: str, public: bool
    ) -> Tuple[Dict[str, Any], int]:
        """Create a folder

        Args:
            name (`str`): name of the folder
            folder_id (`str`): folder id
            public (`bool`): to keep folder public or private

        Raises:
            NotAuthenticated: Raised if the user is not authenticated.
        """
        if not self.api_key:
            raise NotAuthenticated("You need to pass an API key")
        url = urljoin(self.API, "folders/")
        data = {}
        if name:
            data = {"name": name}
        if folder_id:
            data["folder_id"] = folder_id
        if public:
            data["public"] = 1
        headers = {"X-API-KEY": self.api_key}
        async with self.session() as session:
            async with session.post(url, data=data, headers=headers) as res:
                result = await res.json()
                return result, res.status

    async def _delete_folder(self, folder_id: int) -> Tuple[str, int]:
        """Delete a folder

        Args:
            folder_id (`int`): folder id to delete

        Raises:
            NotAuthenticated: Raised if the user is not authenticated.
        """
        if not self.api_key:
            raise NotAuthenticated("You need to pass an API key")

        async with self.session() as session:
            url = urljoin(self.API, f"folders/{folder_id}")
            headers = {"X-API-KEY": self.api_key}
            async with session.delete(url, headers=headers) as resp:
                result = await resp.json()
                return result, resp.status

    async def _get_folder(self, folder_id: int) -> Tuple[Dict[str, Any], int]:
        """get a specific folder

        Args:
            folder_id (`int`): folder id to get

        Raises:
            NotAuthenticated: Raised if the user is not authenticated.

        Returns:
            dict: a dictionary of the folder info
        """
        if not self.api_key:
            raise NotAuthenticated("You need to pass an API key")

        url = urljoin(self.API, f"folders/{folder_id}")
        headers = {"X-API-KEY": self.api_key}
        async with self.session() as session:
            async with session.get(url, headers=headers) as resp:
                result = await resp.text()
                return result, resp.status

    async def _list_folder(self, folder_id: int) -> Tuple[List[Dict[str, Any]], int]:
        """list all the folders

        Args:
            folder_id (`int`): folder id in which you want to list the folders

        Raises:
            NotAuthenticated: Raised if the user is not authenticated.
        """
        if not self.api_key:
            raise NotAuthenticated("You need to pass an API key")
        url = urljoin(self.API, "folders/")
        headers = {"X-API-KEY": self.api_key}
        data = {}
        if folder_id:
            data = {"folder_id": folder_id}
        async with self.session() as session:
            async with session.get(url, params=data, headers=headers) as resp:
                result = await resp.json()
                return result, resp.status
