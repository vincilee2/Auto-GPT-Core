import argparse
from logger import logger
import logging
from config import Config
from colorama import Fore, Style
from ai_config import AIConfig
import prompts
from spinner import Spinner
import commands as cmd
cfg = Config()
import utils


def parse_arguments():
    """Parses the arguments passed to the script"""
    global cfg
    cfg.set_debug_mode(False)

    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--continuous', action='store_true', help='Enable Continuous Mode')
    parser.add_argument('--debug', action='store_true', help='Enable Debug Mode')
    parser.add_argument('--gpt3only', action='store_true', help='Enable GPT3.5 Only Mode')
    args = parser.parse_args()

    if args.debug:
        logger.typewriter_log("Debug Mode: ", Fore.GREEN, "ENABLED")
        cfg.set_debug_mode(True)

parse_arguments()
logger.set_level(logging.DEBUG if cfg.debug_mode else logging.INFO)

# print(prompt)
# Initialize variables
full_message_history = []
result = None
next_action_count = 0
# Make a constant:
user_input = "Determine which next command to use, and respond using the format specified above:"

config = AIConfig.load()
prompt, config = prompts.construct_prompt(config)


#logger.typewriter_log( "Full Prompts: ", Fore.GREEN, f"{prompt}")

def print_assistant_thoughts(assistant_reply):
        thoughts = assistant_reply["thoughts"]
        logger.typewriter_log(f"{config.ai_name} THOUGHTS:", Fore.YELLOW, thoughts['text'])
        logger.typewriter_log(f"{config.ai_name} REASONING:", Fore.YELLOW, thoughts['reasoning'])
        logger.typewriter_log("PLAN:", Fore.YELLOW, "")
        lines = thoughts['plan'].split('\n')
        for line in lines:
            line = line.lstrip("- ")
            logger.typewriter_log("- ", Fore.GREEN, line.strip())
        logger.typewriter_log("CRITICISM:", Fore.YELLOW, thoughts['criticism'])

while True:
    with Spinner("Thinking... "):
        assistant_reply = { 
            "thoughts": {
                "text": "I need to start by recruiting more members to work with me.",
                "reasoning": "I need to get more people on my team to help build my product",
                "plan": "- Use Google Search to find resumes and job posting sites\n- Save the URLs for later use",
                "criticism": "I may spend too much time browsing without focusing on the best candidates",
                "speak": "I will use Google Search to find resumes and job postings, save the URLs for later, and make sure I'm not repeating searches"
            },
            "command": {
                "name": "google",
                "args":{
                    "input": "resume posting sites"
                }
            }
        }
    logger.typewriter_log("REPLY FROM GPT:", Fore.GREEN, f"{assistant_reply}")
    print_assistant_thoughts(assistant_reply)
    command_name, arguments = cmd.get_command(assistant_reply)
    
    user_input = ""
    logger.typewriter_log(
        "NEXT ACTION: ",
        Fore.CYAN,
        f"COMMAND = {Fore.CYAN}{command_name}{Style.RESET_ALL}  ARGUMENTS = {Fore.CYAN}{arguments}{Style.RESET_ALL}")
    print(
        f"Enter 'y' to authorise command, 'y -N' to run N continuous commands, 'n' to exit program, or enter feedback for {config.ai_name}...",
        flush=True)
    
    while True:
        console_input = utils.clean_input(Fore.MAGENTA + "Input:" + Style.RESET_ALL)
        if console_input.lower().rstrip() == "y":
            user_input = "GENERATE NEXT COMMAND JSON"
            logger.typewriter_log(
            "-=-=-=-=-=-=-= COMMAND AUTHORISED BY USER -=-=-=-=-=-=-=",
            Fore.MAGENTA,
            "")
            break
        elif console_input.lower() == "n":
            user_input = "EXIT"
            break
        else:
            user_input = console_input
            command_name = "human_feedback"
            break

    if command_name == "human_feedback":
        result = f"Human feedback: {user_input}"
    else:
        result = f"Command {command_name} returned: {cmd.execute_command(command_name, arguments)}"
    
    memory_to_add = f"Assistant Reply: {assistant_reply} " \
        f"\nResult: {result} " \
        f"\nHuman Feedback: {user_input} "
    
    if result is not None:
        #full_message_history.append(chat.create_chat_message("system", result))
        logger.typewriter_log("SYSTEM: ", Fore.YELLOW, result)
    
    logger.typewriter_log("ADD TO MEMORY:", Fore.GREEN, f"{memory_to_add}")
    break


