from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_get_myself_v1_info_whoami_get_response_api_get_myself_v1_info_whoami_get import (
    ApiGetMyselfV1InfoWhoamiGetResponseApiGetMyselfV1InfoWhoamiGet,
)
from ...types import Response


def _get_kwargs() -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/v1/info/whoami",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ApiGetMyselfV1InfoWhoamiGetResponseApiGetMyselfV1InfoWhoamiGet]:
    if response.status_code == 200:
        response_200 = ApiGetMyselfV1InfoWhoamiGetResponseApiGetMyselfV1InfoWhoamiGet.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ApiGetMyselfV1InfoWhoamiGetResponseApiGetMyselfV1InfoWhoamiGet]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ApiGetMyselfV1InfoWhoamiGetResponseApiGetMyselfV1InfoWhoamiGet]:
    """Api Get Myself

     Return current user as API sees it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiGetMyselfV1InfoWhoamiGetResponseApiGetMyselfV1InfoWhoamiGet]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ApiGetMyselfV1InfoWhoamiGetResponseApiGetMyselfV1InfoWhoamiGet]:
    """Api Get Myself

     Return current user as API sees it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiGetMyselfV1InfoWhoamiGetResponseApiGetMyselfV1InfoWhoamiGet
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ApiGetMyselfV1InfoWhoamiGetResponseApiGetMyselfV1InfoWhoamiGet]:
    """Api Get Myself

     Return current user as API sees it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiGetMyselfV1InfoWhoamiGetResponseApiGetMyselfV1InfoWhoamiGet]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ApiGetMyselfV1InfoWhoamiGetResponseApiGetMyselfV1InfoWhoamiGet]:
    """Api Get Myself

     Return current user as API sees it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiGetMyselfV1InfoWhoamiGetResponseApiGetMyselfV1InfoWhoamiGet
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
