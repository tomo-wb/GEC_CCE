# python clcfce_to_m2.py -in dataset/ -out output
# coding: utf-8

__author__ = "Tomoya Mizumoto"

import codecs
from bs4 import BeautifulSoup
import os
from nltk.tokenize import sent_tokenize, word_tokenize
import platform
import argparse

def get_m2_out(soup):
    conts = soup.p.contents

    src_words = []
    tgt_words = []
    corr_info = []
    for i,cont in enumerate(conts):
        tags = []
        if cont.name == None:
            if cont != " ":
                w = word_tokenize(cont)
                src_words.extend(w)
                tgt_words.extend(w)
        elif cont.name == "ns":
            corr, inc, t, ci = extract(cont)
            if not ci:
                return "", "", ""
            tags.extend(t)
            tags.append(cont["type"])
            src = word_tokenize(inc)
            tgt = word_tokenize(corr)
            tag = "-".join(tags)
            s = len(src_words)
            e = s + len(src)
            m2 = "A " + str(s) + " " + str(e) + "|||" + tag + "|||" + " ".join(tgt) + "|||REQUIRED|||-NONE-|||0"
            corr_info.append(m2)
            src_words.extend(src)
            tgt_words.extend(tgt)

    return " ".join(src_words).encode('utf-8'), " ".join(tgt_words).encode('utf-8'), corr_info

def extract(cont):
    contents = cont.contents
    corr = inc = ""
    ci = True
    tag = []
    if cont.find("i") or cont.find("c"):
        for cont in contents:
            if cont.name == "ns":
                c, i, t, ci = extract(cont)
                tag.extend(t)
                tag.append(cont["type"])
                corr = corr + c
                inc = inc + i
            elif cont.name == "i":
                if cont.find("ns"):
                    c, i, t, ci = extract(cont)
                    tag.extend(t)
                    inc = inc + i
                else:
                    inc = cont.text
            elif cont.name == "c":
                corr = cont.text
            else:
                if cont.parent.name == "i":
                    inc = inc + cont
                elif cont.parent.name == "ns":
                    corr = corr + cont
                    inc = inc + cont
    else:
        ci = False
    return corr, inc, tag, ci

def main():
    refs = []
    assert platform.python_version_tuple()[0] == '2', 'This program supports only python2'

    args = parse_args()
    input_dir = args.input
    output_file = args.output
    for dir in os.listdir(input_dir):
        for f in os.listdir(input_dir + '/' + dir):
            refs.append(input_dir + '/' + dir + '/' +f)

    m2_output = []
    tgt_sents = []
    src_sents = []
    for filename in refs:
        f = codecs.open(filename, 'r', encoding='utf8')
        xml = f.read()
        f.close()
        soup = BeautifulSoup(xml, 'lxml')
        all_tags = soup.find_all()
        for a_tag in all_tags:
            if a_tag.name == "p":
                rep_tokens = []

                contents = a_tag.contents
                for i,cont in enumerate(contents):
                    if cont.name == "ns":
                        rep_tokens.append(cont.encode('utf-8'))
                        cont.replace_with("{}")
                text = a_tag.get_text()
                texts = sent_tokenize(text)
                for i,t in enumerate(texts):
                    while "{}" in t:
                        rep = rep_tokens.pop(0).decode('utf-8')
                        t = t.replace("{}", rep, 1)
                    if len(t) > 1:
                        t = "<p>" + t + "</p>"
                        soup = BeautifulSoup(t, 'lxml')
                        src_text, tgt_text, corr_info = get_m2_out(soup)
                        if src_text != "":
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
    parser.add_argument("-in", "--input", dest="input", type=str, metavar='<str>', required=True, help="The path to the input directory")
    parser.add_argument("-out", "--output", dest="output", type=str, metavar='<str>', required=True, help="The file mame of the output")

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main()