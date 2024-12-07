# Congrads

**Congrads** is a Python toolbox that brings **constraint-guided gradient descent** capabilities to your machine learning projects. Built with seamless integration into PyTorch and PyTorch Lightning, Congrads empowers you to enhance the training and optimization process by incorporating constraints into your training pipeline.

Whether you're working with simple inequality constraints, combinations of input-output relations, or custom constraint formulations, Congrads provides the tools and flexibility needed to build more robust and generalized models.

> <strong>Note:</strong> The Congrads toolbox is currently in alpha phase. Expect significant changes, potential bugs, and incomplete features as we continue to develop and improve the functionality. Feedback is highly appreciated during this phase to help us refine the toolbox and ensure its reliability in later stages.

## Key Features

- **Constraint-Guided Training**: Add constraints to guide the optimization process, ensuring that your model generalizes better by trying to satisfy the constraints.
- **Flexible Constraint Definition**: Define constraints on inputs, outputs, or combinations thereof, using an intuitive and extendable interface. Make use of pre-programmed constraint classes or write your own.
- **Seamless PyTorch Integration**: Use Congrads within your existing PyTorch workflows with minimal setup.
- **PyTorch Lightning Support**: Easily plug into PyTorch Lightning projects for scalable and structured model training.
- **Flexible and extendible**: Write your own custom networks, constraints and dataset classes to easily extend the functionality of the toolbox.

## Installation

Currently, the **Congrads** toolbox can only be installed using pip. We will later expand to other package managers such as conda. 

```bash
pip install congrads
```

## Getting Started

### 1. **Prerequisites**

Before you can use **Congrads**, make sure you have the following installed:

- Python 3.7+
- **PyTorch** (install with CUDA support for GPU training, refer to the [getting started guide](https://pytorch.org/get-started/locally/))
- **PyTorch Lightning** (preffered version 2.4, [installation guide](https://lightning.ai/docs/pytorch/stable/starter/installation.html))

### 2. **Installation**

Please install **Congrads** via pip:

```bash
pip install congrads
```

### 3. **Basic Usage**

#### 1. Import the toolbox

```python
from congrads.descriptor import Descriptor
from congrads.constraints import ScalarConstraint, BinaryConstraint
from congrads.learners import Learner
```

#### 2. Instantiate and configure descriptor

The descriptor describes your specific use-case. It assigns names to specific neurons so you can easily reference them when defining constraints. By settings flags, you can specifiy if a layer is fixed or if it is an output layer.

```python
# Descriptor setup
descriptor = Descriptor()
descriptor.add("input", ["I1", "I2", "I3", "I4"], constant=True)
descriptor.add("output", ["O1", "O2"], output=True)
```

#### 3. Define constraints on your network

You can define constraints on your network using the names previously configured in the descriptor. A set of predefined constraint classes can be used to define inequalities on input or output data.

```python
# Constraints definition
Constraint.descriptor = descriptor
constraints = [
    ScalarConstraint("O1", gt, 0),      # O1 > 0
    BinaryConstraint("O1", le, "O2"),   # O1 <= O2
]
```

#### 4. Adjust network

Your regular Pytorch network can be used with this toolbox. We only require that the output of your model's forward pass is a dictionary of layers. The keys must match the descriptor settings.

```python
def forward(self, X):
    input = X
    output = self.out(self.hidden(self.input(X)))

    return {"input": input, "output": output}
```

You then can use your own network and directly assign it to the learner.

#### 5. Set up network and data

Next, instantiate the adjusted network and the data. At the moment, we require the data to be implemented as a `LightningDataModule` class.

```python
# Data and network setup
network = YourOwnNetwork(n_inputs=4, n_outputs=2, n_hidden_layers=3, hidden_dim=10)
data = YourOwnData(batch_size=100)
```

#### 6. Set up learner

You can specify your own loss function and optimizer with their own settings to be used for learning the model.

```python
# Learner setup
loss_function = MSELoss()
optimizer = Adam(network.parameters(), lr=0.001)

learner = Learner(network, descriptor, constraints, loss_function, optimizer)
```

#### 7. Set up trainer

Finally, set up a trainer to start the actual training of the model.

```python
# Trainer setup
trainer = Trainer(max_epochs=100)

# Train model
trainer.fit(learner, data)
```

## Example Use Cases

- **Optimization with Domain Knowledge**: Ensure outputs meet real-world restrictions or safety standards.
- **Physics-Informed Neural Networks (PINNs)**: Enforce physical laws as constraints in your models.
- **Improve Training Process**: Inject domain knowledge in the training stage, increasing learning efficiency.

## Roadmap

- [ ] Documentation and Notebook examples
- [ ] Add support for constraint parser that can interpret equations
- [ ] Add better handling of metric logging and visualization
- [ ] Revise if Pytorch Lightning is preferable over plain Pytorch
- [ ] Determine if it is feasible to add unit and or functional tests

## Contributing

We welcome contributions to Congrads! Whether you want to report issues, suggest features, or contribute code via issues and pull requests.

## License

Congrads is licensed under the [MIT License with a Commons Clause](LICENSE). This means you are free to use, modify, and distribute the software, but you may not sell or offer it as part of a paid service without permission. We encourage companies that are interested in a collaboration for a specific topic to contact the authors for more information.

---

Elevate your neural networks with Congrads! 🚀
