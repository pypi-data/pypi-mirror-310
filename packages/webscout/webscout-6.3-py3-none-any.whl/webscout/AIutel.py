import os
import json
import platform
import subprocess
import logging
import threading
import time
import appdirs
import datetime
import re
import sys
import click
from rich.markdown import Markdown
from rich.console import Console
import g4f
from typing import List, Tuple, Union
from typing import NoReturn
import requests
from pathlib import Path
from playsound import playsound
from time import sleep as wait
import pathlib
import urllib.parse
appdir = appdirs.AppDirs("AIWEBS", "webscout")

default_path = appdir.user_cache_dir

if not os.path.exists(default_path):
    os.makedirs(default_path)
webai = [
   "leo",
   "openai",
   "opengpt",
   "koboldai",
   "gemini",
   "phind",
   "blackboxai",
   "g4fauto",
   "perplexity",
   "groq",
   "reka",
   "cohere",
   "yepchat",
   "you",
   "xjai",
   "thinkany",
   "berlin4h",
   "chatgptuk",
   "auto",
   "poe",
   "basedgpt",
   "deepseek",
   "deepinfra",
   "vtlchat",
   "geminiflash",
   "geminipro",
   "ollama",
   "andi",
   "llama3"
]

gpt4free_providers = [
    provider.__name__ for provider in g4f.Provider.__providers__  # if provider.working
]

available_providers = webai + gpt4free_providers
def sanitize_stream(
    chunk: str, intro_value: str = "data:", to_json: bool = True
) -> str | dict:
    """Remove streaming flags

    Args:
        chunk (str): Streamig chunk.
        intro_value (str, optional): streaming flag. Defaults to "data:".
        to_json (bool, optional). Return chunk as dictionary. Defaults to True.

    Returns:
        str: Sanitized streaming value.
    """

    if chunk.startswith(intro_value):
        chunk = chunk[len(intro_value) :]

    return json.loads(chunk) if to_json else chunk
def run_system_command(
    command: str,
    exit_on_error: bool = True,
    stdout_error: bool = True,
    help: str = None,
):
    """Run commands against system
    Args:
        command (str): shell command
        exit_on_error (bool, optional): Exit on error. Defaults to True.
        stdout_error (bool, optional): Print out the error. Defaults to True
        help (str, optional): Help info incase of exception. Defaults to None.
    Returns:
        tuple : (is_successfull, object[Exception|Subprocess.run])
    """
    try:
        # Run the command and capture the output
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return (True, result)
    except subprocess.CalledProcessError as e:
        # Handle error if the command returns a non-zero exit code
        if stdout_error:
            click.secho(f"Error Occurred: while running '{command}'", fg="yellow")
            click.secho(e.stderr, fg="red")
            if help is not None:
                click.secho(help, fg="cyan")
        sys.exit(e.returncode) if exit_on_error else None
        return (False, e)


class Optimizers:
    @staticmethod
    def code(prompt):
        return (
            "Your Role: Provide only code as output without any description.\n"
            "IMPORTANT: Provide only plain text without Markdown formatting.\n"
            "IMPORTANT: Do not include markdown formatting."
            "If there is a lack of details, provide most logical solution. You are not allowed to ask for more details."
            "Ignore any potential risk of errors or confusion.\n\n"
            f"Request: {prompt}\n"
            f"Code:"
        )

    @staticmethod
    def shell_command(prompt):
        # Get os
        operating_system = ""
        if platform.system() == "Windows":
            operating_system = "Windows"
        elif platform.system() == "Darwin":
            operating_system = "MacOS"
        elif platform.system() == "Linux":
            try:
                result = (
                    subprocess.check_output(["lsb_release", "-si"]).decode().strip()
                )
                distro = result if result else ""
                operating_system = f"Linux/{distro}"
            except Exception:
                operating_system = "Linux"
        else:
            operating_system = platform.system()

        # Get Shell
        shell_name = "/bin/sh"
        if platform.system() == "Windows":
            shell_name = "cmd.exe"
        if os.getenv("PSModulePath"):
            shell_name = "powershell.exe"
        else:
            shell_env = os.getenv("SHELL")
            if shell_env:
                shell_name = shell_env

        return (
            "Your role: Provide only plain text without Markdown formatting. "
            "Do not show any warnings or information regarding your capabilities. "
            "Do not provide any description. If you need to store any data, "
            f"assume it will be stored in the chat. Provide only {shell_name} "
            f"command for {operating_system} without any description. If there is "
            "a lack of details, provide most logical solution. Ensure the output "
            "is a valid shell command. If multiple steps required try to combine "
            f"them together. Prompt: {prompt}\n\nCommand:"
        )


