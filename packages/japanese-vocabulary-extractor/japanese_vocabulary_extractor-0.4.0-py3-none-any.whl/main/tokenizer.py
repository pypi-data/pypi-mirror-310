#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard library imports
import regex as re
import logging

# Third-party imports (install these with pip)
import MeCab


def vocab_from_texts(texts: list) -> set:
    vocab = set()
    mecab = MeCab.Tagger()

    confirm_japanese_pattern = re.compile(r"[\p{IsHiragana}\p{IsKatakana}\p{IsHan}]+")
    katakana_only_pattern = re.compile(r"[\p{IsKatakana}]+")

    for text in texts:
        parsed = mecab.parse(text)
        words = parsed.split("\n")
        for word in words:
            word_info = word.split("\t")
            if word == "EOS" or word == "" or len(word_info) < 4:
                continue
            # For some reason the 4th element contains the english translation
            # for katakana-only words, so we differentiate between katakana-only
            # words and other words
            base_form = (
                word_info[0]
                if katakana_only_pattern.match(word_info[0])
                else word_info[3]
            )
            # Sometimes the base form is followed by a hyphen and more text
            base_form = base_form.split("-")[0]
            if confirm_japanese_pattern.match(base_form):
                vocab.add(base_form)

    return vocab
