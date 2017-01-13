from slackclient import SlackClient
import time
from konlpy.tag import Twitter
import nltk
import numpy as np
from math import log
import random

EXAMPLE_COMMAND = "섭섭"

slack_client = SlackClient('API_TOKEN')

t = Twitter()

question = []
question.append('뭐 할 줄 알아?')
question.append('사무실 주소는?')
question.append('점심에 뭐 먹지?')

def parse_slack(msg):
    output_list = msg
    # print(output_list)
    # print(len(output_list))

    if output_list and len(output_list) > 0:
        for output in output_list:
            print(output)

            if output and 'text' in output and 'bot_id' not in output:
                command = output['text']
                question_index = question_tfidf(command)
                answer = slack_answer(question_index)

                if command.startswith(EXAMPLE_COMMAND):
                    slack_client.api_call(
                        "chat.postMessage",
                        channel=output['channel'],
                        text=answer,
                        username='섭섭이',
                        icon_emoji=':ghost:'
                    )

    return None

def slack_answer(i):
    if i == 1:
        answer = "[코멘토] 서울시 종로구 동호로 38길 23 (종로5가, 3층)\n070-4154-0804"
    elif i == 2:
        menu = ['야미가','서브웨이','순두부','김치찌개','생선구이','국밥','연어?']
        answer = random.choice(menu)
    else:
        answer = "섭섭이는 지금 사무실 주소를 알고 점심을 추천할 수 있어요"

    return answer

def question_tfidf(q):
    # 질문 형태소 분석
    nouns = t.morphs(q)
    ko = nltk.Text(nouns, name='')
    nouns = ko.vocab()

    # 학습 문장 형태소 분석
    question_nouns = [t.morphs(row) for row in question]

    i = 0
    for noun in question_nouns:
        ko = nltk.Text(question_nouns[i], name='')
        question_nouns[i] = ko.vocab()
        i += 1

    # 문서 유사도 탐색
    q_tfidf = []
    i = 0
    for q_nouns in question_nouns:
        tfidf = []
        for n in nouns:
            try:
                tf = [q_nouns[key] for key in q_nouns if key in n][0] / np.sum([q_nouns[key] for key in q_nouns])
            except IndexError:
                tf = 0

            j = 0
            for d in question:
                if n in d:
                    j += 1
            try:
                idf = log(len(question) / j)
            except ZeroDivisionError:
                idf = 0

            tfidf.append(tf*idf)

        print(np.sum(tfidf))
        q_tfidf.append(np.sum(tfidf))
        i += 1

    return q_tfidf.index(np.amax(q_tfidf))

if __name__ == "__main__":
    if slack_client.rtm_connect():
        print("Connected!")
        while True:
            parse_slack(slack_client.rtm_read())
            time.sleep(1)
    else:
        print("Connection failed.")
