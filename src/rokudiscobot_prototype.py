from util.configloader import Config
import discord

def main():
    conf = Config.load()
    client = discord.Client()

    @client.event
    async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')
    
    @client.event
    async def on_message(message: discord.Message):
        if client.user != message.author and message.is_private:
            # 「おはよう」で始まるか調べる
            if message.content.startswith("おはよう") or message.content.startswith("Hi") or message.content.startswith("Hello"):
                # 送り主がBotだった場合反応したくないので
                    # メッセージを書きます
                    m = "おはようございます" + message.author.name + "さん！"
                    # メッセージが送られてきたチャンネルへメッセージを送ります
                    await client.send_message(message.channel, m)
            elif "yo" in message.content.lower():
                m = "yo"
                # メッセージが送られてきたチャンネルへメッセージを送ります
                await client.send_message(message.channel, m)
            else:
                m = "わかる"
                # メッセージが送られてきたチャンネルへメッセージを送ります
                await client.send_message(message.channel, m)
                
        
    client.run(conf.discord_apikey)

if __name__ == "__main__":
    main()