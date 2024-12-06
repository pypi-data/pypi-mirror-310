"""A simple script to demonstrate tensorflow."""
from __future__ import annotations

import tensorflow

if __name__ == "__main__":
    import tensorflow as tf

    tf.add(1, 2).numpy()

    hello = tf.constant("Hello, TensorFlow!")
    hello.numpy()
