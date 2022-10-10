# K-RET: Knowledgeable Biomedical Relation Extraction System based on BERT

K-RET is a flexible biomedical RE system, allowing for the use of any pre-trained BERT-based system (e.g., SciBERT and BioBERT) to inject knowledge in the form of knowledge graphs from a single source or multiple sources simultaneously. This knowledge can be applied to various contextualizing tokens or just to the tokens of the candidate relation for single and multi-token entities.

Our academic paper which describes K-RET in detail can be found [here]().

The [uer](/uer/) folder corresponds to an updated version of the toolkit developed by [Zhao et al. (2019)](https://aclanthology.org/D19-3041) available [here](https://github.com/dbiir/UER-py). 

## Downloading Pre-Trained Models

Available versions of the best performing pre-trained models are as follows:

* [DRUG-DRUG]()
* [DRUG-DISEASE]()
* [GENE-PHENOTYPE]()

The training details are described in our academic paper.

## Getting Started

Our project includes code adaption of the K-BERT model available [here](https://github.com/autoliuweijie/K-BERT).

Use the [K-RET Image](https://hub.docker.com/r/dpavot/kret) available at Docker Hub to set up the experimental environment.

### Usage Example:

````
 CUDA_VISIBLE_DEVICES='1,2,3' python3 -u run_classification.py \
    --pretrained_model_path ./models/pre_trained_model_scibert/output_model.bin \
    --config_path ./models/pre_trained_model_scibert/scibert_scivocab_uncased/config.json \
    --vocab_path ./models/pre_trained_model_scibert/scibert_scivocab_uncased/vocab.txt \
    --train_path ./datasets/ddi_corpus/train.tsv \
    --dev_path ./datasets/ddi_corpus/dev.tsv \
    --test_path ./datasets/ddi_corpus/test.tsv \
    --epochs_num 30 \
    --batch_size 32 \
    --kg_name "['ChEBI']" \
    --output_model_path ./outputs/scibert_ddi.bin | tee ./outputs/scibert_ddi.log &
````

For more options check [**run.sh**](/run.sh) and, for additional configuration settings (e.g., max_number_entities and contextual_knowledge), check [**brain/config.py**](/brain/config.py).

## Reference

- Diana Sousa and Francisco M. Couto. 2022. K-RET: Knowledgeable Biomedical Relation Extraction System based on BERT.