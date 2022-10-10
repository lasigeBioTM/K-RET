#!/usr/bin/env bash

set -e

# Running Example

CUDA_VISIBLE_DEVICES='1,2,3' python3 -u run_classification.py \
    --pretrained_model_path ./models/pre_trained_model_scibert/output_model.bin \
    --config_path ./models/pre_trained_model_scibert/scibert_scivocab_uncased/config.json \
    --vocab_path ./models/pre_trained_model_scibert/scibert_scivocab_uncased/vocab.txt \
    --train_path ./datasets/ddi_corpus/train.tsv \
    --dev_path ./datasets/ddi_corpus/dev.tsv \
    --test_path ./datasets/ddi_corpus/test.tsv \
    --epochs_num 30 --batch_size 32 --kg_name "['ChEBI']" \
    --output_model_path ./outputs/scibert_ddi.bin \
    | tee ./outputs/scibert_ddi.log &

# --kg_name is a list of knowledge graphs names, e.g. ['GO','HPO'], ['ChEBI','DOID'] and ['ChEBI']
