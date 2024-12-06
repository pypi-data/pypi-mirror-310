from switchbot_utility.switchbot_device import SwitchbotDevice


class IrOthers(SwitchbotDevice):
    """IR virtual device others class"""

    def customize(self, button_name: str) -> str:
        """Execute customized button

        Args:
            button_name (str):
        """

        body = {"commandType": "customize", "parameter": "default"}
        body["command"] = button_name

        response = self.command(self.deviceId, body)
        return response.text
