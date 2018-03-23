from util.configloader import Config
import discord
import re
import sys

def main():
    conf = Config.load()
    client = discord.Client()

    @client.event
    async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')
    import traceback

    def log_message_information(message: discord.Message):
        try:
            print(message.channel.name)
            print(message.channel.is_private)
            if message.channel.is_private:
                print(message.channel.owner)
                print(message.channel.recipients)
            else:
                print(dir(message))
            print(message.channel_mentions)
            print(message.mentions)
            print(message.mention_everyone)
        except:
            exc_type, exc_val, tb = sys.exc_info()
            traceback.print_exception(exc_type, exc_val, tb)
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

    def get_listen_reply(message: discord.Message):
        """メンションなしの場合のリアクション
        """
        if re.match(r"^(おはよう|よお|よう|Hello|はろー)", message.content):
            return "おはようございます" + message.author.name + "さん！"
        elif re.match(r"^わかり手だ", message.content):
            return "そうだよ"
        elif re.match(r"^わかる", message.content):
            return "わかり手だ"
        elif "yo" in message.content.lower():
            return "yo"
        return None

    def get_mention_reply(message: discord.Message):
        """メンションに対するリアクション
        """
        if re.match(r"^(おはよう|よお|よう|Hello|はろー)", message.content):
            return "おはようございます" + message.author.name + "さん！"
        elif re.match(r"^わかり手だ", message.content):
            return "そうだよ"
        elif re.match(r"^わかる", message.content):
            return "わかり手だ"
        elif "yo" in message.content.lower():
            return "yo"
        return "わかる"


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
                    await client.send_message(message.channel, reply_text)
            if not reply_text and filter(lambda member: member == client.user, message.mentions):
                reply_text = get_mention_reply(message)
                if reply_text:    
                    # メッセージが送られてきたチャンネルへメッセージを送ります
                    await client.send_message(message.channel, reply_text)
    try:
        client.run(conf.discord_apikey)
    finally:
        print("client exit")
        client.close()

if __name__ == "__main__":
    main()