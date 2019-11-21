# CubeWorks Pi Configurator

## Android App

The Android App is available on the Google Play Store:

<a href='https://play.google.com/store/apps/details?id=de.cubeworksgmbh.android.piconfigurator'>
<img alt='Get it on Google Play' width='300px' src='https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png'/>
</a>

https://play.google.com/store/apps/details?id=de.cubeworksgmbh.android.piconfigurator

## Bluetooth Server

### Dependencies

Install the following dependencied on your Raspberry Pi

    sudo apt-get install pi-bluetooth
    sudo apt-get install bluetooth bluez
    sudo apt-get install bluez python-bluez

### Run the server

    sudo python server.py

## Protocol

There are basically two important command to handle from the server:

* `get`
* `save [...]`

Commands are seperated by a new line ('\n').

The server should allways respond to these commands with
`values [...]`

All values provided by the `values` response will be showed to the user.

Values are JSON encoded objects containing the following keys

* label (only required field): Text to show
* value: current value of the text input field (default: "")
* unit: Text to show behind value field (default: "")
* type: "text", "label", "error", "success", "readonly" (defult: "text")

### Examples

- App -> Pi: `get`
- Pi -> App: `values [{"label": "Value 1", "value": "42", "unit": "x"},{"label": "Value 2", "value": "23", "unit": "y"}]`
- App -> Pi: `save [{"label": "Value 1", "value": "1", "unit": "x"},{"label": "Value 2", "value": "2", "unit": "y"}]`
- Pi -> App: `values [{"label": "All values saved!", "type": "success"}]`
