from typing import Optional, Dict, Any

from fake_useragent import UserAgent


def get_default(UserAgent_kwargs: Optional[Dict[str, Any]] = None) -> Dict[str, str]:  # noqa
    if UserAgent_kwargs is None:
        UserAgent_kwargs = dict(platforms=["pc"])  # noqa
    headers = {
        "User-Agent": UserAgent(**UserAgent_kwargs).random
    }
    return headers


def update_default(headers: Optional[Dict[str, str]] = None,
                   default: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    if headers is None:
        headers = {}
    if default is None:
        default = get_default()
    headers.update(default)
    return headers
