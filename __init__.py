def classFactory(iface):
    from .batch_layer_renamer import BatchLayerRenamer
    return BatchLayerRenamer(iface)
