import psutil
import rumps
from Foundation import NSUserNotification
from Foundation import NSUserNotificationCenter
from Foundation import NSUserNotificationDefaultSoundName


def send_notification(title, text):
    notification = NSUserNotification.alloc().init()
    notification.setTitle_(title)
    notification.setInformativeText_(text)
    notification.setSoundName_(NSUserNotificationDefaultSoundName)


def get_battery_level():
    battery = psutil.sensors_battery()
    if battery is None:
        return "No battery detected"
    else:
        return f"Battery at {battery.percent}%"


class BatteryStatusApp(rumps.App):
    def __init__(self):
        super(BatteryStatusApp, self).__init__("Battery Status")
        self.menu = ["Battery level: N/A"]

    def check_battery_level(self, battery_level):
        if battery_level and battery_level < 20:
            send_notification("Low battery", "Battery is below 20%")

    @rumps.timer(60)
    def update_battery_level(self, _):
        battery_level = get_battery_level()
        self.menu = [f"Battery level: {battery_level}"]
        self.check_battery_level(battery_level) if type(battery_level) is int else None


if __name__ == "__main__":
    send_notification("Low battery", "Battery is below 20%")
    app = BatteryStatusApp()
    app.run()
