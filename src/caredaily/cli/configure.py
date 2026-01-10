import os
from configparser import ConfigParser

import click
from tabulate import tabulate

from caredaily import (
    Authentication,
    CareDaily,
    CloudConnectivity,
    APIKeyType,
    CareDailyException,
)


@click.group("configure", short_help="Manage configuration.")
@click.pass_context
def configure(ctx):
    pass


@click.command("interactive", short_help="Interactive configuration.")
@click.option("--profile", help="The profile to use.")
@click.option("--username", help="Username")
@click.option("--password", help="Password", hide_input=True)
@click.pass_context
def interactive(ctx, profile, username, password):
    """
    Interactive configuration command for setting up CareDaily profiles.

    This command allows users to interactively configure their CareDaily profiles,
    including hostname, SSL verification, proxies, API key, and key type.
    """
    profile = profile or ctx.obj.get("profile") or os.environ.get("CAREDAILY_PROFILE")
    try:
        config_object = ConfigParser()
        credentials_object = ConfigParser()

        # Determine the user profile directory based on the operating system
        if os.name == "nt":  # Windows
            user_profile = os.environ["UserProfile"]
        else:  # Unix-based systems
            user_profile = os.environ["HOME"]

        profile = profile or os.environ.get("CAREDAILY_PROFILE")
        if not profile:
            click.echo("Profile not specified. Use CAREDAILY_PROFILE environment variable or --profile option.")
            return
        config_path = os.path.join(user_profile, ".caredaily", "config")
        credentials_path = os.path.join(user_profile, ".caredaily", "credentials")

        # Read the configuration file
        config_object.read(config_path)
        if "default" not in config_object.sections():
            click.echo("Configuration not initialized. Run `caredaily configure init` first.")
            return
        
        default_config = config_object["default"]
        if not config_object.has_section(f"profile {profile}"):
            config_object[f"profile {profile}"] = {}
        profile_config = config_object[f"profile {profile}"] if profile else {}

        click.echo(f"Configuring profile: {profile}")

        # Prompt for hostname
        hostname = (
            profile_config.get("hostname") or default_config.get("hostname") or "None"
        )
        _hostname = click.prompt("CareDaily Hostname", default=hostname)

        if _hostname != hostname:
            profile_config["hostname"] = _hostname

        # Prompt for SSL verification
        ssl_verify = (
            profile_config.get("ssl_verify")
            or default_config.get("ssl_verify")
            or "true"
        )
        _ssl_verify = click.confirm("SSL Verify", default=bool(ssl_verify))
        if _ssl_verify != bool(ssl_verify):
            profile_config["ssl_verify"] = "true" if _ssl_verify else "false"

        # Prompt for proxies
        proxies = (
            profile_config.get("proxies") or default_config.get("proxies") or ""
        )
        _proxies = click.prompt("Proxies", default=proxies)
        if _proxies != proxies:
            profile_config["proxies"] = _proxies

        ctx.obj["caredaily"].update_config("hostname", hostname)
        ctx.obj["caredaily"].update_config("ssl_verify", _ssl_verify)
        ctx.obj["caredaily"].update_config("proxies", proxies)
        try:
            ctx.obj["caredaily"].app_api(CloudConnectivity).check_availability()
        except Exception as e:
            import traceback
            click.echo(traceback.format_exc())
            click.echo(f"Error checking availability: {e}")
            return
        
        # Write the updated configuration to the file
        with open(config_path, "w") as configfile:
            config_object.write(configfile)

        # Read the credentials file
        credentials_object.read(credentials_path)
        default_credentials = credentials_object["default"]
        if not credentials_object.has_section(f"{profile}"):
            credentials_object[f"{profile}"] = {}
        profile_credentials = credentials_object[f"{profile}"] if profile else {}

        sign_in = username or password
        if not sign_in:
            # Prompt user to optionally sign in
            sign_in = click.confirm("Sign in with username?")
        if sign_in:
            if not username:
                username = click.prompt("Enter your username", default="", show_default=False)
            if not password:
                password = click.prompt("Enter your password", default="", hide_input=True, show_default=False)
            key_type_prompt = click.prompt(
                "Key type:",
                type=click.Choice(['User', 'Admin']),
                default='User',
                show_choices=True
            )
            key_type = (
                APIKeyType.USER 
                if key_type_prompt == "User" 
                else APIKeyType.ADMIN
            )
            try:
                result = (
                    ctx.obj["caredaily"]
                    .app_api(Authentication)
                    .login_by_username(
                        username=username, 
                        password=password, 
                        key_type=key_type)
                )
            except CareDailyException as e:
                if e.context.get("resultCode") == 17:
                    click.echo(f"{e.message}")
                    passcode = click.prompt("Enter passcode:")
                    result = (
                        ctx.obj["caredaily"]
                        .app_api(Authentication)
                        .login_by_username(username=username, passcode=passcode, key_type=key_type)
                    )
                else:
                    raise e
            profile_credentials["key"] = result.data.get("key", "")
            profile_credentials["key_expire_ms"] = f"{result.data.get('keyExpireMs', '')}"
            profile_credentials["key_type"] = f"{result.data.get('keyType', '')}"
        else:
            # Prompt for API key
            api_key = profile_credentials.get("key") or default_credentials.get("key")
            _api_key = click.prompt(f"API Key [{None if not api_key else f'***{api_key[:5]}'}]", default=api_key, show_default=False)
            if _api_key != api_key:
                profile_credentials["key"] = _api_key

            # Prompt for key type
            key_type = profile_credentials.get("key_type") or default_credentials.get(
                "key_type"
            )
            _key_type = click.prompt("Key Type", default=key_type)
            if _key_type != key_type:
                profile_credentials["key_type"] = _key_type

        # Write the updated credentials to the file
        with open(credentials_path, "w") as credentialsfile:
            credentials_object.write(credentialsfile)
        ctx.invoke(list, profile=profile)
        click.echo(f"Configured '{profile}' successfully.")
    except Exception as e:
        import traceback
        click.echo(traceback.format_exc())
        raise click.UsageError(f"Error while managing configuration file: {e}")
    pass