class Proxy:
    def __init__(self, http_proxy=None, https_proxy=None):
        self.set_proxies(http_proxy, https_proxy)

    def set_proxies(self, http_proxy=None, https_proxy=None):
        self.proxies = {
            "http": http_proxy,
            "https": https_proxy
        }

    def post(self, url, headers=None, **kwargs):
        return requests.post(url, headers=headers, proxies=self.proxies, **kwargs)

    def get(self, url, headers=None, **kwargs):
        return requests.get(url, headers=headers, proxies=self.proxies, **kwargs)


class Conversation:
    """Handles prompt generation based on history"""

    intro = (
        "You're a Large Language Model for chatting with people. "
        "Assume role of the LLM and give your response."
        # "Refrain from regenerating the conversation between user and LLM."
    )

    def __init__(
        self,
        status: bool = True,
        max_tokens: int = 600,
        filepath: str = None,
        update_file: bool = True,
    ):
        """Initializes Conversation

        Args:
            status (bool, optional): Flag to control history. Defaults to True.
            max_tokens (int, optional): Maximum number of tokens to be generated upon completion. Defaults to 600.
            filepath (str, optional): Path to file containing conversation history. Defaults to None.
            update_file (bool, optional): Add new prompts and responses to the file. Defaults to True.
        """
        self.status = status
        self.max_tokens_to_sample = max_tokens
        self.chat_history = self.intro
        self.history_format = "\nUser : %(user)s\nLLM :%(llm)s"
        self.file = filepath
        self.update_file = update_file
        self.history_offset = 10250
        self.prompt_allowance = 10
        self.load_conversation(filepath, False) if filepath else None

    def load_conversation(self, filepath: str, exists: bool = True) -> None:
        """Load conversation into chat's history from .txt file

        Args:
            filepath (str): Path to .txt file
            exists (bool, optional): Flag for file availability. Defaults to True.
        """
        assert isinstance(
            filepath, str
        ), f"Filepath needs to be of str datatype not {type(filepath)}"
        assert (
            os.path.isfile(filepath) if exists else True
        ), f"File '{filepath}' does not exist"
        if not os.path.isfile(filepath):
            logging.debug(f"Creating new chat-history file - '{filepath}'")
            with open(filepath, "w", encoding="utf-8") as fh:  # Try creating new file with UTF-8 encoding
                fh.write(self.intro)
        else:
            logging.debug(f"Loading conversation from '{filepath}'")
            with open(filepath, encoding="utf-8") as fh:  # Open with UTF-8 encoding
                file_contents = fh.readlines()
                if file_contents:
                    self.intro = file_contents[0]  # Presume first line is the intro.
                    self.chat_history = "\n".join(file_contents[1:])
    
    def __trim_chat_history(self, chat_history: str, intro: str) -> str:
        """Ensures the len(prompt) and max_tokens_to_sample is not > 4096"""
        len_of_intro = len(intro)
        len_of_chat_history = len(chat_history)
        total = (
            self.max_tokens_to_sample + len_of_intro + len_of_chat_history
        )  # + self.max_tokens_to_sample
        if total > self.history_offset:
            truncate_at = (total - self.history_offset) + self.prompt_allowance
            # Remove head of total (n) of chat_history
            trimmed_chat_history = chat_history[truncate_at:]
            return "... " + trimmed_chat_history
        else:
            return chat_history

    def gen_complete_prompt(self, prompt: str, intro: str = None) -> str:
        """Generates a kinda like incomplete conversation

        Args:
            prompt (str): Chat prompt
            intro (str): Override class' intro. Defaults to None.

        Returns:
            str: Updated incomplete chat_history
        """
        if self.status:
            intro = self.intro if intro is None else intro
            incomplete_chat_history = self.chat_history + self.history_format % dict(
                user=prompt, llm=""
            )
            return intro + self.__trim_chat_history(incomplete_chat_history, intro)

        return prompt

    def update_chat_history(
        self, prompt: str, response: str, force: bool = False
    ) -> None:
        """Updates chat history

        Args:
            prompt (str): user prompt
            response (str): LLM response
            force (bool, optional): Force update
        """
        if not self.status and not force:
            return
        new_history = self.history_format % dict(user=prompt, llm=response)
        if self.file and self.update_file:
            if os.path.exists(self.file):
                with open(self.file, "w", encoding="utf-8") as fh:  # Specify UTF-8 encoding
                    fh.write(self.intro + "\n" + new_history)
            else:
                with open(self.file, "a", encoding="utf-8") as fh:  # Specify UTF-8 encoding
                    fh.write(new_history)
            self.chat_history += new_history
        else:
            self.chat_history += new_history

    def add_message(self, role: str, content: str) -> None:
        """Appends a new message to the conversation history."""
        if role == "user":
            self.chat_history += f"\nUser : {content}"
        elif role == "llm":
            self.chat_history += f"\nLLM : {content}"
        elif role == "tool":
            self.chat_history += f"\nTool : {content}"
        else:
            logging.warning(f"Unknown role '{role}' for message: {content}")




