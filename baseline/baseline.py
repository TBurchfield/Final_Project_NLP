#!/usr/bin/env python3

from collections import defaultdict
import json

def parse_comments():
    for comment in sys.stdin:
        comment = json.loads(comment)
        body = comment['body'].split()
        for word in body
            yield word, comment['ups'] / len(body)


def set_scores():
    word_score = defaultdict(int)
    for word, score in parse_comments():
        word_score[word] += score

    return word_score


if __name__ == '__main__':
    word_score = set_scores()
    for word, score in word_score.items():
        print(word, score)
