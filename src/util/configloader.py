from pathlib import Path
from configparser import ConfigParser

def discover():
    """コンフィグファイルの場所を取得、なかった場合は例外を投げる
    """
    root = Path(__file__).parent.parent.parent
    discover_list = [
        root / Path(".discobot.apikeys.conf"),
        root / Path(".discobot/apikeys.conf"),
        root / Path("dat/config/apikeys.conf"),
    ]
    existing = list(filter(Path.is_file, discover_list))
    if not existing:
        raise FileNotFoundError("""no apikeys.conf
        create  .discobot/apikeys.conf or dat/config/apikeys.conf and write apitoken config.
        Here is format.
            [DEFAULT]
            DISCORD_API_TOKEN = <APIKEY>
        """)
    return existing[0]

class Config:
    def __init__(self):
        self.discord_apikey = ''

    @staticmethod
    def load(filepath: Path=None):
        if filepath is None:
            filepath = discover() # 引数がNoneの場合はリストから検索
        config = ConfigParser()
        config.read(str(filepath))
        obj = Config()
        obj.discord_apikey = config["DEFAULT"]["DISCORD_API_TOKEN"]
        return obj   