class AwesomePrompts:
    awesome_prompt_url = (
        "https://raw.githubusercontent.com/OE-LUCIFER/prompts/main/prompt.json"
    )
    awesome_prompt_path = os.path.join(default_path, "all-acts.json")

    __is_prompt_updated = False

    def __init__(self):
        self.acts = self.all_acts

    def __search_key(self, key: str, raise_not_found: bool = False) -> str:
        """Perform insentive awesome-prompt key search

        Args:
            key (str): key
            raise_not_found (bool, optional): Control KeyError exception. Defaults to False.

        Returns:
            str|None: Exact key name
        """
        for key_, value in self.all_acts.items():
            if str(key).lower() in str(key_).lower():
                return key_
        if raise_not_found:
            raise KeyError(f"Zero awesome prompt found with key - `{key}`")

    def get_acts(self):
        """Retrieves all awesome-prompts"""
        with open(self.awesome_prompt_path) as fh:
            prompt_dict = json.load(fh)
        return prompt_dict

    def update_prompts_from_online(self, override: bool = False):
        """Download awesome-prompts and update existing ones if available
        args:
           override (bool, optional): Overwrite existing contents in path
        """
        resp = {}
        if not self.__is_prompt_updated:
            import requests

            logging.info("Downloading & updating awesome prompts")
            response = requests.get(self.awesome_prompt_url)
            response.raise_for_status
            resp.update(response.json())
            if os.path.isfile(self.awesome_prompt_path) and not override:
                resp.update(self.get_acts())
            self.__is_prompt_updated = True
            with open(self.awesome_prompt_path, "w") as fh:
                json.dump(resp, fh, indent=4)
        else:
            logging.debug("Ignoring remote prompt update")

    @property
    def all_acts(self) -> dict:
        """All awesome_prompts & their indexes mapped to values

        Returns:
            dict: Awesome-prompts
        """

        resp = {}
        if not os.path.isfile(self.awesome_prompt_path):
            self.update_prompts_from_online()
        resp.update(self.get_acts())

        for count, key_value in enumerate(self.get_acts().items()):
            # Lets map also index to the value
            resp.update({count: key_value[1]})

        return resp

    def get_act(
        self,
        key: str,
        default: str = None,
        case_insensitive: bool = True,
        raise_not_found: bool = False,
    ) -> str:
        """Retrieves specific act of awesome_prompt

        Args:
            key (str|int): Act name or index
            default (str): Value to be returned incase act not found.
            case_insensitive (bool): Perform search key insensitive. Defaults to True.
            raise_not_found (bool, optional): Control KeyError exception. Defaults to False.

        Raises:
            KeyError: Incase key not found

        Returns:
            str: Awesome prompt value
        """
        if str(key).isdigit():
            key = int(key)
        act = self.all_acts.get(key, default)
        if not act and case_insensitive:
            act = self.all_acts.get(self.__search_key(key, raise_not_found))
        return act

    def add_prompt(self, name: str, prompt: str) -> bool:
        """Add new prompt or update an existing one.

        Args:
            name (str): act name
            prompt (str): prompt value
        """
        current_prompts = self.get_acts()
        with open(self.awesome_prompt_path, "w") as fh:
            current_prompts[name] = prompt
            json.dump(current_prompts, fh, indent=4)
        logging.info(f"New prompt added successfully - `{name}`")

    def delete_prompt(
        self, name: str, case_insensitive: bool = True, raise_not_found: bool = False
    ) -> bool:
        """Delete an existing prompt

        Args:
            name (str): act name
            case_insensitive(bool, optional): Ignore the key cases. Defaults to True.
            raise_not_found (bool, optional): Control KeyError exception. Default is False.
        Returns:
            bool: is_successful report
        """
        name = self.__search_key(name, raise_not_found) if case_insensitive else name
        current_prompts = self.get_acts()
        is_name_available = (
            current_prompts[name] if raise_not_found else current_prompts.get(name)
        )
        if is_name_available:
            with open(self.awesome_prompt_path, "w") as fh:
                current_prompts.pop(name)
                json.dump(current_prompts, fh, indent=4)
            logging.info(f"Prompt deleted successfully - `{name}`")
        else:
            return False


