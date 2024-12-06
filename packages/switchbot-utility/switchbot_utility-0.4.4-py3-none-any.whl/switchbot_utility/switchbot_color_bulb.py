from switchbot_utility.switchbot_strip_light import SwitchbotStripLight


class SwitchbotColorBulb(SwitchbotStripLight):
    """Switchbot Color Bulb class"""

    def set_color_temperature(self, temperature: int) -> str:
        """Set color temperature"""
        body = {
            "commandType": "command",
            "command": "setColorTemperature",
        }
        body["parameter"] = temperature
        result = self.command(self.deviceId, body)
        return result.text

    def get_color_temperature(self) -> dict:
        """Returns the color temperature value, range from 2700 to 6500"""
        status = self.get_status()
        return status["colorTemperature"]
