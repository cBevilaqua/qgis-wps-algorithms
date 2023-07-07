from qgis.core import QgsApplication, QgsProcessingProvider
from .buffer import BufferAlgorithm
from .intersection import IntersectionAlgorithm
from .dissolve import DissolveAlgorithm
from .difference import DifferenceAlgorithm


class Provider(QgsProcessingProvider):
    def __init__(self):
        super().__init__()

    def id(self):
        # Unique identifier for your provider
        return "custom"

    def getAlgs(self):
        algs = [
            BufferAlgorithm(),
            IntersectionAlgorithm(),
            DissolveAlgorithm(),
            DifferenceAlgorithm(),
        ]
        return algs

    def name(self):
        return "Zoox Qgis Algos Provider"

    def loadAlgorithms(self):
        self.algs = self.getAlgs()
        for a in self.algs:
            self.addAlgorithm(a)
