from pathlib import Path
import os
from InquirerPy import prompt
import os
import json
from shutil import copyfile

CONFIGURE_PATH = f"{os.getenv('HOME')}/.slack_async_alert/credentials.json"
slack_async_alert_CLI_PATH = f"{os.getenv('HOME')}/.slack_async_alert/bin"
CONFIGURE_PATH = os.getenv("CONFIGURE_PATH", CONFIGURE_PATH)


def set_configure():
    # prepare directory
    Path(os.path.dirname(CONFIGURE_PATH)).mkdir(exist_ok=True, parents=True)
    if os.path.exists(CONFIGURE_PATH):
        with open(CONFIGURE_PATH) as f:
            prompt_settings = json.load(f)
    else:
        prompt_settings = {"slack_key": None}

    config_qus = []
    for default_qus in CONFIGURE_QUESTIONS:
        default_qus["default"] = prompt_settings[default_qus["name"]]
        config_qus.append(default_qus)

    answers = prompt(config_qus)
    with open(CONFIGURE_PATH, "w") as f:
        json.dump(answers, f, indent=4, sort_keys=True)


def get_configure():
    if not os.path.exists(CONFIGURE_PATH):
        raise ValueError(
            f"Slack api key not found, check {CONFIGURE_PATH} file exists, and has api key\n if not exists, use slrt-configure to set api-key."
        )
    with open(CONFIGURE_PATH) as f:
        prompt_settings = json.load(f)
    
    # install slrt command, if not exists.
    # check slrt command installed
    return_code = os.system("which slrt")
    if return_code != 0:
        # export command
        export_command = f'export PATH="$PATH:{slack_async_alert_CLI_PATH}"'
        # find bash type
        shell_type = os.getenv("SHELL").split("/")[-1]
        if shell_type in ["bash", "zsh"]:
            if shell_type == "bash":
                shell_config_path = f"{os.getenv('HOME')}/.bashrc"
            elif shell_type == "zsh":
                shell_config_path = f"{os.getenv('HOME')}/.zshrc"
            with open(shell_config_path, "a") as f:
                f.write(f"\n{export_command}")
        else:
            Warning(f'we cannot support your shell program, add "{export_command}" to your shell config file(ex. .bashrc, .zshrc)')
        Path(slack_async_alert_CLI_PATH).mkdir(exist_ok=True, parents=True)
        copyfile(os.path.join(os.path.dirname(__file__), "slrt"), os.path.join(slack_async_alert_CLI_PATH, "slrt"))
        os.system(f'chmod 777 {os.path.join(slack_async_alert_CLI_PATH, "slrt")}')
    return prompt_settings


CONFIGURE_QUESTIONS = [
    {
        "type": "input",
        "name": "slack_key",
        "message": "What's your slack key?",
    },
    {
        "type": "input",
        "name": "user_id",
        "message": "What's your slack user id?",
    },
    {
        "type": "input",
        "name": "hardware_identifier",
        "message": "Is there any identifier when you receive from this server/computer?",
    },
]
