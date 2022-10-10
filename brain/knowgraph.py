# coding: utf-8

import os
import string

# import config
from brain import config   # switch to previous line in docker
import numpy as np
from nltk.util import everygrams
from nltk.tokenize import word_tokenize
import nltk
import string
import ssmpy
import obonet
nltk.download('punkt')


def sent_everygram(sent_split):
    """

    :param sent_split:
    :return:
    """

    combinations = list(everygrams(sent_split))
    save_combinations = []

    for gram in combinations:
        save_combinations.append(' '.join(gram))

    return save_combinations


def auxiliary_organization(annotated_sentence):
    """

    :param annotated_sentence:
    :return:
    """

    punctuation = string.punctuation

    new_sentence = []
    index = 0
    counter = 0

    if annotated_sentence[-1] != ('.', []):  # for sentences that don't end with a period, we added a period
        annotated_sentence.append(('.', []))

    for element in annotated_sentence:

        combination_left = ' ' + element[0]
        combination_right = element[0] + ' '

        if counter > 1:
            counter -= 1

        elif index == 0:
            if combination_left in annotated_sentence[index + 1][0] or combination_right in \
                    annotated_sentence[index + 1][0]:
                pass
            else:
                new_sentence.append(element)

        elif element[0] in punctuation:
            new_sentence.append(element)

        elif combination_left in annotated_sentence[index - 1][0] or combination_right in annotated_sentence[index - 1][0]:
            while ' ' + annotated_sentence[index + counter][0] in annotated_sentence[index - 1][0] \
                    or annotated_sentence[index + counter][0] + ' ' in annotated_sentence[index - 1][0]:
                counter += 1
            pass

        elif combination_left in annotated_sentence[index + 1][0] or combination_right in annotated_sentence[index + 1][0]:
            pass

        else:
            new_sentence.append(element)

        index += 1

    return new_sentence


