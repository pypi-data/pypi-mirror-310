from ape import plugins


@plugins.register(plugins.Config)
def config_class():
    from ape_blast.ecosystem import BlastConfig

    return BlastConfig


@plugins.register(plugins.EcosystemPlugin)
def ecosystems():
    from ape_blast.ecosystem import Blast

    yield Blast


@plugins.register(plugins.NetworkPlugin)
def networks():
    from ape.api.networks import (
        LOCAL_NETWORK_NAME,
        ForkedNetworkAPI,
        NetworkAPI,
        create_network_type,
    )

    from ape_blast.ecosystem import NETWORKS

    for network_name, network_params in NETWORKS.items():
        yield "blast", network_name, create_network_type(*network_params)
        yield "blast", f"{network_name}-fork", ForkedNetworkAPI

    # NOTE: This works for local providers, as they get chain_id from themselves
    yield "blast", LOCAL_NETWORK_NAME, NetworkAPI


@plugins.register(plugins.ProviderPlugin)
def providers():
    from ape.api.networks import LOCAL_NETWORK_NAME
    from ape_node import Node
    from ape_test import LocalProvider

    from ape_blast.ecosystem import NETWORKS

    for network_name in NETWORKS:
        yield "blast", network_name, Node

    yield "blast", LOCAL_NETWORK_NAME, LocalProvider


def __getattr__(name: str):
    if name == "NETWORKS":
        from ape_blast.ecosystem import NETWORKS

        return NETWORKS

    elif name == "Blast":
        from ape_blast.ecosystem import Blast

        return Blast

    elif name == "BlastConfig":
        from ape_blast.ecosystem import BlastConfig

        return BlastConfig

    else:
        raise AttributeError(name)


__all__ = [
    "NETWORKS",
    "Blast",
    "BlastConfig",
]