@click.command("list", short_help="List the current configuration.")
@click.option("--profile", help="The profile to use.")
@click.pass_context
def list(ctx, profile):
    """
    List the current configuration for CareDaily profiles.

    This command lists the current configuration settings for the specified profile,
    including hostname, SSL verification, proxies, API key, and key type.
    """

    class Config:
        def __init__(self, name, value="<not set>", type="None", location="None"):
            """
            Initialize a Config object.

            :param name: The name of the configuration setting.
            :param value: The value of the configuration setting.
            :param type: The type of the configuration setting.
            :param location: The location of the configuration setting.
            """
            self.name = name
            self.value = value
            self.type = type
            self.location = location

        def get_config(self):
            """
            Get the configuration as a dictionary.

            :return: A dictionary representation of the configuration.
            """
            return {
                "name": self.name,
                "value": self.value,
                "type": self.type,
                "location": self.location,
            }

    # Initialize configuration settings
    config = {
        "profile": Config(name="profile"),
        "hostname": Config(name="hostname"),
        "ssl_verify": Config(name="ssl_verify"),
        "proxies": Config(name="proxies"),
        "key": Config(name="key"),
        "key_type": Config(name="key_type"),
    }

    config_object = ConfigParser()
    credentials_object = ConfigParser()

    # Determine the user profile directory based on the operating system
    if os.name == "nt":  # Windows
        user_profile = os.environ["UserProfile"]
    else:  # Unix-based systems
        user_profile = os.environ["HOME"]

    # Determine the profile type and location
    profile_type = "None"
    profile_location = "None"
    if profile:
        profile_type = "profile"
    elif os.environ.get("CAREDAILY_PROFILE"):
        profile_type = "environment"
        profile_location = "CAREDAILY_PROFILE"

    profile = profile or os.environ.get("CAREDAILY_PROFILE")
    config["profile"].value = profile or "<not set>"
    config["profile"].type = profile_type
    config["profile"].location = profile_location

    # Paths to configuration and credentials files
    config_path = os.path.join(user_profile, ".caredaily", "config")
    credentials_path = os.path.join(user_profile, ".caredaily", "credentials")

    # Read the configuration file
    config_object.read(config_path)
    default_config = config_object["default"]
    try:
        profile_config = config_object[f"profile {profile}"] if profile else {}
    except KeyError:
        raise click.BadParameter(f"Profile '{profile}' not found.")

    # Set configuration values
    config["hostname"].value = (
        profile_config.get("hostname") or default_config.get("hostname") or "<not set>"
    )
    config["hostname"].type = "config_file"
    config["hostname"].location = config_path

    config["ssl_verify"].value = (
        profile_config.get("ssl_verify")
        or default_config.get("ssl_verify")
        or "<not set>"
    )
    config["ssl_verify"].type = "config_file"
    config["ssl_verify"].location = config_path

    config["proxies"].value = (
        profile_config.get("proxies") or default_config.get("proxies") or "<not set>"
    )
    config["proxies"].type = "config_file"
    config["proxies"].location = config_path

    # Read the credentials file
    credentials_object.read(credentials_path)
    default_credentials = credentials_object["default"]
    profile_credentials = credentials_object[f"{profile}"] if profile else {}

    def obfuscate_string(s: str = "<not set>") -> str:
        """
        Obfuscating strings and limiting to 9 characters

        :param s: The string to obfuscate.
        :return: The obfuscated string.
        """
        if s == "<not set>":
            return s
        return "*" * 5 + s[-4:]

    # Set credentials values
    config["key"].value = obfuscate_string(
        profile_credentials.get("key") or default_credentials.get("key") or "<not set>"
    )
    config["key"].type = "credentials_file"
    config["key"].location = credentials_path

    config["key_type"].value = (
        profile_credentials.get("key_type")
        or default_credentials.get("key_type")
        or "<not set>"
    )
    config["key_type"].type = "credentials_file"
    config["key_type"].location = credentials_path

    # Display the configuration in a table format
    click.echo(
        tabulate(
            [[v.name, v.value, v.type, v.location] for k, v in config.items()],
            headers=["Name", "Value", "Type", "Location"],
        )
    )


