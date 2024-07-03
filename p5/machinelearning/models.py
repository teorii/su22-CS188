import nn

class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        return nn.DotProduct(x, self.get_weights())

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        if nn.as_scalar(PerceptronModel.run(self, x)) >= 0:
            return 1
        return -1

    def train(self, dataset):
        """
        Train the perceptron until convergence.
        """
        training = True
        while training:
            training = False
            for x, y in dataset.iterate_once(1):
                p = self.get_prediction(x)
                if p != nn.as_scalar(y):
                    training = True
                    self.w.update(x,nn.as_scalar(y))

class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """
    def __init__(self):
        # Initialize your model parameters here
        self.batch_size = 20
        self.learning_rate = -0.001
        self.fw = nn.Parameter(1, 15)
        self.fb = nn.Parameter(1,15)
        self.sw = nn.Parameter(15, 10)
        self.sb = nn.Parameter(1,10)
        self.tw = nn.Parameter(10,1)
        self.tb = nn.Parameter(1,1)

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        batch1 = nn.ReLU(nn.AddBias(nn.Linear(x, self.fw), self.fb))
        batch2 = nn.ReLU(nn.AddBias(nn.Linear(batch1, self.sw), self.sb))
        return nn.AddBias(nn.Linear(batch2, self.tw), self.tb)

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        return nn.SquareLoss(self.run(x), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        diff = float("inf")
        lloss = None
        while diff > 0.000035:
            for x, y in dataset.iterate_once(self.batch_size):
                loss = self.get_loss(x, y)
                if lloss:
                    diff = abs(nn.as_scalar(loss)-nn.as_scalar(lloss))
                lloss = loss
                if diff > 0.0001:
                    grad = nn.gradients(loss, [self.fw, self.fb, self.sw, self.sb, self.tw, self.tb])
                    self.fw.update(grad[0], self.learning_rate)
                    self.fb.update(grad[1], self.learning_rate)
                    self.sw.update(grad[2], self.learning_rate)
                    self.sb.update(grad[3], self.learning_rate)
                    self.tw.update(grad[4], self.learning_rate)
                    self.tb.update(grad[5], self.learning_rate)

class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize your model parameters here
        self.bsize = 10
        self.learning_rate = -0.05
        self.fw = nn.Parameter(784, 49)
        self.fb = nn.Parameter(1, 49)
        self.sw = nn.Parameter(49, 98)
        self.sb = nn.Parameter(1, 98)
        self.tw = nn.Parameter(98, 10)
        self.tb = nn.Parameter(1, 10)

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        batch1 = nn.ReLU(nn.AddBias(nn.Linear(x, self.fw), self.fb))
        batch2 = nn.ReLU(nn.AddBias(nn.Linear(batch1, self.sw), self.sb))
        return nn.AddBias(nn.Linear(batch2, self.tw), self.tb)

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        return nn.SoftmaxLoss(self.run(x), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        while dataset.get_validation_accuracy() < 0.97:
            for x, y in dataset.iterate_once(self.bsize):
                loss = self.get_loss(x, y)
                grad = nn.gradients(loss, [self.fw, self.sw, self.tw, self.fb, self.sb, self.tb])
                self.fw.update(grad[0], self.learning_rate)
                self.fb.update(grad[3], self.learning_rate)
                self.sw.update(grad[1], self.learning_rate)
                self.sb.update(grad[4], self.learning_rate)
                self.tw.update(grad[2], self.learning_rate)
                self.tb.update(grad[5], self.learning_rate)

class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]

        # Initialize your model parameters here
        self.bsize = 10
        self.learning_rate = -0.015
        self.fw = nn.Parameter(self.num_chars, 400)
        self.sw = nn.Parameter(400, 400)
        self.sb = nn.Parameter(1, 400)
        self.fb = nn.Parameter(1, 400)
        self.tw = nn.Parameter(400, 5)
        self.tb = nn.Parameter(1, 5)

    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)
        """
        v = nn.Linear(nn.DataNode(xs[0].data), self.fw)
        for element in xs:
            v = nn.ReLU(nn.AddBias(nn.Linear(nn.Add(nn.Linear(element, self.fw), v), self.sw), self.sb))
        return nn.AddBias(nn.Linear(v, self.tw), self.tb)

    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        return nn.SoftmaxLoss(self.run(xs), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        while dataset.get_validation_accuracy() < 0.825:
            for x, y in dataset.iterate_once(self.bsize):
                loss = self.get_loss(x, y)
                grad = nn.gradients(loss, [self.fw, self.sw, self.tw, self.fb, self.sb, self.tb])
                self.fw.update(grad[0], self.learning_rate)
                self.fb.update(grad[3], self.learning_rate)
                self.sw.update(grad[1], self.learning_rate)
                self.sb.update(grad[4], self.learning_rate)
                self.tw.update(grad[2], self.learning_rate)
                self.tb.update(grad[5], self.learning_rate)
