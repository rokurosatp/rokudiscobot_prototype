from util.configloader import Config
from util import tokenizer, regalias_gen
import argparse
import logging
import traceback
import discord
import re
import sys

def get_listen_reply(message: discord.Message):
    """メンションなしの場合のリアクション
    """
    if re.match(r"^(おはよう|よお|よう|Hello|はろー)", message.content):
        return "おはようございます" + message.author.name + "さん！"
    elif re.match(r"^わかり手だ", message.content):
        return "そうだよ"
    elif re.match(r"^わかる", message.content):
        return "わかり手だ"
    elif re.match(r"^わからん", message.content):
        return "いや、わかる"
    elif re.match(r"^(強そう|つよそう)", message.content):
        return "(小並感)"
    elif re.match(r"^hoge", message.content):
        return "fuga"
    elif re.match(r"^ほげ", message.content):
        return "ふが"
    elif "yo" in message.content.lower():
        return "yo"
    return None

def get_mention_reply(message: discord.Message):
    """メンションに対するリアクション
    """
    mt = re.match("^\<\@\w+\>\s*(.*)$", message.content)
    content = mt.group(1)
    if re.match(r"^(おはよう|よお|よう|Hello|はろー)", content):
        return "おはようございます" + message.author.name + "さん！"
    elif re.match(r"^わかり手だ", content):
        return "そうだよ"
    elif re.match(r"^わかる", content):
        return "わかり手だ"
    elif re.match(r"^わからん", content):
        return "いや、わかる"
    elif tokenizer.in_class_of(content, classes={"太郎", "二郎", "花子", "プリウス"}):
        return tokenizer.tokenize_mecab(content)
    elif regalias_gen.enabled() and re.match(r"^(二つ名|alias)", content):
        return regalias_gen.generate_alias()
    elif "yo" in content.lower():
        return "yo"
    return "わかる"

def main():
    conf = Config.load()
    client = discord.Client()

    @client.event
    async def on_ready():
        logging.info('Logged in as')
        logging.info("%s", client.user.name)
        logging.info("%s", client.user.id)

    def log_message_information(message: discord.Message):
        try:
            logging.debug("message.channel.name=%s", str(message.channel.name))
            logging.debug("message.is_private=%s", str(message.channel.is_private))
            if message.channel.is_private:
                logging.debug("message.channel.owner=%s", str(message.channel.owner))
                logging.debug("message.channel.recipients=%s", str(message.channel.recipients))
            logging.debug("message.channel_mentions=%s", str(message.channel_mentions))
            logging.debug("message.mentions=%s", str(message.mentions))
            logging.debug("message.mention_everyone=%s", str(message.mention_everyone))
            logging.debug("message.content=%s", str(message.content))
            logging.debug("message.clean_content=%s", str(message.clean_content))
        except:
            exc_type, exc_val, tb = sys.exc_info()
            logging.error(traceback.format_exception(exc_type, exc_val, tb))
        """dir(Channel)
        [..., '_clean_content', '_handle_call', '_handle_mentions',
        '_handle_upgrades', '_raw_channel_mentions', '_raw_mentions', '_raw_role_mentions',
        '_system_content', '_update',
        'attachments', 'author', 'call', 'channel', 'channel_mentions', 'clean_content',
        'content', 'edited_timestamp', 'embeds', 'id', 'mention_everyone', 'mentions',
        'nonce', 'pinned', 'raw_channel_mentions', 'raw_mentions', 'raw_role_mentions', 'reactions',
        'role_mentions', 'server', 'system_content', 'timestamp', 'tts', 'type']
        """
        """dir(PrivateChannel)
        [..., '_update_group',
        'created_at', 'icon', 'icon_url', 'id', 'is_private',
        'me', 'name', 'owner', 'permissions_for', 'recipients', 'type', 'user']
        """


    @client.event
    async def on_message(message: discord.Message):
        main_channel = "bot"
        active_channels = ["dev", "bot", "Direct Message with rokusan63"]
        if client.user != message.author:
            log_message_information(message)
            reply_text = None
            # メッセージを最大１個送る
            if not reply_text and message.channel.is_private or message.channel.name in active_channels:
                reply_text = get_listen_reply(message)
                if reply_text:
                    # メッセージが送られてきたチャンネルへメッセージを送ります
                    logging.debug("replying as listened message")
                    await client.send_message(message.channel, reply_text)
            if not reply_text and any(filter(lambda member: member == client.user, message.mentions)):
                reply_text = get_mention_reply(message)
                if reply_text:    
                    # メッセージが送られてきたチャンネルへメッセージを送ります
                    logging.debug("replying as mention message")
                    await client.send_message(message.channel, reply_text)
    try:
        client.run(conf.discord_apikey)
    finally:
        logging.info("client exit")
        client.close()

def debug_on_console():
    class PseudoMessage:
        def __init__(self):
            self.content = ""
            self.author = None
    class PseudoUser:
        def __init__(self, name):
            self.name = name
    while True:
        message = PseudoMessage()
        message.content = input(">")
        if re.match(r"exit(|\(\))", message.content):
            break
        elif re.match(r"^(@\w+)\s+(.*)$", message.content):
            mt = re.match(r"^(@\w+)\s(.*)$", message.content)
            message.author = PseudoUser(mt.groups()[0])
            message.content = "<@{}> {}".format("test", mt.groups()[1])
            reply_text = get_mention_reply(message)            
        else:
            reply_text = get_listen_reply(message)
        print(reply_text)

LOGFILE_DEFAULT = "/var/log/rokudiscobot.log"

def init_logging(arg):
    logfile = arg.logfile if arg.logfile else LOGFILE_DEFAULT
    loglevel = getattr(logging, arg.loglevel)
    logging.basicConfig(filename=logfile, level=loglevel, format='%(asctime)s[%(levelname)s]:%(message)s')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--console", action="store_true")
    parser.add_argument("--logfile", type=str)
    parser.add_argument("--loglevel", type=str, choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="WARNING")
    arg = parser.parse_args()
    init_logging(arg)
    if arg.console:
        debug_on_console()
    else:
        main()