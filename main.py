import re
import logging
from slackbot.bot import Bot
from slackbot.bot import respond_to
from slackbot.bot import listen_to
import boto3


logger = logging.getLogger(__name__)
AWS_REGION = 'ap-northeast-1'


@respond_to('hi', re.IGNORECASE)
def hi(message):
    message.reply('HI!')
    message.react('+1')


@respond_to('AWS Region', re.IGNORECASE)
def aws_region(message):
    text = '''
    バージニア北部  : us-east-1
    オハイオ        : us-east-2
    北カリフォルニア: us-west-1
    オレゴン        : us-west-2
    カナダ          : ca-central-1
    フランクフルト  : eu-central-1
    アイルランド    : eu-west-1
    ロンドン        : eu-west-2
    パリ            : eu-west-3
    東京            : ap-northeast-1
    ソウル          : ap-northeast-2
    大阪            : ap-northeast-3
    シンガポール    : ap-southeast-1
    シドニー        : ap-southeast-2
    ムンバイ        : ap-south-1
    サンパウロ      : sa-east-1
    '''
    message.reply(text)


@respond_to('Attack (.*)', re.IGNORECASE)
def slack_vegeta(message, request):
    sqs_queue_name = "vegeta-queue"
    sqs = boto3.resource('sqs', region_name=AWS_REGION)
    queue = sqs.get_queue_by_name(QueueName=sqs_queue_name)
    channel_id = message.channel
    response = queue.send_message(MessageBody=request,
                                  MessageAttributes={
                                      'ChannelID': {
                                          'StringValue': channel_id._body['id'],
                                          'DataType': 'String'}})
    logger.info(response)
    message.reply("Http attack will soon begin !" + request + channel_id._body['id'])


@listen_to('Can someone help me?')
def help(message):
    # Message is replied to the sender (prefixed with @user)
    message.reply('Yes, I can!')

    # Message is sent on the channel
    message.send('I can help everybody!')

    # Start a thread on the original message
    message.reply("Here's a threaded reply", in_thread=True)


def main():
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    main()
