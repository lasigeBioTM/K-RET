# K-RET: Knowledgeable Biomedical Relation Extraction System

K-RET is a flexible biomedical RE system, allowing for the use of any pre-trained BERT-based system (e.g., SciBERT and BioBERT) to inject knowledge in the form of knowledge graphs from a single source or multiple sources simultaneously. This knowledge can be applied to various contextualizing tokens or just to the tokens of the candidate relation for single and multi-token entities.

Our academic paper which describes K-RET in detail can be found [here](https://academic.oup.com/bioinformatics/advance-article/doi/10.1093/bioinformatics/btad174/7108769).

The [uer](/uer/) folder corresponds to an updated version of the toolkit developed by [Zhao et al. (2019)](https://aclanthology.org/D19-3041) available [here](https://github.com/dbiir/UER-py). 

## Downloading Pre-Trained Models

You should use both a baseline model and one of our pre-trained models to predict new data. If you wish to train a model on your data, you only need a baseline model, which can be either model referenced in our academic paper. 

### Baseline Models

After downloading a baseline model, for instance [Scibert](https://huggingface.co/allenai/scibert_scivocab_uncased/tree/main), the model needs to be converted using the uer toolkit. For this, you can run the following example, making the necessary adaptations given different baseline models or paths. 

````
cd K-RET/uer/
python3 convert_bert_from_huggingface_to_uer.py --input_model_path ../models/pre_trained_model_scibert/scibert_scivocab_uncased/pytorch_model.bin --output_model_path ../models/pre_trained_model_scibert/output_model.bin
````

````
cd K-RET/uer/
python3 convert_bert_from_huggingface_to_uer.py --input_model_path ../models/pre_trained_model_scibert/scibert_scivocab_uncased/pytorch_model.bin --output_model_path ../models/pre_trained_model_scibert/output_model.bin
````

### Our Models

Available versions of the best performing pre-trained models are as follows:

* [DRUG-DRUG](https://drive.google.com/drive/folders/1-XRHAz1IY5C1L5GMqKrKWxEnwIVfhU-d?usp=sharing)
* [DRUG-DISEASE](https://drive.google.com/drive/folders/10fIQlKdJEJk-C4bQkB4WkNfk0gmcgKXx?usp=sharing)
* [GENE-PHENOTYPE](https://drive.google.com/drive/folders/1GR67jrAC9jxwliPdGFvUUSolWcpvhKlO?usp=sharing)

The training details are described in our academic paper.

## Getting Started

Our project includes code adaption of the K-BERT model available [here](https://github.com/autoliuweijie/K-BERT).
Use the [K-RET Image](https://hub.docker.com/r/dpavot/kret) available at Docker Hub to set up the rest of the experimental environment.

### Usage Example

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

### Predict New Data Example

````
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
````

#### Process Results Example

````
python3 src/process_results.py ./outputs/ddi_results.log ./datasets/ddi_corpus/test.tsv ddi_results.tsv
````

## Reference

- Diana Sousa and Francisco M. Couto. 2022. K-RET: Knowledgeable Biomedical Relation Extraction System. Bioinformatics.
