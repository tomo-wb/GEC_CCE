# Preprocess code for for Cross-Corpora Evaluation of Grammatical Error Correction
This repository contains the Preprocess code for Cross-Corpora Evaluation of Grammatical Error Correction described in :

> Masato Mita, Tomoya Mizumoto, Masahiro Kaneko, Ryo Nagata and Kentaro Inui. 2019. [**Cross-Corpora Evaluation and Analysis of Grammatical Error Correction Models — Is Single-Corpus Evaluation Enough?**](https://www.aclweb.org/anthology/N19-1132.pdf). In Proceedings of the 17th Annual Conference of the North American Chapter of the Association for Computational Linguistics. Minneapolis, USA.


If you make use of this code, please cite the above papers.



## Pre-requisites

We only support Python 2. It is safest to install everything in a clean [virtualenv](https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv).

It can be installed  as follows:  
```
pip install -r requirements.txt
```
 (**NOTE**: To get the exact data you may need to use  NLTK v2.0b7 for tokenization. )


## Data Preparation for Cross-Corpora Evaluation
To convert raw data (.xml) to m2 format use the following preprocessing script. 

```
## CLC-FCE
python2 clcfce_to_m2.py -in dataset/ -out output

## KJ/ICNLAE
python2 kj_to_m2.py -in kj_all.raw -out output_file
```


### Preprocessing Scripts for the Other Corpora
For the other corpora we used such as CoNLL-2014, 2013 and JFELG, you can use the following official preprocessing scripts.

* CoNLL 2014
  * http://www.comp.nus.edu.sg/~nlp/conll14st.html

* CoNLL 2013
  * http://www.comp.nus.edu.sg/~nlp/conll13st.html

* JFLEG
    * https://github.com/keisks/jfleg

### Evaluation 

You can evaluate your systems using the following scorers (M2socorer and GLUE).

* M2scorer
    * https://github.com/nusnlp/m2scorer
* GLEU
    * https://github.com/cnap/gec-ranking
