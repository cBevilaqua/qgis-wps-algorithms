class Test:
    def __init__(self):
        pass


def WPSClassFactory(iface):
    # from .example_algorithm import ExampleProcessingAlgorithm
    from .provider import Provider

    iface.registerProvider(Provider())
    return Test()
