import tensorflow as tf
from tensorflow.keras import optimizers

class MAML:
    def __init__(self, model, meta_lr, task_lr, inner_steps=1):
        """
        Initialize the MAML model.
        
        :param model: A Keras model instance.
        :param meta_lr: Meta-learning rate.
        :param task_lr: Task-specific learning rate.
        :param inner_steps: Number of inner loop steps.
        """
        self.model = model
        self.meta_optimizer = optimizers.Adam(learning_rate=meta_lr)
        self.task_optimizer = optimizers.SGD(learning_rate=task_lr)
        self.inner_steps = inner_steps

    def train_step(self, support_set, query_set):
        """
        Perform one meta-training step.
        
        :param support_set: Support set data (x, y).
        :param query_set: Query set data (x, y).
        :return: Meta-loss.
        """
        with tf.GradientTape() as meta_tape:
            meta_loss = 0.0
            for (x_spt, y_spt), (x_qry, y_qry) in zip(support_set, query_set):
                with tf.GradientTape() as task_tape:
                    y_pred = self.model(x_spt, training=True)
                    task_loss = tf.reduce_mean(tf.losses.sparse_categorical_crossentropy(y_spt, y_pred))
                
                # Compute gradients and update task-specific parameters
                task_gradients = task_tape.gradient(task_loss, self.model.trainable_variables)
                task_optimized_weights = [w - self.task_optimizer.learning_rate * g for w, g in zip(self.model.trainable_variables, task_gradients)]
                
                # Inner loop
                for _ in range(self.inner_steps - 1):
                    with tf.GradientTape() as inner_task_tape:
                        y_pred = self.model(x_spt, training=True)
                        task_loss = tf.reduce_mean(tf.losses.sparse_categorical_crossentropy(y_spt, y_pred))
                    
                    task_gradients = inner_task_tape.gradient(task_loss, self.model.trainable_variables)
                    task_optimized_weights = [w - self.task_optimizer.learning_rate * g for w, g in zip(task_optimized_weights, task_gradients)]
                
                # Evaluate on query set
                y_pred = self.model(x_qry, training=True)
                query_loss = tf.reduce_mean(tf.losses.sparse_categorical_crossentropy(y_qry, y_pred))
                meta_loss += query_loss
        
        # Compute meta-gradients and update meta-parameters
        meta_gradients = meta_tape.gradient(meta_loss, self.model.trainable_variables)
        self.meta_optimizer.apply_gradients(zip(meta_gradients, self.model.trainable_variables))
        
        return meta_loss