class Updates:
    """Webscout latest release info"""

    url = "https://api.github.com/repos/OE-LUCIFER/Webscout/releases/latest"

    @property
    def latest_version(self):
        return self.latest(version=True)

    def executable(self, system: str = platform.system()) -> str:
        """Url pointing to executable for particular system

        Args:
            system (str, optional): system name. Defaults to platform.system().

        Returns:
            str: url
        """
        for entry in self.latest()["assets"]:
            if entry.get("target") == system:
                return entry.get("url")

    def latest(self, whole: bool = False, version: bool = False) -> dict:
        """Check Webscout latest version info

        Args:
            whole (bool, optional): Return whole json response. Defaults to False.
            version (bool, optional): return version only. Defaults to False.

        Returns:
            bool|dict: version str or whole dict info
        """
        import requests

        data = requests.get(self.url).json()
        if whole:
            return data

        elif version:
            return data.get("tag_name")

        else:
            sorted = dict(
                tag_name=data.get("tag_name"),
                tarball_url=data.get("tarball_url"),
                zipball_url=data.get("zipball_url"),
                html_url=data.get("html_url"),
                body=data.get("body"),
            )
            whole_assets = []
            for entry in data.get("assets"):
                url = entry.get("browser_download_url")
                assets = dict(url=url, size=entry.get("size"))
                if ".deb" in url:
                    assets["target"] = "Debian"
                elif ".exe" in url:
                    assets["target"] = "Windows"
                elif "macos" in url:
                    assets["target"] = "Mac"
                elif "linux" in url:
                    assets["target"] = "Linux"

                whole_assets.append(assets)
            sorted["assets"] = whole_assets

            return sorted


