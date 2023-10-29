from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.config import Config
from twilio.rest import Client
from jnius import autoclass


Config.set('graphics', 'width', '350')
Config.set('graphics', 'height', '500')


class MainScreen(BoxLayout):

    def _init_(self, **kwargs):
        super()._init_(**kwargs)

        self.orientation = 'vertical'
        self.padding = 50

        self.title_label = Label(text='Women Safety App', font_size='30sp', size_hint=(1, 0.3))
        self.add_widget(self.title_label)

        self.phone_number_label = Label(text='Enter Phone Number:', font_size='20sp', size_hint=(1, 0.1))
        self.add_widget(self.phone_number_label)

        self.phone_number_input = TextInput(multiline=False, font_size='20sp', size_hint=(1, 0.1))
        self.add_widget(self.phone_number_input)

        self.message_label = Label(text='Enter Message:', font_size='20sp', size_hint=(1, 0.1))
        self.add_widget(self.message_label)

        self.message_input = TextInput(multiline=False, font_size='20sp', size_hint=(1, 0.3))
        self.add_widget(self.message_input)

        self.send_button = Button(text='Send', font_size='20sp', size_hint=(1, 0.2))
        self.send_button.bind(on_press=self.send_message)
        self.add_widget(self.send_button)

    def send_message(self, instance):
        account_sid = 'AC2bcedecaa8ad370f9fed1c6b1d50f8b7'
        auth_token = 'ea604f81a2ff65a49756e1362ae4f203'
        client = Client(account_sid, auth_token)

        phone_number = self.phone_number_input.text
        message = self.message_input.text

        try:
            message = client.messages.create(
                to=phone_number,
                from_='+15074432169',
                body=message)

            popup = Popup(title='Success', content=Label(text='Message sent!'), size_hint=(None, None), size=(250, 150))
            popup.open()
        except Exception as e:
            popup = Popup(title='Error', content=Label(text='Message not sent: ' + str(e)), size_hint=(None, None), size=(350, 150))
            popup.open()

        # Use jnius to access the Android API
        PythonActivity = autoclass('org.renpy.android.PythonActivity')
        mActivity = PythonActivity.mActivity
        LocationManager = autoclass('android.location.LocationManager')
        locationManager = mActivity.getSystemService(PythonActivity.LOCATION_SERVICE)
        locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 0, 0, PythonActivity)

        location = locationManager.getLastKnownLocation(LocationManager.GPS_PROVIDER)

        if location:
            latitude = location.getLatitude()
            longitude = location.getLongitude()
            message = 'Help! I am in danger! My current location is: {}, {}'.format(latitude, longitude)


        try:
            message = client.messages.create(
                to=phone_number,
                from_='+15074432169',
                body=message)

            popup = Popup(title='Success', content=Label(text='Emergency message sent!'), size_hint=(None, None), size=(250, 150))
            popup.open()
        except Exception as e:
            popup = Popup(title='Error', content=Label(text='Emergency message not sent: ' + str(e)), size_hint=(None, None), size=(350, 150))
            popup.open()


class WomenSafetyApp(App):

    def build(self):
        return MainScreen()


if _name_ == '_main_':
    app = WomenSafetyApp()
    app.run()

    # get location using jnius
    Location = autoclass('android.location.Location')
    LocationManager = autoclass('android.location.LocationManager')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    mActivity = PythonActivity.mActivity
    locationManager = mActivity.getSystemService(Context.LOCATION_SERVICE)
    locationProvider = LocationManager.GPS_PROVIDER
    location = locationManager.getLastKnownLocation(locationProvider)

    if location is not None:
        latitude = location.getLatitude()
        longitude = location.getLongitude()
        message = 'Help! I am in danger! My current location is: {}, {}'.format(latitude, longitude)
        # send the emergency message
        try:
            message = client.messages.create(
                to=phone_number,
                from_='+15074432169',
                body=message)

            popup = Popup(title='Success', content=Label(text='Emergency message sent!'), size_hint=(None, None), size=(250, 150))
            popup.open()
        except Exception as e:
            popup = Popup(title='Error', content=Label(text='Emergency message not sent: ' + str(e)), size_hint=(None, None), size=(350, 150))
            popup.open()
