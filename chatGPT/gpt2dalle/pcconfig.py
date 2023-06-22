import pynecone as pc

class GptdalleConfig(pc.Config):
    pass

config = GptdalleConfig(
    app_name="gpt2dalle",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)