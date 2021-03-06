
import json, os, logging
logger = logging.getLogger(__name__)

class Settings:
    """ Loads data from settings.txt into the bot """
    
    PATH = os.path.join(os.getcwd(), "settings.txt")
    
    def __init__(self, bot):
        try:
            # Try to load the file using json.
            # And pass the data to the Bot class instance if this succeeds.
            with open(Settings.PATH, "r") as f:
                settings = f.read()
                data = json.loads(settings)
                # "BannedWords" is only a key in the settings in older versions.
                # We moved to a separate file for blacklisted words.
                if "BannedWords" in data:
                    logger.info("Updating Blacklist system to new version...")
                    try:
                        with open("blacklist.txt", "r+") as f:
                            logger.info("Moving Banned Words to the blacklist.txt file...")
                            # Read the data, and split by word or phrase, then add BannedWords
                            banned_list = f.read().split("\n") + data["BannedWords"]
                            # Remove duplicates and sort by length, longest to shortest
                            banned_list = sorted(list(set(banned_list)), key=lambda x: len(x), reverse=True)
                            # Clear file, and then write in the new data
                            f.seek(0)
                            f.truncate(0)
                            f.write("\n".join(banned_list))
                            logger.info("Moved Banned Words to the blacklist.txt file.")
                    
                    except FileNotFoundError:
                        with open("blacklist.txt", "w") as f:
                            logger.info("Moving Banned Words to a new blacklist.txt file...")
                            # Remove duplicates and sort by length, longest to shortest
                            banned_list = sorted(list(set(data["BannedWords"])), key=lambda x: len(x), reverse=True)
                            f.write("\n".join(banned_list))
                            logger.info("Moved Banned Words to a new blacklist.txt file.")
                    
                    # Remove BannedWords list from data dictionary, and then write it to the settings file
                    del data["BannedWords"]

                    with open(Settings.PATH, "w") as f:
                        f.write(json.dumps(data, indent=4, separators=(",", ": ")))
                    
                    logger.info("Updated Blacklist system to new version.")

                bot.set_settings(data["Host"],
                                data["Port"],
                                data["Channel"],
                                data["Nickname"],
                                data["Authentication"],
                                data["DeniedUsers"],
                                data["Cooldown"],
                                data["KeyLength"],
                                data["MaxSentenceWordAmount"])

        except ValueError:
            logger.error("Error in settings file.")
            raise ValueError("Error in settings file.")

        except FileNotFoundError:
            Settings.write_default_settings_file()
            raise ValueError("Please fix your settings.txt file that was just generated.")
    
    @staticmethod
    def write_default_settings_file():
        # If the file is missing, create a standardised settings.txt file
        # With all parameters required.
        with open(Settings.PATH, "w") as f:
            standard_dict = {
                                "Host": "irc.chat.twitch.tv",
                                "Port": 6667,
                                "Channel": "#<channel>",
                                "Nickname": "<name>",
                                "Authentication": "oauth:<auth>",
                                "DeniedUsers": ["StreamElements", "Nightbot", "Moobot", "Marbiebot"],
                                "Cooldown": 20,
                                "KeyLength": 2,
                                "MaxSentenceWordAmount": 25
                            }
            f.write(json.dumps(standard_dict, indent=4, separators=(",", ": ")))

    @staticmethod
    def update_cooldown(cooldown):
        with open(Settings.PATH, "r") as f:
            settings = f.read()
            data = json.loads(settings)
        data["Cooldown"] = cooldown
        with open(Settings.PATH, "w") as f:
            f.write(json.dumps(data, indent=4, separators=(",", ": ")))

