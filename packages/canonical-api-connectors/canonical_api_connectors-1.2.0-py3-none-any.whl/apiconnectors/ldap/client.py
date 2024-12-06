"""LDAP API client."""

from typing import (
    Dict,
    Optional,
)

import ldap


class LDAPClient:
    """
    LDAPClient - Class for interacting with the an LDAP server.

    Attributes:
        _client: LDAP client.
    """

    def __init__(self, uri: str, password: str, dn: str):
        """Initialize an instance of the LDAPClient class for interacting an LDAP server.

        Args:
            uri (str): LDAP server URI.
            password (str): LDAP server password.
            dn (str): LDAP server bind distinguished name.

        Attributes:
            _client: LDAP client.
        """
        ldap_conn = ldap.initialize(uri)
        ldap_conn.simple_bind_s(dn, password)
        self._client = ldap_conn

    def find_entries(
        self,
        dn: str,
        search_fields: dict = None,
        want: list = None,
        allow_multiple=True,
    ) -> Optional[list]:
        """Find entries in LDAP matching the specified search criteria.

        Args:
            dn (str): The base distinguished name (DN) to search within.
            search_fields (dict): A dictionary of fields to filter by.
            want (list): A list of attributes to fetch for each entry.
            allow_multiple (bool): Whether multiple matching entries are allowed.

        Returns:
            Optional[list]: A list of tuples where each tuple contains the DN and a dictionary
            of attributes for the matching entries, or `None` if no entries are found.

        Raises:
            ValueError: If multiple entries are found and `allow_multiple` is False.
        """
        try:
            if search_fields:
                search_filter = _ldap_search_filter_or(search_fields)
                ldap_result = self._client.search_s(
                    dn, ldap.SCOPE_ONELEVEL, search_filter, want
                )
            else:
                ldap_result = self._client.search_s(dn, ldap.SCOPE_BASE, want)
        except ldap.NO_SUCH_OBJECT:
            return None

        if not ldap_result or len(ldap_result) == 0:
            return None

        if len(ldap_result) > 1 and not allow_multiple:
            raise ValueError("Found multiple entries and on_multiple=fail, bailing")

        results = []
        for (
            dn,  # pylint: disable=redefined-argument-from-local
            attributes,
        ) in ldap_result:
            if isinstance(dn, bytes):
                dn = dn.decode("utf-8")
            attributes = _decode_dict(attributes)
            results.append((dn, attributes))
        return results


def _ldap_search_filter_or(search_fields: Dict[str, str]) -> str:
    """Build OR search filter based on search fields.

    Args:
        search_fields (dict): Search fields key/value mappings.
    """
    filter_parts = [f"({key}={value})" for key, value in search_fields.items()]
    search_filter = f"(|{''.join(filter_parts)})"
    return search_filter


def _decode_dict(data: dict) -> dict:
    """Decode a dictionary's values.

    Converts bytes to strings and recursively processing lists and nested dictionaries.

    Args:
        data (dict): The dictionary to decode.

    Returns:
        dict: A new dictionary with decoded values, or None if the input is None.
    """
    if data is None:
        return data
    blocklist = ["jpegPhoto"]
    rv = {}
    for key, value in data.items():
        # Skip keys in blocklist
        if key in blocklist:
            continue

        if isinstance(value, bytes):
            value = value.decode("utf-8")
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv


def _decode_list(data: list) -> list:
    """Decode a list's elements, converting bytes to strings and recursively processing nested lists and dictionaries.

    Args:
        data (list): The list to decode.

    Returns:
        list: A new list with decoded elements.
    """
    rv = []
    for item in data:
        if isinstance(item, bytes):
            item = item.decode("utf-8")
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv
