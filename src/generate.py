"""
This module is converted from the procedural script here
https://github.com/imcaspar/gpt2-ml/blob/master/scripts/demo.py
Additionally, refactoring was done to separate the model loading from generation
So the model doesn't have to be loaded everytime we run generation
"""

import os
import re
import tensorflow.compat.v1 as tf
import numpy as np
from train.modeling import GroverConfig, sample
from tokenization import tokenization


class Generate(object):

    def __init__(self):
        # TODO: move the hardcoded vars into a configuration file
        ckpt_fn = '../model/model.ckpt-430000'
        config_fn = 'configs/mega.json'
        vocab_file_path = "tokenization/clue-vocab.txt"
        batch_size = 1
        max_batch_size = None

        self.top_p = 0.95
        self.min_len_value = 1024
        self.eos_token_value = 102

        # ignore tf deprecated warning temporarily
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
        tf.logging.set_verbosity(tf.logging.DEBUG)
        from tensorflow.python.util import deprecation

        deprecation._PRINT_DEPRECATION_WARNINGS = False
        try:
            from tensorflow.python.util import module_wrapper as deprecation
        except ImportError:
            from tensorflow.python.util import deprecation_wrapper as deprecation
        deprecation._PER_MODULE_WARNING_LIMIT = 0
        #####

        self.tokenizer = tokenization.FullTokenizer(vocab_file=vocab_file_path, do_lower_case=True)

        news_config = GroverConfig.from_json_file(config_fn)

        # We might have to split the batch into multiple chunks if the batch size is too large
        default_mbs = {12: 32, 24: 16, 48: 3}
        max_batch_size = max_batch_size if max_batch_size is not None else default_mbs[news_config.num_hidden_layers]

        # factorize batch_size = (num_chunks * batch_size_per_chunk) s.t. batch_size_per_chunk < max_batch_size
        self.num_chunks = int(np.ceil(batch_size / max_batch_size))
        self.batch_size_per_chunk = int(np.ceil(batch_size / self.num_chunks))

        # This controls the top p for each generation.
        self.top_p = np.ones((self.num_chunks, self.batch_size_per_chunk), dtype=np.float32) * self.top_p

        tf_config = tf.ConfigProto(allow_soft_placement=True)
        self.sess = tf.Session(config=tf_config)

        self.initial_context = tf.placeholder(tf.int32, [self.batch_size_per_chunk, None])
        self.p_for_topp = tf.placeholder(tf.float32, [self.batch_size_per_chunk])
        self.eos_token = tf.placeholder(tf.int32, [])
        self.min_len = tf.placeholder(tf.int32, [])

        self.tokens, self.probs = sample(news_config=news_config, initial_context=self.initial_context,
                                         eos_token=self.eos_token, min_len=self.min_len, ignore_ids=None,
                                         p_for_topp=self.p_for_topp,
                                         do_topk=False)

        saver = tf.train.Saver()
        saver.restore(self.sess, ckpt_fn)

    def generate(self, prefix):
        line = tokenization.convert_to_unicode(prefix)
        bert_tokens = self.tokenizer.tokenize(line)
        encoded = self.tokenizer.convert_tokens_to_ids(bert_tokens)
        context_formatted = []
        context_formatted.extend(encoded)
        # Format context end

        gens = []
        for chunk_i in range(self.num_chunks):
            tokens_out, probs_out = self.sess.run([self.tokens, self.probs],
                                                  feed_dict={self.initial_context: [context_formatted] * self.batch_size_per_chunk,
                                                             self.eos_token: self.eos_token_value,
                                                             self.min_len: self.min_len_value,
                                                             self.p_for_topp: self.top_p[chunk_i]})
            for t_i, p_i in zip(tokens_out, probs_out):
                extraction = self.extract_generated_target(output_tokens=t_i)
                gens.append(extraction['extraction'])
        generated = re.findall('.{1,70}', gens[0].replace('[UNK]', '').replace('##', ''))
        generated = "".join(generated)

        # TODO: removing the prefix from generated result is not working intermittently.
        #  This may be due to the prefix containing punctuation, or certain special chars. Need to investigate.
        generated = generated.replace(prefix, "")

        return generated

    def extract_generated_target(self, output_tokens):
        """
        Given some tokens that were generated, extract the target
        :param output_tokens: [num_tokens] thing that was generated
        :return:
        """
        # Filter out first instance of start token
        assert output_tokens.ndim == 1

        start_ind = 0
        end_ind = output_tokens.shape[0]

        return {
            'extraction': tokenization.printable_text(''.join(self.tokenizer.convert_ids_to_tokens(output_tokens))),
            'start_ind': start_ind,
            'end_ind': end_ind,
        }