@click.command("list-profiles", short_help="List configured profiles.")
@click.pass_context
def list_profiles(ctx):
    """
    List configured profiles for CareDaily.

    This command lists all the profiles that are configured in the CareDaily credentials file.
    """

    # Determine the user profile directory based on the operating system
    if os.name == "nt":  # Windows
        user_profile = os.environ["UserProfile"]
    else:  # Unix-based systems
        user_profile = os.environ["HOME"]

    # Path to the credentials file
    credentials_path = os.path.join(user_profile, ".caredaily", "credentials")

    # Read the credentials file
    credentials_object = ConfigParser()
    credentials_object.read(credentials_path)

    # List all sections (profiles) in the credentials file
    click.echo("\t".join(credentials_object.sections()))


@click.command("init", short_help="Initialize the default configuration profiles.")
@click.pass_context
def init(ctx):
    """
    Initialize a default or specific profile in the ~/.caredaily/ directory.

    This command creates the necessary configuration and credentials files for a profile.
    """
    try:
        # Determine the user profile directory based on the operating system
        if os.name == "nt":  # Windows
            user_profile = os.environ["UserProfile"]
        else:  # Unix-based systems
            user_profile = os.environ["HOME"]

        caredaily_dir = os.path.join(user_profile, ".caredaily")
        config_path = os.path.join(caredaily_dir, "config")
        credentials_path = os.path.join(caredaily_dir, "credentials")

        # Check if the directory or files already exist
        if os.path.exists(caredaily_dir):
            if os.path.exists(config_path) or os.path.exists(credentials_path):
                click.echo("Configuration already exists, use `caredaily configure interactive`.")
                return
                
        # Prompt user for hostname
        hostname = click.prompt("CareDaily Hostname", default="app.peoplepowerco.com")
        ctx.obj["caredaily"].update_config("hostname", hostname)
        try:
            ctx.obj["caredaily"].app_api(CloudConnectivity).check_availability()
        except Exception as e:
            click.echo(f"Error checking availability: {e}")
            return

        # Prompt user for optional core and private paths
        current_path = os.getcwd()
        core_path = click.prompt("Optional core path", default=f"{current_path}", show_default=True)
        private_path = click.prompt("Optional private path", default=f"{current_path}", show_default=True)

        # Prompt user to optionally sign in
        sign_in = click.confirm("Would you like to sign in and save credentials?")
        key, key_expire_ms, key_type = "", "", ""
        if sign_in:
            username = click.prompt("Enter your username", default="", show_default=False)
            password = click.prompt("Enter your password", default="", hide_input=True, show_default=False)
            result = (
                ctx.obj["caredaily"]
                .app_api(Authentication)
                .login_by_username(username=username, password=password)
            )

            key = result.data.get("key", "")
            key_expire_ms = result.data.get("key_expire_ms", "")
            key_type = result.data.get("key_type", "")
        

        def obfuscate_string(s: str = "<not set>") -> str:
            """
            Obfuscating strings and limiting to 9 characters

            :param s: The string to obfuscate.
            :return: The obfuscated string.
            """
            if s == "":
                return s
            return "*" * 5 + s[-4:]
        
        profile = None
        if os.environ.get("CAREDAILY_PROFILE") is not None:
            profile = os.environ.get("CAREDAILY_PROFILE")
            click.echo(f"Initializing known profile: {profile}")

        # Echo and describe the changes
        click.echo(f"Creating CareDaily config at {config_path}:")
        click.echo(
            "\n```\n"
            f"[default]\n"
            f"hostname = app.peoplepowerco.com\n"
            f"ssl_verify = true\n"
            f"proxies = \n"
            f"core_path = {core_path}\n"
            f"private_path = {private_path}"
        )
        if profile:
            click.echo(
                f"\n[profile {profile}]"
            )
        click.echo("```\n")
        click.echo(f"Creating CareDaily credentials at {credentials_path}:")
        click.echo(
            "\n```\n"
            f"[default]\n"
            f"key = {key}\n"
            f"key_expire_ms = {key_expire_ms}\n"
            f"key_type = {key_type}\n"
        )
        if profile and profile != "default":
            click.echo(
                f"\n[{profile}]\n"
                f"key = {obfuscate_string(key)}\n"
                f"key_expire_ms = {key_expire_ms}\n"
                f"key_type = {key_type}"
            )
        click.echo("```\n")
        # Confirm with the user
        if not click.confirm("Do you want to proceed?"):
            click.echo("Initialization canceled.")
            return

        # Create the directory and files
        os.makedirs(caredaily_dir, exist_ok=True)

        # Write to the config file
        with open(config_path, "w") as config_file:
            config_file.write(
                f"[default]\n"
                f"hostname = app.peoplepowerco.com\n"
                f"ssl_verify = true\n"
                f"proxies = \n"
                f"core_path = {core_path}\n"
                f"private_path = {private_path}\n"
            )
            if profile:
                config_file.write(
                    f"\n[profile {profile}]\n"
                )

        # Write to the credentials file
        with open(credentials_path, "w") as credentials_file:
            credentials_file.write(
                f"[default]\n"
                f"key = {key}\n"
                f"key_expire_ms = {key_expire_ms}\n"
                f"key_type = {key_type}\n"
            )
            if profile and profile != "default":
                credentials_file.write(
                    f"\n[{profile}]\n"
                    f"key = {key}\n"
                    f"key_expire_ms = {key_expire_ms}\n"
                    f"key_type = {key_type}\n"
                )
            
        ctx.invoke(list)
        click.echo("Initialization completed successfully.")
    except Exception as e:
        import traceback
        click.echo(traceback.format_exc())
        click.echo(f"Error during initialization: {e}")


configure.add_command(interactive)
configure.add_command(list)
configure.add_command(list_profiles)
configure.add_command(init)
