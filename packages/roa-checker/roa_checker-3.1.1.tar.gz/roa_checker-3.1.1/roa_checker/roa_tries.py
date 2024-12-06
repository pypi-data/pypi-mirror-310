from ipaddress import IPv4Network, IPv6Network

from .roa_trie import ROATrie


class IPv4ROATrie(ROATrie[IPv4Network]):
    """Trie of IPv4 CIDRs for ROAs"""

    PrefixCls = IPv4Network


class IPv6ROATrie(ROATrie[IPv6Network]):
    """Trie of IPv6 CIDRs for ROAs"""

    PrefixCls = IPv6Network
