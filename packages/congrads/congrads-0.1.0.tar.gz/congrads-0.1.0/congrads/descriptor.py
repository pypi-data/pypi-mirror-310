class Descriptor:
    """
    A class to manage the mapping of neurons to layers and their properties
    (e.g., output, constant, or variable) in a neural network.

    This class enables the organization and description of network elements,
    such as associating neurons with specific layers and categorizing layers
    as outputs, constants, or variables.

    This allows users to easily place constraints on parts of the network by
    referencing the name that is configured in this class.
    """

    def __init__(
        self,
    ):
        """
        Initialize the Descriptor class with empty mappings for neurons and layers.

        This includes:
            - `neuron_to_layer`: A dictionary mapping neuron names to their corresponding layer names.
            - `neuron_to_index`: A dictionary mapping neuron names to their corresponding index within a layer.
            - `output_layers`: A set that holds the names of layers marked as output layers.
            - `constant_layers`: A set that holds the names of layers marked as constant layers.
            - `variable_layers`: A set that holds the names of layers marked as variable layers.
        """

        # Define dictionaries that will translate neuron names to layer and index
        self.neuron_to_layer: dict[str, str] = {}
        self.neuron_to_index: dict[str, int] = {}

        # Define sets that will hold the layers based on which type
        self.output_layers: set[str] = set()
        self.constant_layers: set[str] = set()
        self.variable_layers: set[str] = set()

    def add(
        self,
        layer_name: str,
        neuron_names: list[str],
        output: bool = False,
        constant: bool = False,
    ):
        """
        Add a layer to the descriptor, associating it with neurons and marking it
        as an output or constant layer.

        Args:
            layer_name (str): The name of the layer to be added.
            neuron_names (list[str]): A list of neuron names that belong to the layer.
            output (bool, optional): If True, mark this layer as an output layer. Defaults to False.
            constant (bool, optional): If True, mark this layer as a constant layer. Defaults to False.
        """

        if output:
            self.output_layers.add(layer_name)

        if constant:
            self.constant_layers.add(layer_name)
        else:
            self.variable_layers.add(layer_name)

        for index, neuron_name in enumerate(neuron_names):
            self.neuron_to_layer[neuron_name] = layer_name
            self.neuron_to_index[neuron_name] = index
