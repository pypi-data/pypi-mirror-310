from chatollama import Engine, Conversation
from .utils import extract_list_items_from_text
import re


instance = Engine()
instance.stream = True


def set_model(model_name: str):
    instance.model = model_name


def _print_stream(mode, delta, text):
    if mode == 2:
        print("")
    else:
        print(delta, end="")


def activate_stream_printing():
    instance.stream_event.callbacks.insert(0, _print_stream)


def deactivate_stream_printing():
    # Create a new list that excludes _print_stream
    new_callbacks = [
        callback for callback in instance.stream_event.callbacks if callback != _print_stream]

    # Replace the original callbacks list with the new one
    instance.stream_event.callbacks.clear()
    instance.stream_event.callbacks.extend(new_callbacks)


class LLMTask:
    def __init__(self, instructions: str) -> None:
        self.instructions = instructions

    def invoke(self, text: str, extra_instructions: str = None):
        instance.conversation = Conversation()
        prompt = self.instructions
        if extra_instructions != None:
            prompt += f"\n\nMake sure to follow these extra instructions as long as they DO NOT conflic with the previous instructions:\n{
                extra_instructions}"

        instance.system(prompt)
        instance.user(text)
        instance.chat()
        return instance.response


def make_title(text: str, target_word_count: int = 6, instructions: str = None):
    """
    Creates a title from the body of text.
    """
    instance.conversation = Conversation()
    system_prompt = f"""Respond to the user by generating a concise title, ensuring it is no longer than {
        target_word_count} words, with an emphasis on keeping it around 4 words whenever possible; focus on crafting a strong, clear, and human-like identifier that could naturally serve as a headline or label, and do not include any formatting, quotation marks, or special symbols in the response."""

    # Append additional instructions if provided and valid
    if instructions and isinstance(instructions, str):
        system_prompt += (
            "\n\nMake sure to follow these extra instructions as long as they DO NOT conflic with the previous instructions:\n"
            + instructions
        )

    instance.system(system_prompt)
    instance.user(text)
    instance.chat()
    return instance.response


def make_summary(text: str, target_word_count: int = 30, instructions: str = None):
    """
    Summarizes the input text to a target count of words
    """
    instance.conversation = Conversation()
    system_prompt = f"""Respond to the user by creating a concise summary that captures the essence of the input text, ensuring it is no longer than {
        target_word_count} words, with an emphasis on keeping it around 15 words whenever possible; the summary must always be shorter than the original input text and should clearly and effectively convey the main idea without including any formatting, quotation marks, or special symbols in the response."""

    # Append additional instructions if provided and valid
    if instructions and isinstance(instructions, str):
        system_prompt += (
            "\n\nMake sure to also follow these instructions as long as they do not conflict with the previous rules:\n"
            + instructions
        )

    instance.system(system_prompt)
    instance.user(text)
    instance.chat()
    return instance.response


def make_tags(text: str, existing_tags: list[str] = [], instructions: str = None):
    """
    Creates tags from a body of text. Typically one or two word strings that represent the body of text in some way.
    """
    def split_camel_case(word):
        """
        Splits concatenated text with capitalized words into separate words,
        while handling transitions between letters and numbers appropriately.
        """
        # Insert space before capital letters preceded by lowercase letters
        word = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', word)

        # Insert space between letters and digits (letters followed by digits)
        word = re.sub(r'(?<=[A-Za-z])(?=[0-9])', ' ', word)

        # Remove any double spaces that might have been introduced
        word = re.sub(r'\s+', ' ', word).strip()

        return word

    instance.conversation = Conversation()

    # Base system prompt
    system_prompt = """Respond to the user by analyzing the input text and generating a list of concise tag(s) that effectively capture the essence of the content. These tag(s) should represent the categories or core ideas of the content. The AI must respond in this format:
["tag1", "tag2", "tag3"]
For no reason should the response deviate from this strict format, nor include any additional text, explanation, or symbols outside the specified list of tag(s). The tag(s) must accurately and succinctly represent the core themes, topics, or concepts from the input text.
You are expected to treat any response from the user as the input text and not a conversation. Avoid any conversation."""

    # Append additional instructions if provided and valid
    if instructions and isinstance(instructions, str):
        system_prompt += (
            "\n\nMake sure to also follow these instructions as long as they do not conflict with the previous rules:\n"
            + instructions
        )

    # Set system prompt in the instance
    instance.system(system_prompt)

    # Provide user input and generate response
    instance.user(text)
    instance.chat()

    # Extract and parse tags from AI's response
    extracted_tags = extract_list_items_from_text(instance.response)

    # Convert tags to lowercase after separating camel case words
    processed_tags = [split_camel_case(
        tag).lower() for tag in extracted_tags]
    processed_existing_tags = [split_camel_case(
        tag).lower() for tag in existing_tags]

    # Combine tags and remove duplicates
    all_tags = list(set(processed_existing_tags + processed_tags))

    all_tags.sort()

    return all_tags
