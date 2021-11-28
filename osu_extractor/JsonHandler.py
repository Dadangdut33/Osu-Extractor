import json
import os
import os.path
dir_path = os.path.dirname(os.path.realpath(__file__))
jsons_path = os.path.join(dir_path, '../json/')
setting_json_path = os.path.join(dir_path, '../json/Settings.json')
homedir = os.path.expanduser("~")

class JsonHandler:
    """
    Class to handle Create, Read, &  Update of json files
    """
    def __init__(self):
        self.settingsCache = None

        # Default Setting
        self.default_Setting = {
            "output_path": {
                "img": "default",
                "video": "default",
                "song": "default",
                "custom": "default"
            },
            "default_extract": {
                "song": True,
                "img": True,
                "video": False,
                "custom": False,
                "custom_list": []
            },
            "osu_path": f"{homedir}\AppData\Local\osu!"
        }

    # -------------------------------------------------
    # Create dir if not exists
    def createDirIfGone(self):
        """
        Create the json directory if not exists
        """
        if not os.path.exists(jsons_path):
            try:
                os.makedirs(jsons_path)
            except Exception as e:
                print("Error: " + str(e))
    
    # -------------------------------------------------
    # Settings
    def writeSetting(self, data):
        """Write setting

        Args:
            data (dict): Data to write

        Returns:
            bool: True if success, False if failed
            status: Status text of the operation
        """
        is_Success = False
        status = ""
        try:
            self.createDirIfGone()
            with open(setting_json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                status = "Setting has been changed successfully"
                is_Success = True
        except Exception as e:
            status = str(e)
            print("Error: " + str(e))
        finally:
            self.settingsCache = data
            return is_Success, status
    
    def setDefault(self):
        """Set default setting

        Returns:
            bool: True if success, False if failed
            status: Status text of the operation
        """
        is_Success = False
        status = ""
        try:
            self.createDirIfGone()
            with open(setting_json_path, 'w', encoding='utf-8') as f:
                json.dump(self.default_Setting, f, ensure_ascii=False, indent=4)
                status = "Successfully set setting to default"
                is_Success = True
        except Exception as e:
            status = str(e)
            print("Error: " + str(e))
        finally:
            self.settingsCache = self.default_Setting
            return is_Success, status

    def loadSetting(self):
        """Load setting

        Returns:
            bool: True if success, False if failed
            data: The data of the setting
        """
        is_Success = False
        data = ""
        try:
            self.createDirIfGone()
            with open(setting_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                is_Success = True
        except FileNotFoundError as e:
            data = "Settings.json not found! Program will now try creating a default Settings.json file"
            # Not found popup handled in main
        except Exception as e:
            data = str(e)
            print("Error: " + str(e))
        finally:
            self.settingsCache = data
            return is_Success, data

    def readSetting(self):
        """Read the currently loaded setting from the settings cache

        Returns:
            dict: The setting data
        """
        return self.settingsCache