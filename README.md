# python-slackbot #

##배경##
[Modern PHP](https://www.facebook.com/groups/655071604594451/) 그룹에서 전창완님의 [PHP로 Slack Bot 만들기 (전창완)](https://github.com/ModernPUG/meetup/blob/master/2016_12/02_PHP_Slack_Bot.md) 글을 보고
한창 Python을 공부하고 있는 중이라 Python으로 봇을 만들어 보았다.

슬랙에서 제공하는 [Real Time Messaging API](https://api.slack.com/rtm)를 이용한다.

##Process##
rtm.connect를 이용하여 연결을 한다. 그럼 봇에 접속표시(파란불 표시)가 된다.
rtm.read를 통해 메세지를 받는다. 단, 받는 메세지는 ```while True:```를 통해 무한루프로 돌린다.
질문이 들어오면 학습된 질문과 tf-idf 유사도 가장 높은 질문을 선택한다.
해당 질문에 맞는 대답을 한다.