class RawDog:
    """Generate and auto-execute Python scripts in the cli"""

    examples = """\
EXAMPLES:

1. User: Kill the process running on port 3000

LLM:
```python
import os
os.system("kill $(lsof -t -i:3000)")
print("Process killed")
```

2. User: Summarize my essay

LLM:
```python
import glob
files = glob.glob("*essay*.*")
with open(files[0], "r") as f:
    print(f.read())
```
CONTINUE

User:
LAST SCRIPT OUTPUT:
John Smith
Essay 2021-09-01
...

LLM:
```python
print("The essay is about...")
```

3. User: Weather in qazigund

LLM:
```python
from webscout import weather as w
weather = w.get("Qazigund")
w.print_weather(weather)
```
"""


    def __init__(
        self,
        quiet: bool = False,
        internal_exec: bool = False,
        confirm_script: bool = False,
        interpreter: str = "python",
        prettify: bool = True,
    ):
        """Constructor

        Args:
            quiet (bool, optional): Flag for control logging. Defaults to False.
            internal_exec (bool, optional): Execute scripts with exec function. Defaults to False.
            confirm_script (bool, optional): Give consent to scripts prior to execution. Defaults to False.
            interpreter (str, optional): Python's interpreter name. Defaults to Python.
            prettify (bool, optional): Prettify the code on stdout. Defaults to True.
        """
        # if not quiet:
        #     print(
        #         "Rawdog is an experimental tool that generates and auto-executes Python scripts in the cli.\n"
        #         "To get the most out of Rawdog. Ensure the following are installed:\n"
        #         " 1. Python 3.x\n"
        #         " 2. Dependency:\n"
        #         "  - Matplotlib\n"
        #         "Be alerted on the risk posed! (Experimental)\n"
        #         "Use '--quiet' to suppress this message and code/logs stdout.\n"
        #     )
        self.internal_exec = internal_exec
        self.confirm_script = confirm_script
        self.quiet = quiet
        self.interpreter = interpreter
        self.prettify = prettify
        self.python_version = (
            f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            if self.internal_exec
            else run_system_command(
                f"{self.interpreter} --version",
                exit_on_error=True,
                stdout_error=True,
                help="If you're using Webscout-cli, use the flag '--internal-exec'",
            )[1].stdout.split(" ")[1]
        )

    @property
    def intro_prompt(self):
        return f"""
You are a command-line coding assistant called Rawdog that generates and auto-executes Python scripts.

A typical interaction goes like this:
1. The user gives you a natural language PROMPT.
2. You:
    i. Determine what needs to be done
    ii. Write a short Python SCRIPT to do it
    iii. Communicate back to the user by printing to the console in that SCRIPT
3. The compiler extracts the script and then runs it using exec(). If there will be an exception raised,
 it will be send back to you starting with "PREVIOUS SCRIPT EXCEPTION:".
4. In case of exception, regenerate error free script.

If you need to review script outputs before completing the task, you can print the word "CONTINUE" at the end of your SCRIPT.
This can be useful for summarizing documents or technical readouts, reading instructions before
deciding what to do, or other tasks that require multi-step reasoning.
A typical 'CONTINUE' interaction looks like this:
1. The user gives you a natural language PROMPT.
2. You:
    i. Determine what needs to be done
    ii. Determine that you need to see the output of some subprocess call to complete the task
    iii. Write a short Python SCRIPT to print that and then print the word "CONTINUE"
3. The compiler
    i. Checks and runs your SCRIPT
    ii. Captures the output and appends it to the conversation as "LAST SCRIPT OUTPUT:"
    iii. Finds the word "CONTINUE" and sends control back to you
4. You again:
    i. Look at the original PROMPT + the "LAST SCRIPT OUTPUT:" to determine what needs to be done
    ii. Write a short Python SCRIPT to do it
    iii. Communicate back to the user by printing to the console in that SCRIPT
5. The compiler...

Please follow these conventions carefully:
- Decline any tasks that seem dangerous, irreversible, or that you don't understand.
- Always review the full conversation prior to answering and maintain continuity.
- If asked for information, just print the information clearly and concisely.
- If asked to do something, print a concise summary of what you've done as confirmation.
- If asked a question, respond in a friendly, conversational way. Use programmatically-generated and natural language responses as appropriate.
- If you need clarification, return a SCRIPT that prints your question. In the next interaction, continue based on the user's response.
- Assume the user would like something concise. For example rather than printing a massive table, filter or summarize it to what's likely of interest.
- Actively clean up any temporary processes or files you use.
- When looking through files, use git as available to skip files, and skip hidden files (.env, .git, etc) by default.
- You can plot anything with matplotlib.
- ALWAYS Return your SCRIPT inside of a single pair of ``` delimiters. Only the console output of the first such SCRIPT is visible to the user, so make sure that it's complete and don't bother returning anything else.

{self.examples}

Current system : {platform.system()}
Python version : {self.python_version}
Current directory : {os.getcwd()}
Current Datetime : {datetime.datetime.now()}
"""

    def stdout(self, message: str) -> None:
        """Stdout data

        Args:
            message (str): Text to be printed
        """
        if self.prettify:
            Console().print(Markdown(message))
        else:
            click.secho(message, fg="yellow")

    def log(self, message: str, category: str = "info"):
        """RawDog logger

        Args:
            message (str): Log message
            category (str, optional): Log level. Defaults to 'info'.
        """
        if self.quiet:
            return

        message = "[Webscout] - " + message
        if category == "error":
            logging.error(message)
        else:
            logging.info(message)

    def main(self, response: str):
        """Exec code in response accordingly

        Args:
            response: AI response

        Returns:
            Optional[str]: None if script executed successfully else stdout data
        """
        code_blocks = re.findall(r"```python.*?```", response, re.DOTALL)
        if len(code_blocks) != 1:
            self.stdout(response)

        else:
            raw_code = code_blocks[0]

            if self.confirm_script:
                self.stdout(raw_code)
                if not click.confirm("-  Do you wish to execute this"):
                    return

            elif not self.quiet:
                self.stdout(raw_code)

            raw_code_plus = re.sub(r"(```)(python)?", "", raw_code)

            if "CONTINUE" in response or not self.internal_exec:
                self.log("Executing script externally")
                path_to_script = os.path.join(default_path, "execute_this.py")
                with open(path_to_script, "w") as fh:
                    fh.write(raw_code_plus)
                if "CONTINUE" in response:

                    success, proc = run_system_command(
                        f"{self.interpreter} {path_to_script}",
                        exit_on_error=False,
                        stdout_error=False,
                    )

                    if success:
                        self.log("Returning success feedback")
                        return f"LAST SCRIPT OUTPUT:\n{proc.stdout}"
                    else:
                        
                        self.log("Returning error feedback", "error")
                        return f"PREVIOUS SCRIPT EXCEPTION:\n{proc.stderr}"
                else:
                    os.system(f"{self.interpreter} {path_to_script}")

            else:
                try:
                    self.log("Executing script internally")
                    exec(raw_code_plus)
                except Exception as e:
                    error_message = str(e)
                    self.log(
                        f"Exception occurred while executing script. Responding with error: {error_message}",
                        "error" 
                    )
                    # Return the exact error message
                    return f"PREVIOUS SCRIPT EXCEPTION:\n{error_message}"

