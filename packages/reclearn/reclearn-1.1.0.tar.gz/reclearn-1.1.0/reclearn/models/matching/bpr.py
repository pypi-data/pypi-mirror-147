"""
Created on Nov 13, 2020
Updated on Apr 9, 2022
Reference: "BPR: Bayesian Personalized Ranking from Implicit Feedback", UAI, 2009
@author: Ziyao Geng(zggzy1996@163.com)
"""
import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Embedding, Input
from tensorflow.keras.regularizers import l2

from reclearn.models.losses import bpr_loss


class BPR(Model):
    def __init__(self, user_num, item_num, embed_dim, use_l2norm=False, embed_reg=0., seed=None):
        """Bayesian Personalized Ranking - Matrix Factorization
        Args:
            :param user_num: An integer type. The largest user index + 1.
            :param item_num: An integer type. The largest item index + 1.
            :param embed_dim: An integer type. Embedding dimension of user vector and item vector.
            :param use_l2norm: A boolean. Whether user embedding, item embedding should be normalized or not.
            :param embed_reg: A float type. The regularizer of embedding.
            :param seed: A Python integer to use as random seed.
        :return:
        """
        super(BPR, self).__init__()
        # user embedding
        self.user_embedding = Embedding(input_dim=user_num,
                                        input_length=1,
                                        output_dim=embed_dim,
                                        embeddings_initializer='random_normal',
                                        embeddings_regularizer=l2(embed_reg))
        # item embedding
        self.item_embedding = Embedding(input_dim=item_num,
                                        input_length=1,
                                        output_dim=embed_dim,
                                        embeddings_initializer='random_normal',
                                        embeddings_regularizer=l2(embed_reg))
        # norm
        self.use_l2norm = use_l2norm
        # seed
        tf.random.set_seed(seed)

    def call(self, inputs):
        # user info
        user_embed = self.user_embedding(tf.reshape(inputs['user'], [-1, ]))  # (None, embed_dim)
        # item info
        pos_info = self.item_embedding(tf.reshape(inputs['pos_item'], [-1, ]))  # (None, embed_dim)
        neg_info = self.item_embedding(inputs['neg_item'])  # (None, neg_num, embed_dim)
        # norm
        if self.use_l2norm:
            pos_info = tf.math.l2_normalize(pos_info, axis=-1)
            neg_info = tf.math.l2_normalize(neg_info, axis=-1)
            user_embed = tf.math.l2_normalize(user_embed, axis=-1)
        # calculate positive item scores and negative item scores
        pos_scores = tf.reduce_sum(tf.multiply(user_embed, pos_info), axis=-1, keepdims=True)  # (None, 1)
        neg_scores = tf.reduce_sum(tf.multiply(tf.expand_dims(user_embed, axis=1), neg_info), axis=-1)  # (None, neg_num)
        # add loss
        self.add_loss(bpr_loss(pos_scores, neg_scores))
        logits = tf.concat([pos_scores, neg_scores], axis=-1)
        return logits

    def get_user_vector(self, inputs):
        if len(inputs) < 2 and inputs.get('user') is not None:
            return self.user_embedding(inputs['user'])

    def summary(self):
        inputs = {
            'user': Input(shape=(), dtype=tf.int32),
            'pos_item': Input(shape=(), dtype=tf.int32),
            'neg_item': Input(shape=(1,), dtype=tf.int32)  # suppose neg_num=1
        }
        Model(inputs=inputs, outputs=self.call(inputs)).summary()