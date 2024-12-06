from switchbot_utility.switchbot_ir_device import SwitchbotIrDevice


class IrLight(SwitchbotIrDevice):
    """Switchbot virtual IR Light"""

    def brightness_up(self) -> str:
        """Brightness up"""
        self._body["command"] = "brightnessUp"
        result = self.command(self.deviceId, self._body)
        return result.text

    def brightness_down(self) -> str:
        """Brightness down"""
        self._body["command"] = "brightnessDown"
        result = self.command(self.deviceId, self._body)
        return result.text
