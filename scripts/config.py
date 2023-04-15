import abc
import os
import openai
import yaml
from dotenv import load_dotenv
load_dotenv()


class Singleton(abc.ABCMeta, type):
    """
    Singleton metaclass for ensuring only one instance of a class.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Call method for the singleton metaclass."""
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(
                *args, **kwargs)
        return cls._instances[cls]


class AbstractSingleton(abc.ABC, metaclass=Singleton):
    pass


class Config(metaclass=Singleton):
    """
    Configuration class to store the state of bools for different scripts access.
    """

    def __init__(self):
        """Initialize the Config class"""
        self.debug_mode = False

        self.fast_llm_model = os.getenv("FAST_LLM_MODEL", "gpt-3.5-turbo")
        self.smart_llm_model = os.getenv("SMART_LLM_MODEL", "gpt-4")
        self.fast_token_limit = int(os.getenv("FAST_TOKEN_LIMIT", 4000))
        self.smart_token_limit = int(os.getenv("SMART_TOKEN_LIMIT", 8000))

        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.temperature = float(os.getenv("TEMPERATURE", "1"))
        self.use_azure = os.getenv("USE_AZURE") == 'True'
        self.execute_local_commands = os.getenv('EXECUTE_LOCAL_COMMANDS', 'False') == 'True'

        if self.use_azure:
            self.load_azure_config()
            openai.api_type = self.openai_api_type
            openai.api_base = self.openai_api_base
            openai.api_version = self.openai_api_version
        openai.api_key = self.openai_api_key

    def get_azure_deployment_id_for_model(self, model: str) -> str:
        """
        Returns the relevant deployment id for the model specified.

        Parameters:
            model(str): The model to map to the deployment id.

        Returns:
            The matching deployment id if found, otherwise an empty string.
        """
        if model == self.fast_llm_model:
            return self.azure_model_to_deployment_id_map["fast_llm_model_deployment_id"]
        elif model == self.smart_llm_model:
            return self.azure_model_to_deployment_id_map["smart_llm_model_deployment_id"]
        elif model == "text-embedding-ada-002":
            return self.azure_model_to_deployment_id_map["embedding_model_deployment_id"]
        else:
            return ""

    AZURE_CONFIG_FILE = os.path.join(os.path.dirname(__file__), '..', 'azure.yaml')

    def load_azure_config(self, config_file: str=AZURE_CONFIG_FILE) -> None:
        """
        Loads the configuration parameters for Azure hosting from the specified file path as a yaml file.

        Parameters:
            config_file(str): The path to the config yaml file. DEFAULT: "../azure.yaml"

        Returns:
            None
        """
        try:
            with open(config_file) as file:
                config_params = yaml.load(file, Loader=yaml.FullLoader)
        except FileNotFoundError:
            config_params = {}
        self.openai_api_type = os.getenv("OPENAI_API_TYPE", config_params.get("azure_api_type", "azure"))
        self.openai_api_base = os.getenv("OPENAI_AZURE_API_BASE", config_params.get("azure_api_base", ""))
        self.openai_api_version = os.getenv("OPENAI_AZURE_API_VERSION", config_params.get("azure_api_version", ""))
        self.azure_model_to_deployment_id_map = config_params.get("azure_model_map", [])

    def set_debug_mode(self, value: bool):
        """Set the debug mode value."""
        self.debug_mode = value