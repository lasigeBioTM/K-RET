#!/usr/bin/env bash

set -e

# Running Example

CUDA_VISIBLE_DEVICES='0' python3 -u run_classification.py \
    --pretrained_model_path ./models/pre_trained_model_scibert/output_model.bin \
    --config_path ./models/pre_trained_model_scibert/scibert_scivocab_uncased/config.json \
    --vocab_path ./models/pre_trained_model_scibert/scibert_scivocab_uncased/vocab.txt \
    --train_path ./datasets/ddi_corpus/train.tsv \
    --dev_path ./datasets/ddi_corpus/dev.tsv \
    --test_path ./datasets/ddi_corpus/test.tsv \
    --epochs_num 30 --batch_size 32 --kg_name "[]" \
    --testing True \
    --to_test_model ./outputs/scibert_ddi.bin \
    | tee ./outputs/ddi_results.log &

# python3 src/process_results.py ./outputs/ddi_results.log ./datasets/ddi_corpus/test.tsv ddi_results.tsv


