import copy
from copy import deepcopy
import networkx as nx
from Models.TELink import TELink


def evaluateNetwork(network, chromosome):
    InterfacesQuantities = _calculateInterfacesQuantity(chromosome)
    TIRF = _calculateTIRF(network, chromosome)

    return InterfacesQuantities, TIRF


def _calculateInterfacesQuantity(chromosome):
    """The interface quantity is equal to TeLink x 2,
     because each TeLink is connected to two interface (one per OTS)"""
    InterfacesQuantities = 0
    for gene in chromosome:
        InterfacesQuantities += (gene * 2)
    return InterfacesQuantities


def _calculateTIRF(network, chromosome):
    """TIRF is defined as: IR/TTR. Where, IR = number of failures and
    TTR = Total restore attempts"""
    NetworkCopy = deepcopy(network)
    NetworkGraph = nx.MultiGraph()
    TELinks = []

    for linkBundle in NetworkCopy.LinkBundles:
        TELinks.append(TELink(NodeFrom=linkBundle.NodeFrom,
                              NodeTo=linkBundle.NodeTo,
                              LinkBundleId=linkBundle.id))

    # At This point the Network Graph has the Network modeled on TELink rather than Link bundles
    _convertToGraph(chromosome, TELinks, NetworkGraph)
    NetworkGraphCopy = copy.deepcopy(NetworkGraph)

    IsAllServicesAllocated = _allocateServices(NetworkCopy, NetworkGraph, NetworkGraphCopy)

    if not IsAllServicesAllocated:
        # TODO: Implement a penalty
        pass

    return None


def _convertToGraph(chromosome, TELinks, NetworkGraph):
    count = 0
    for gene in chromosome:
        TELinkAux = TELinks[count]
        for x in range(gene):
            NetworkGraph.add_edge(TELinkAux.NodeFrom, TELinkAux.NodeTo, key=TELinkAux.LinkBundleId + "_" + str(x),
                                  link=TELink(TELinkAux.NodeFrom, TELinkAux.NodeTo, TELinkAux.LinkBundleId))
        count += 1


def _allocateServices(NetworkCopy, NetworkGraph, NetworkGraphCopy):
    NonAllocatedServices = []
    IsServicesAllocated = True

    for service in NetworkCopy.Services:
        all_edge_paths = nx.all_simple_edge_paths(NetworkGraphCopy, service.NodeFrom, service.NodeTo)
        sorted_all_edge_paths = sorted(list(all_edge_paths), key=lambda a: len(a))

        AllocationIsCompleted = False

        edges = sorted_all_edge_paths[0]
        for edge in edges:
            TELINK = (NetworkGraph.get_edge_data(edge[0], edge[1])[edge[2]]).get("link")
            TELINK.IsBusy = True
            AllocationIsCompleted = True
            NetworkGraphCopy.remove_edge(edge[0], edge[1], edge[2])

        if not AllocationIsCompleted:
            NonAllocatedServices.append(service)

    if len(NonAllocatedServices) > 0:
        IsServicesAllocated = False

    return IsServicesAllocated