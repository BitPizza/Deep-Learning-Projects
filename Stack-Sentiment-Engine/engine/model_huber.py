import tensorflow as tf

class Model:
    
    def __init__(self, num_layers, size_layer, dimension_input, dimension_output, learning_rate):
        def lstm_cell():
            return tf.nn.rnn_cell.LSTMCell(size_layer)
        self.rnn_cells = tf.nn.rnn_cell.MultiRNNCell([lstm_cell() for _ in range(num_layers)])
        self.X = tf.placeholder(tf.float32, [None, None, dimension_input])
        self.Y = tf.placeholder(tf.float32, [None, dimension_output])
        drop = tf.contrib.rnn.DropoutWrapper(self.rnn_cells, output_keep_prob = 0.5)
        self.outputs, self.last_state = tf.nn.dynamic_rnn(drop, self.X, dtype = tf.float32)
        self.rnn_W = tf.Variable(tf.random_normal((size_layer, dimension_output)))
        self.rnn_B = tf.Variable(tf.random_normal([dimension_output]))
        self.logits = tf.matmul(self.outputs[:, -1], self.rnn_W) + self.rnn_B
        self.cost = tf.losses.huber_loss(predictions = self.logits, labels = self.Y)
        self.optimizer = tf.train.AdamOptimizer(learning_rate = learning_rate).minimize(self.cost)
        self.correct_pred = tf.equal(tf.argmax(self.logits, 1), tf.argmax(self.Y, 1))
        self.accuracy = tf.reduce_mean(tf.cast(self.correct_pred, tf.float32))