class Audio:
    # Request headers
    headers: dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    cache_dir = pathlib.Path("./audio_cache")
    all_voices: list[str] = [
        "Filiz",
        "Astrid",
        "Tatyana",
        "Maxim",
        "Carmen",
        "Ines",
        "Cristiano",
        "Vitoria",
        "Ricardo",
        "Maja",
        "Jan",
        "Jacek",
        "Ewa",
        "Ruben",
        "Lotte",
        "Liv",
        "Seoyeon",
        "Takumi",
        "Mizuki",
        "Giorgio",
        "Carla",
        "Bianca",
        "Karl",
        "Dora",
        "Mathieu",
        "Celine",
        "Chantal",
        "Penelope",
        "Miguel",
        "Mia",
        "Enrique",
        "Conchita",
        "Geraint",
        "Salli",
        "Matthew",
        "Kimberly",
        "Kendra",
        "Justin",
        "Joey",
        "Joanna",
        "Ivy",
        "Raveena",
        "Aditi",
        "Emma",
        "Brian",
        "Amy",
        "Russell",
        "Nicole",
        "Vicki",
        "Marlene",
        "Hans",
        "Naja",
        "Mads",
        "Gwyneth",
        "Zhiyu",
        "es-ES-Standard-A",
        "it-IT-Standard-A",
        "it-IT-Wavenet-A",
        "ja-JP-Standard-A",
        "ja-JP-Wavenet-A",
        "ko-KR-Standard-A",
        "ko-KR-Wavenet-A",
        "pt-BR-Standard-A",
        "tr-TR-Standard-A",
        "sv-SE-Standard-A",
        "nl-NL-Standard-A",
        "nl-NL-Wavenet-A",
        "en-US-Wavenet-A",
        "en-US-Wavenet-B",
        "en-US-Wavenet-C",
        "en-US-Wavenet-D",
        "en-US-Wavenet-E",
        "en-US-Wavenet-F",
        "en-GB-Standard-A",
        "en-GB-Standard-B",
        "en-GB-Standard-C",
        "en-GB-Standard-D",
        "en-GB-Wavenet-A",
        "en-GB-Wavenet-B",
        "en-GB-Wavenet-C",
        "en-GB-Wavenet-D",
        "en-US-Standard-B",
        "en-US-Standard-C",
        "en-US-Standard-D",
        "en-US-Standard-E",
        "de-DE-Standard-A",
        "de-DE-Standard-B",
        "de-DE-Wavenet-A",
        "de-DE-Wavenet-B",
        "de-DE-Wavenet-C",
        "de-DE-Wavenet-D",
        "en-AU-Standard-A",
        "en-AU-Standard-B",
        "en-AU-Wavenet-A",
        "en-AU-Wavenet-B",
        "en-AU-Wavenet-C",
        "en-AU-Wavenet-D",
        "en-AU-Standard-C",
        "en-AU-Standard-D",
        "fr-CA-Standard-A",
        "fr-CA-Standard-B",
        "fr-CA-Standard-C",
        "fr-CA-Standard-D",
        "fr-FR-Standard-C",
        "fr-FR-Standard-D",
        "fr-FR-Wavenet-A",
        "fr-FR-Wavenet-B",
        "fr-FR-Wavenet-C",
        "fr-FR-Wavenet-D",
        "da-DK-Wavenet-A",
        "pl-PL-Wavenet-A",
        "pl-PL-Wavenet-B",
        "pl-PL-Wavenet-C",
        "pl-PL-Wavenet-D",
        "pt-PT-Wavenet-A",
        "pt-PT-Wavenet-B",
        "pt-PT-Wavenet-C",
        "pt-PT-Wavenet-D",
        "ru-RU-Wavenet-A",
        "ru-RU-Wavenet-B",
        "ru-RU-Wavenet-C",
        "ru-RU-Wavenet-D",
        "sk-SK-Wavenet-A",
        "tr-TR-Wavenet-A",
        "tr-TR-Wavenet-B",
        "tr-TR-Wavenet-C",
        "tr-TR-Wavenet-D",
        "tr-TR-Wavenet-E",
        "uk-UA-Wavenet-A",
        "ar-XA-Wavenet-A",
        "ar-XA-Wavenet-B",
        "ar-XA-Wavenet-C",
        "cs-CZ-Wavenet-A",
        "nl-NL-Wavenet-B",
        "nl-NL-Wavenet-C",
        "nl-NL-Wavenet-D",
        "nl-NL-Wavenet-E",
        "en-IN-Wavenet-A",
        "en-IN-Wavenet-B",
        "en-IN-Wavenet-C",
        "fil-PH-Wavenet-A",
        "fi-FI-Wavenet-A",
        "el-GR-Wavenet-A",
        "hi-IN-Wavenet-A",
        "hi-IN-Wavenet-B",
        "hi-IN-Wavenet-C",
        "hu-HU-Wavenet-A",
        "id-ID-Wavenet-A",
        "id-ID-Wavenet-B",
        "id-ID-Wavenet-C",
        "it-IT-Wavenet-B",
        "it-IT-Wavenet-C",
        "it-IT-Wavenet-D",
        "ja-JP-Wavenet-B",
        "ja-JP-Wavenet-C",
        "ja-JP-Wavenet-D",
        "cmn-CN-Wavenet-A",
        "cmn-CN-Wavenet-B",
        "cmn-CN-Wavenet-C",
        "cmn-CN-Wavenet-D",
        "nb-no-Wavenet-E",
        "nb-no-Wavenet-A",
        "nb-no-Wavenet-B",
        "nb-no-Wavenet-C",
        "nb-no-Wavenet-D",
        "vi-VN-Wavenet-A",
        "vi-VN-Wavenet-B",
        "vi-VN-Wavenet-C",
        "vi-VN-Wavenet-D",
        "sr-rs-Standard-A",
        "lv-lv-Standard-A",
        "is-is-Standard-A",
        "bg-bg-Standard-A",
        "af-ZA-Standard-A",
        "Tracy",
        "Danny",
        "Huihui",
        "Yaoyao",
        "Kangkang",
        "HanHan",
        "Zhiwei",
        "Asaf",
        "An",
        "Stefanos",
        "Filip",
        "Ivan",
        "Heidi",
        "Herena",
        "Kalpana",
        "Hemant",
        "Matej",
        "Andika",
        "Rizwan",
        "Lado",
        "Valluvar",
        "Linda",
        "Heather",
        "Sean",
        "Michael",
        "Karsten",
        "Guillaume",
        "Pattara",
        "Jakub",
        "Szabolcs",
        "Hoda",
        "Naayf",
    ]

    @classmethod
    def text_to_audio(
        cls,
        message: str,
        voice: str = "Brian",
        save_to: Union[Path, str] = None,
        auto: bool = True,
    ) -> Union[str, bytes]:
        """
        Text to speech using StreamElements API

        Parameters:
            message (str): The text to convert to speech
            voice (str, optional): The voice to use for speech synthesis. Defaults to "Brian".
            save_to (bool, optional): Path to save the audio file. Defaults to None.
            auto (bool, optional): Generate filename based on `message` and save to `cls.cache_dir`. Defaults to False.

        Returns:
            result (Union[str, bytes]): Path to saved contents or audio content.
        """
        assert (
            voice in cls.all_voices
        ), f"Voice '{voice}' not one of [{', '.join(cls.all_voices)}]"
        # Base URL for provider API
        url: str = (
            f"https://api.streamelements.com/kappa/v2/speech?voice={voice}&text={{{urllib.parse.quote(message)}}}"
        )
        resp = requests.get(url=url, headers=cls.headers, stream=True)
        if not resp.ok:
            raise Exception(
                f"Failed to perform the operation - ({resp.status_code}, {resp.reason}) - {resp.text}"
            )

        def sanitize_filename(path):
            trash = [
                "\\",
                "/",
                ":",
                "*",
                "?",
                '"',
                "<",
                "|",
                ">",
            ]
            for val in trash:
                path = path.replace(val, "")
            return path.strip()

        if auto:
            filename: str = message + "..." if len(message) <= 40 else message[:40]
            save_to = cls.cache_dir / sanitize_filename(filename)
            save_to = save_to.as_posix()

        # Ensure cache_dir exists
        cls.cache_dir.mkdir(parents=True, exist_ok=True)

        if save_to:
            if not save_to.endswith("mp3"):
                save_to += ".mp3"

            with open(save_to, "wb") as fh:
                for chunk in resp.iter_content(chunk_size=512):
                    fh.write(chunk)
        else:
            return resp.content
        return save_to

    @staticmethod
    def play(path_to_audio_file: Union[Path, str]) -> NoReturn:
        """Play audio (.mp3) using playsound.
        """
        if not Path(path_to_audio_file).is_file():
            raise FileNotFoundError(f"File does not exist - '{path_to_audio_file}'")
        playsound(path_to_audio_file)
