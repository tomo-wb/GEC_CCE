# python2 kj_to_m2.py -in kj_all.raw -out output_file
# output: .src, .tgt and .m2
# This script is for KJ and ICNALE

__author__ = "Tomoya Mizumoto"

import codecs
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
import platform
import argparse

def get_m2_out(text):
    soup = BeautifulSoup(text, 'lxml')
    contents = soup.p.contents

    src_words = []
    tgt_words = []
    corr_info = []
    for cont in contents:
        if cont.name == None:
            if cont != " ":
                w = word_tokenize(cont)
                src_words.extend(w)
                tgt_words.extend(w)
        else:
            if len(cont.find_all()) > 0:
                src, tags = extract(cont.contents)
                tags.append(cont.name)
                tgt = word_tokenize(cont["crr"])
                s = len(src_words)
                e = s + len(src)
                tag = "-".join(tags)
            else:
                src = word_tokenize(cont.text)
                tgt = word_tokenize(cont["crr"])
                tag = cont.name
                s = len(src_words)
                e = s + len(src)
            m2 = "A " + str(s) + " " + str(e) + "|||" + tag + "|||" + " ".join(tgt) + "|||REQUIRED|||-NONE-|||0"
            corr_info.append(m2)
            src_words.extend(src)
            tgt_words.extend(tgt)

    return " ".join(src_words).encode('utf-8'), " ".join(tgt_words).encode('utf-8'), corr_info

def extract(contents):
    src = []
    tags = []
    for cont in contents:
        if cont.name == None:
            src.extend(word_tokenize(cont))
        elif len(cont.find_all()) > 0:
            s, t = extract(cont.contents)
            src.extend(s)
            tags.extend(t)
        else:
            tags.append(cont.name)
            src.extend(word_tokenize(cont.text))
    return src, tags

def main():
    assert platform.python_version_tuple()[0] == '2', 'This program supports only python2'
    args = parse_args()
    input_file = args.input
    output_file = args.output

    texts = []
    with codecs.open(input_file, 'r', encoding='utf8') as f:
        for line in f:
            line = line.rstrip('\n')
            # do not use a sentence with "uk" or "f" tags
            # do not use a sentence whose "crr" is unknown (???)
            if not "<uk>" in line and not "<f>" in line and not "crr=\"???\"" in line and not "<uk " in line:
                texts.append("<p>" + line + "</p>")

    m2_output = []
    tgt_sents = []
    src_sents = []
    for text in texts:
        src_text, tgt_text, corr_info = get_m2_out(text)
        tgt_sents.append(tgt_text)
        src_sents.append(src_text)
        m2_output.append("S " + src_text)
        for corr in corr_info:
            m2_output.append(corr.encode('utf-8'))
        m2_output.append("")
    output(output_file + ".m2", m2_output)
    output(output_file + ".src", src_sents)
    output(output_file + ".tgt", tgt_sents)

def output(output_file, output_texts):
    with open(output_file, mode='w') as f:
        for text in output_texts:
            f.write(str(text) + "\n")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-in", "--input", dest="input", type=str, metavar='<str>', required=True, help="The path to the input data")
    parser.add_argument("-out", "--output", dest="output", type=str, metavar='<str>', required=True, help="The file mame of the output")

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main()
