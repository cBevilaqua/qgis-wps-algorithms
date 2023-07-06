"""Dissolve

https://docs.qgis.org/3.28/en/docs/user_manual/processing_algs/gdal/vectorgeoprocessing.html#dissolve
"""

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingOutputNumber,
    QgsProcessingParameterDistance,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterVectorDestination,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterField,
    QgsFeatureRequest,
)
from qgis import processing


class DissolveAlgorithm(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer,
    creates some new layers and returns some results.
    """

    # INPUT = "INPUT"
    # OUTPUT = "OUTPUT"

    def __init__(self):
        super().__init__()

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        # Must return a new copy of your algorithm.
        return DissolveAlgorithm()

    def name(self):
        """
        Returns the unique algorithm name.
        """
        return "dissolve"

    def displayName(self):
        """
        Returns the translated algorithm name.
        """
        return self.tr("Dissolve")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to.
        """
        return self.tr("Custom scripts")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs
        to.
        """
        return "customscripts"

    def shortHelpString(self):
        """
        Returns a localised short help string for the algorithm.
        """
        return self.tr("Qgis dissolve")

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and outputs of the algorithm.
        """
        # 'INPUT' is the recommended name for the main input
        # parameter.
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                "INPUT",
                self.tr("Input layer"),
                types=[QgsProcessing.TypeVectorAnyGeometry],
            )
        )

        # check how to add a droptown with attributes

        self.addParameter(
            QgsProcessingParameterField(
                "FIELDS",
                self.tr("Fields (Optional)"),
                parentLayerParameterName="INPUT",
                allowMultiple=False,  # ver como usa e pega varios
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorDestination(
                "OUTPUT",
                self.tr("Intersection output"),
            )
        )

        """
        self.addParameter(
            QgsProcessingParameterDistance(
                "BUFFERDIST",
                self.tr("BUFFERDIST"),
                defaultValue=1.0,
                # Make distance units match the INPUT layer units:
                parentParameterName="INPUT",
            )
        )
        """

        """
        self.addParameter(
            QgsProcessingParameterDistance(
                "CELLSIZE",
                self.tr("CELLSIZE"),
                defaultValue=10.0,
                parentParameterName="INPUT",
            )
        )
        """
        self.addOutput(
            QgsProcessingOutputNumber(
                "NUMBEROFFEATURES", self.tr("Number of features processed")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        # First, we get the count of features from the INPUT layer.
        # This layer is defined as a QgsProcessingParameterFeatureSource
        # parameter, so it is retrieved by calling
        # self.parameterAsSource.
        input_featuresource = self.parameterAsSource(parameters, "INPUT", context)
        numfeatures = input_featuresource.featureCount()
        field_name = self.parameterAsString(parameters, "FIELD", context)

        # Retrieve the buffer distance and raster cell size numeric
        # values. Since these are numeric values, they are retrieved
        # using self.parameterAsDouble.
        # bufferdist = self.parameterAsDouble(parameters, "BUFFERDIST", context)
        # rastercellsize = self.parameterAsDouble(parameters, "CELLSIZE", context)

        if feedback.isCanceled():
            return {}

        # to ignore invalid features
        # context.setInvalidGeometryCheck(QgsFeatureRequest.GeometryNoCheck)

        params = {
            "INPUT": parameters["INPUT"],
            "OUTPUT": parameters["OUTPUT"],
        }

        if field_name is not None and field_name != "":
            params["FIELD"] = field_name

        result = processing.run(
            "gdal:dissolve",
            params,
            # Because the buffer algorithm is being run as a step in
            # another larger algorithm, the is_child_algorithm option
            # should be set to True
            is_child_algorithm=True,
            #
            # It's important to pass on the context and feedback objects to
            # child algorithms, so that they can properly give feedback to
            # users and handle cancelation requests.
            context=context,
            feedback=feedback,
        )

        # Check for cancelation
        if feedback.isCanceled():
            return {}

        # Return the results
        return {
            "OUTPUT": result["OUTPUT"],
            "NUMBEROFFEATURES": numfeatures,
        }
