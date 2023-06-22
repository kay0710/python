import pynecone as pc

class ChatbotConfig(pc.Config):
    pass

config = ChatbotConfig(
    app_name="chatbot",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
    port=3000,
)
