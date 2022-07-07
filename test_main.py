import firebase_admin
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from workout_banner import WorkoutBanner
from kivy.uix.label import Label
import requests
import json
import os
from os import walk
from functools import partial
from test_firebase import MyFireBase
from firebase_admin import auth, credentials, db
import pyrebase
import firebase
# import os
# from dotenv import load_dotenv
# load_dotenv()

class HomeScreen(Screen):
    pass
class LabelButton(ButtonBehavior, Label):
    pass
class ImageButton(ButtonBehavior, Image):
    pass
class ChangeAvatarScreen(Screen):
    pass
class LoginScreen(Screen):
    pass
class AddFriendScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass


# user = auth.create_user(email='rrr@gmail.com',password='121212')
# users_ref.child('users').push(user.email)



'''Delete all user from DB'''
# users_ref = db.reference('/users')
# users_ref.set('')
# quit()
'''Delete all user from auth'''
# firebase_admin.initialize_app()
# all_user = auth.list_users().users
# all_user_uid = []
# for user in all_user:
#     all_user_uid.append(user.uid)
# for uid in all_user_uid:
#     auth.delete_user(uid)
# quit()


GUI = Builder.load_file('main.kv')

GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
# cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
# firebase_admin.initialize_app(cred)

'''Setting up pyrebase'''
firebase_config = {
    'apiKey': "AIzaSyAV8XcBYsI11P15Asy1Vtm7k4uwsSdKDtw",
    'authDomain': "test-project-80109.firebaseapp.com",
    'databaseURL': "https://test-project-80109-default-rtdb.firebaseio.com",
    'projectId': "test-project-80109",
    'storageBucket': "test-project-80109.appspot.com",
    'messagingSenderId': "1009245828697",
    'appId': "1:1009245828697:web:a46bc86feec4e064882348",
    'measurementId': "G-T086LY8ESC",
    'serciveAccount': GOOGLE_APPLICATION_CREDENTIALS
}
my_firebase = pyrebase.initialize_app(firebase_config)
config_auth = my_firebase.auth()
config_db = my_firebase.database()


'''Start running main app'''
class MainApp(App):
    def build(self):
        self.my_firebase = MyFireBase()
        return GUI

    def on_start(self):

        # Populate avatar grid
        avatar_grid = self.root.ids['change_avatar_screen'].ids['avatar_grid']
        for root_dir, folder, file in walk("avatars"):
            for f in file:
                img = ImageButton(source="avatars/" + f, on_release=partial(self.my_firebase.change_avatar, f))
                avatar_grid.add_widget(img)




    def change_screen(self, screen_name):

        '''Changin screen change direction back to left (changed to right in change avatar function) '''
        self.root.ids['screen_manager'].transition.direction = 'left'
        # Gets the screen manager from the root
        screen_manager = self.root.ids['screen_manager']

        # Sets the current screen to the screen that was passed
        # in as parameter in homescreen.kv - app.change_screen
        screen_manager.current = screen_name

    def add_friend(self, friend_id):
        friend_exists = config_db.child('users').order_by_child('my_friend_id').equal_to(str(friend_id)).get()
        if friend_exists[0].val()['my_friend_id'] == friend_id:
            print('found')
        else:
            print('There is no user with this id')



MainApp().run()