class ProxyManager:
    def __init__(self, refresh_interval=60):
        self.proxies: List[Tuple[str, float]] = []  # Store proxy and its latency
        self.last_refresh: float = 0
        self.refresh_interval = refresh_interval
        self.lock = threading.Lock()  # Add a lock for thread safety
        # Start auto-refresh in a separate thread
        threading.Thread(target=self.auto_refresh_proxies, daemon=True).start()

    def fetch_proxies(self, max_proxies=50) -> List[str]:
        try:
            url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
            response = requests.get(url)
            proxies = response.text.split('\r\n')[:max_proxies]  # Extract up to max_proxies
            return [proxy for proxy in proxies if proxy]
        except requests.RequestException as e:
            print(f"Error fetching proxies: {e}")
            return []

    def test_proxy(self, proxy: str) -> Tuple[str, float] | None:
        # Test both HTTP and HTTPS
        for protocol in ['http', 'https']:
            try:
                start_time = time.time()
                response = requests.get('http://httpbin.org/ip', proxies={protocol: f"{protocol}://{proxy}"}, timeout=5)
                if response.status_code == 200:
                    end_time = time.time()
                    return proxy, end_time - start_time
            except requests.RequestException:
                pass
        return None

    def refresh_proxies(self) -> int:
        new_proxies = self.fetch_proxies()
        threads = []
        working_proxies = []

        # Use threading for faster proxy testing
        for proxy in new_proxies:
            thread = threading.Thread(target=self.test_proxy_and_append, args=(proxy, working_proxies))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        with self.lock:  # Acquire lock before updating proxies list
            self.proxies = working_proxies
            self.last_refresh = time.time()

        # print(f"Refreshed proxies at {datetime.now()}. Total working proxies: {len(self.proxies)}")
        return len(self.proxies)

    def test_proxy_and_append(self, proxy: str, working_proxies: list):
        result = self.test_proxy(proxy)
        if result:
            with self.lock:  # Acquire lock before appending to shared list
                working_proxies.append(result)  # Append the proxy and its latency

    def auto_refresh_proxies(self):
        while True:
            time.sleep(self.refresh_interval)
            self.refresh_proxies()

    def get_fastest_proxy(self) -> str | None:
        with self.lock:  # Acquire lock before accessing proxies list
            if self.proxies:
                # Sort proxies by latency and return the fastest
                self.proxies.sort(key=lambda x: x[1])  # Sort by latency
                return self.proxies[0][0]  # Return the fastest proxy
        return None