import yaml
from colorama import Fore, Style
import os
from logger import logger
import utils
class AIConfig:
    """
    A class object that contains the configuration information for the AI

    Attributes:
        ai_name (str): The name of the AI.
        ai_role (str): The description of the AI's role.
        ai_goals (list): The list of objectives the AI is supposed to complete.
    """

    def __init__(self, ai_name: str="", ai_role: str="", ai_goals: list=[]) -> None:
        """
        Initialize a class instance

        Parameters:
            ai_name (str): The name of the AI.
            ai_role (str): The description of the AI's role.
            ai_goals (list): The list of objectives the AI is supposed to complete.
        Returns:
            None
        """

        self.ai_name = ai_name
        self.ai_role = ai_role
        self.ai_goals = ai_goals

    # Soon this will go in a folder where it remembers more stuff about the run(s)
    SAVE_FILE = os.path.join(os.path.dirname(__file__), '..', 'ai_settings.yaml')

    @classmethod
    def load(cls: object, config_file: str=SAVE_FILE) -> object:
        """
        Returns class object with parameters (ai_name, ai_role, ai_goals) loaded from yaml file if yaml file exists,
        else returns class with no parameters.

        Parameters:
           cls (class object): An AIConfig Class object.
           config_file (int): The path to the config yaml file. DEFAULT: "../ai_settings.yaml"

        Returns:
            cls (object): An instance of given cls object
        """

        try:
            with open(config_file) as file:
                config_params = yaml.load(file, Loader=yaml.FullLoader)
        except FileNotFoundError:
            config_params = {}

        ai_name = config_params.get("ai_name", "")
        ai_role = config_params.get("ai_role", "")
        ai_goals = config_params.get("ai_goals", [])

        return cls(ai_name, ai_role, ai_goals)

    def save(self, config_file: str=SAVE_FILE) -> None:
        """
        Saves the class parameters to the specified file yaml file path as a yaml file.

        Parameters:
            config_file(str): The path to the config yaml file. DEFAULT: "../ai_settings.yaml"

        Returns:
            None
        """

        config = {"ai_name": self.ai_name, "ai_role": self.ai_role, "ai_goals": self.ai_goals}
        with open(config_file, "w") as file:
            yaml.dump(config, file)

    @classmethod
    def init_from_user(cls):
        """Prompt the user for input"""
        ai_name = ""
        # Construct the prompt
        logger.typewriter_log(
            "Welcome to Auto-GPT! ",
            Fore.GREEN,
            "Enter the name of your AI and its role below. Entering nothing will load defaults.",
            speak_text=True)

        # Get AI Name from User
        logger.typewriter_log(
            "Name your AI: ",
            Fore.GREEN,
            "For example, 'Entrepreneur-GPT'")
        ai_name = utils.clean_input("AI Name: ")
        if ai_name == "":
            ai_name = "Entrepreneur-GPT"

        logger.typewriter_log(
            f"{ai_name} here!",
            Fore.LIGHTBLUE_EX,
            "I am at your service.",
            speak_text=True)

        # Get AI Role from User
        logger.typewriter_log(
            "Describe your AI's role: ",
            Fore.GREEN,
            "For example, 'an AI designed to autonomously develop and run businesses with the sole goal of increasing your net worth.'")
        ai_role = utils.clean_input(f"{ai_name} is: ")
        if ai_role == "":
            ai_role = "an AI designed to autonomously develop and run businesses with the sole goal of increasing your net worth."

        # Enter up to 5 goals for the AI
        logger.typewriter_log(
            "Enter up to 5 goals for your AI: ",
            Fore.GREEN,
            "For example: \nIncrease net worth, Grow Twitter Account, Develop and manage multiple businesses autonomously'")
        print("Enter nothing to load defaults, enter nothing when finished.", flush=True)
        ai_goals = []
        for i in range(5):
            ai_goal = utils.clean_input(f"{Fore.LIGHTBLUE_EX}Goal{Style.RESET_ALL} {i+1}: ")
            if ai_goal == "":
                break
            ai_goals.append(ai_goal)
        if len(ai_goals) == 0:
            ai_goals = ["Increase net worth", "Grow Twitter Account",
                        "Develop and manage multiple businesses autonomously"]

        config = cls(ai_name, ai_role, ai_goals)
        return config

