from logger import logger
from colorama import Fore, Style
from ai_config import AIConfig
from pathlib import Path
import utils

def load_prompt():
    """Load the prompt from prompts/v1.txt"""
    try:
        # get directory of this file:
        file_dir = Path(__file__).parent
        prompt_file_path = file_dir / "prompts" / "v1.txt"

        # Load the prompt from data/prompt.txt
        with open(prompt_file_path, "r") as prompt_file:
            prompt = prompt_file.read()

        return prompt
    except FileNotFoundError:
        print("Error: Prompt file not found", flush=True)
        return ""

def construct_prompt(config):
    """Construct the prompt for the AI to respond to"""
    if config.ai_name:
        logger.typewriter_log(
            f"Welcome back! ",
            Fore.GREEN,
            f"Would you like me to return to being {config.ai_name}?",
            speak_text=True)
        should_continue = utils.clean_input(f"""Continue with the last settings?
Name:  {config.ai_name}
Role:  {config.ai_role}
Goals: {config.ai_goals}
Continue (y/n): """)
        if should_continue.lower() == "n":
            config = AIConfig()

    if not config.ai_name:
        config = AIConfig.init_from_user()
        config.save()

    # Get rid of this global:
    global ai_name
    ai_name = config.ai_name

    full_prompt = construct_full_prompt(config)
    return full_prompt, config


def construct_full_prompt(config) -> str:
    """
    Returns a prompt to the user with the class information in an organized fashion.

    Parameters:
        None

    Returns:
        full_prompt (str): A string containing the initial prompt for the user including the ai_name, ai_role and ai_goals.
    """

    prompt_start = """Your decisions must always be made independently without seeking user assistance. Play to your strengths as an LLM and pursue simple strategies with no legal complications."""

    # Construct full prompt
    full_prompt = f"You are {config.ai_name}, {config.ai_role}\n{prompt_start}\n\nGOALS:\n\n"
    for i, goal in enumerate(config.ai_goals):
        full_prompt += f"{i+1}. {goal}\n"

    full_prompt += f"\n\n{load_prompt()}"
    return full_prompt