class KnowledgeGraph(object):
    """
    spo_files - list of Path of *.spo files, or default kg name. e.g., ['HowNet']
    """

    def __init__(self, spo_files, predicate=False):
        self.training = config.CONTEXTUAL_KNOWLEDGE
        self.predicate = predicate
        self.spo_files = spo_files
        self.spo_file_paths = [config.KGS.get(f, f) for f in spo_files]
        self.lookup_table = self._create_lookup_table()
        self.segment_vocab = list(self.lookup_table.keys()) + config.NEVER_SPLIT_TAG
        self.special_tags = set(config.NEVER_SPLIT_TAG)

    def _create_lookup_table(self):

        lookup_table = {}

        for spo_path in self.spo_file_paths:
            print("[KnowledgeGraph] Loading spo from {}".format(spo_path))
            with open(spo_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        subj, pred, obje = line.strip().split("\t")
                    except:
                        print("[KnowledgeGraph] Bad spo:", line)
                    if self.predicate:
                        value = pred + obje
                    else:
                        value = obje
                    if subj in lookup_table.keys():
                        lookup_table[subj].add(value)
                    else:
                        lookup_table[subj] = set([value])
        return lookup_table

    def add_knowledge_with_vm(self, sent_batch, max_entities=config.MAX_ENTITIES, add_pad=True, max_length=128):
        """
        input: sent_batch - list of sentences, e.g., ["abcd", "efgh"]
        return: know_sent_batch - list of sentences with entites embedding
                position_batch - list of position index of each character.
                visible_matrix_batch - list of visible matrixs
                seg_batch - list of segment tags
        """

        split_sent_batch = [word_tokenize(sent) for sent in sent_batch]
        # print(split_sent_batch)

        know_sent_batch = []
        position_batch = []
        visible_matrix_batch = []
        seg_batch = []
        for split_sent in split_sent_batch:

            # create tree
            sent_tree = []
            pos_idx_tree = []
            abs_idx_tree = []
            pos_idx = -1
            abs_idx = -1
            abs_idx_src = []

            combinations = sent_everygram(split_sent)  # accommodate multiple word annotations

            if self.training:
                pass
            else:
                # just entity knowledge #
                used_tokens = []
                # END just entity knowledge #

            for token in combinations:
                number_tokens = len(token.split(' '))

                if self.training:
                    # all knowledge #
                    entities = list(self.lookup_table.get(token, []))[:max_entities]
                    number_tokens = len(token.split(' '))
                    if entities or number_tokens == 1:
                        sent_tree.append((token, entities))
                    # END all knowledge #

                else:
                    # just entity knowledge #
                    entities = []
                    if token.startswith('< e1 >') and token.endswith('< /e1 >') or token.startswith('< e2 >') and token.endswith('< /e2 >'):
                        entity_token = token[7:-8]
                        entities = list(self.lookup_table.get(entity_token, []))[:max_entities]
                        number_tokens = 0

                    if entities:
                        sent_tree.append((token[7:-8], entities))
                        used_tokens.append(token[7:-8])

                    elif number_tokens == 1 and token not in ['<', '>', 'e1', 'e2', '/e1', '/e2'] and token not in used_tokens:
                        sent_tree.append((token, entities))
                    # END just entity knowledge #

            sent_tree = auxiliary_organization(sent_tree)

            try:  # guarantee good annotation
                len(sent_tree) == len(split_sent)
            except Exception:
                raise Exception('Sentence annotation error, check sentence', split_sent + '.')

            for elements in sent_tree:

                token = elements[0]
                entities = elements[1]

                if token in self.special_tags:
                    token_pos_idx = [pos_idx + 1]
                    token_abs_idx = [abs_idx + 1]
                else:
                    token_pos_idx = [pos_idx + i for i in range(1, len(token) + 1)]
                    token_abs_idx = [abs_idx + i for i in range(1, len(token) + 1)]
                abs_idx = token_abs_idx[-1]

                entities_pos_idx = []
                entities_abs_idx = []
                for ent in entities:
                    ent_pos_idx = [token_pos_idx[-1] + i for i in range(1, len(ent) + 1)]
                    entities_pos_idx.append(ent_pos_idx)
                    ent_abs_idx = [abs_idx + i for i in range(1, len(ent) + 1)]
                    abs_idx = ent_abs_idx[-1]
                    entities_abs_idx.append(ent_abs_idx)

                pos_idx_tree.append((token_pos_idx, entities_pos_idx))
                pos_idx = token_pos_idx[-1]
                abs_idx_tree.append((token_abs_idx, entities_abs_idx))
                abs_idx_src += token_abs_idx

            # Get know_sent and pos
            know_sent = []
            pos = []
            seg = []
            for i in range(len(sent_tree)):
                word = sent_tree[i][0]
                if word in self.special_tags:
                    know_sent += [word]
                    seg += [0]
                else:
                    add_word = list(word)
                    know_sent += add_word
                    seg += [0] * len(add_word)
                pos += pos_idx_tree[i][0]
                for j in range(len(sent_tree[i][1])):
                    add_word = list(sent_tree[i][1][j])
                    know_sent += add_word
                    seg += [1] * len(add_word)
                    pos += list(pos_idx_tree[i][1][j])

            token_num = len(know_sent)

            # Calculate visible matrix
            visible_matrix = np.zeros((token_num, token_num))
            for item in abs_idx_tree:
                src_ids = item[0]
                for id in src_ids:
                    visible_abs_idx = abs_idx_src + [idx for ent in item[1] for idx in ent]
                    visible_matrix[id, visible_abs_idx] = 1
                for ent in item[1]:
                    for id in ent:
                        visible_abs_idx = ent + src_ids
                        visible_matrix[id, visible_abs_idx] = 1

            src_length = len(know_sent)
            if len(know_sent) < max_length:
                pad_num = max_length - src_length
                know_sent += [config.PAD_TOKEN] * pad_num
                seg += [0] * pad_num
                pos += [max_length - 1] * pad_num
                visible_matrix = np.pad(visible_matrix, ((0, pad_num), (0, pad_num)), 'constant')  # pad 0
            else:
                know_sent = know_sent[:max_length]
                seg = seg[:max_length]
                pos = pos[:max_length]
                visible_matrix = visible_matrix[:max_length, :max_length]

            know_sent_batch.append(know_sent)
            position_batch.append(pos)
            visible_matrix_batch.append(visible_matrix)
            seg_batch.append(seg)

        return know_sent_batch, position_batch, visible_matrix_batch, seg_batch


# TEST

# hpo = KnowledgeGraph(['ChEBI', 'HPO'])
# hpo.add_knowledge_with_vm(["The <e1>venlafaxine</e1> something, <e2>seizure</e2> invented incomplete male pseudohermaphroditism."])
