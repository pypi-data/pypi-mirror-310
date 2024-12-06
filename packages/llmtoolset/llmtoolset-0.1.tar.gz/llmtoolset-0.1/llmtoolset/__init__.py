from chatollama import Engine, Conversation

instance = Engine()


def set_model(model_name: str):
    instance.model = model_name
