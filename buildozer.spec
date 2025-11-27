[app]

# (str) Title of your application
title = CyberGuardian

# (str) Package name
package.name = cyberguardian

# (str) Package domain (needed for android/ios packaging)
package.domain = org.cyberguardian

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,html,css,js,json,txt

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,flask,flask-cors,requests,chardet,idna,urllib3,certifi

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (list) Garden requirements
#garden_requirements =

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (str) Android additional adb arguments
#android.adb_args = -H 127.0.0.1

# (list) Android application meta-data to set (key=value format)
#android.meta_data =

# (str) XML file to include as an intent filters in <activity> tag
#android.manifest.intent_filters =

# (str) launchMode to set for the main activity
#android.manifest.launch_mode = standard

# (list) Android additional libraries to copy into libs/armeabi
#android.add_libs_armeabi = libs/android/*.so
#android.add_libs_armeabi_v7a = libs/android-v7/*.so
#android.add_libs_arm64_v8a = libs/android-v8/*.so
#android.add_libs_x86 = libs/android-x86/*.so
#android.add_libs_mips = libs/android-mips/*.so

# (bool) Indicate whether the screen should stay on
# Don't sleep on app
#android.wakelock = False

# (list) Android additionnal jars to add to the application
#android.add_jars = foo.jar,bar.jar,./some/path/baz.jar

# (list) Android aapt2 compile args
#android.aapt2_compile_args =

# (list) Android packaging options
#android.packaging_options =

# (list) Java classes to add as activities to the manifest android.manifest.application.activity.
#android.add_activities = com.example.ExampleActivity

#
# Python for android (p4a) specific
#

# (str) python-for-android fork to use, defaults to upstream (kivy)
#p4a.fork = kivy

# (str) python-for-android branch to use, defaults to master
#p4a.branch = master

# (str) Bootstrap to use for android builds
# p4a.bootstrap = sdl2

# (int) Port number to specify an explicit --port= p4a argument (eg for bootstrap flask)
#p4a.port =

# (str) python-for-android recipes to use, defaults to empty
#p4a.local_recipes =

# (list) python-for-android whitelist
#p4a.whitelist =

# (bool) If True, then skip trying to update the p4a package code with git
#p4a.hook =

# (bool) If True, then automatically launch the app on the device
#p4a.launcher = False

#
# iOS specific
#

# (str) Path to a custom kivy-ios folder
#ios.kivy_ios_dir = ../kivy-ios
# (str) CMake package location
#ios.cmake_package =

# (str) PythonHome location
#ios.python_home =

# (str) Python library location
#ios.python_lib =

# (str) The name of the python library
#ios.python_lib_name =

# (str) The path to the python library
#ios.python_lib_path =

# (str) The path to the python include
#ios.python_include =

# (str) The path to the python site-packages
#ios.python_site_packages =

# (str) The path to the python site-packages
#ios.python_site_packages_dir =

# (str) The path to the python site-packages
#ios.python_site_packages_dir_name =

# (str) The path to the python site-packages
#ios.python_site_packages_dir_path =

# (str) The path to the python site-packages
#ios.python_site_packages_dir_path_name =

# (str) The path to the python site-packages
#ios.python_site_packages_dir_path_name_ext =

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output storage, absolute or relative to spec file
# bin_dir = ./bin

#    -----------------------------------------------------------------------------
#    List as sections
#
#    You can define all the "list" as [section:name].
#    Each line will be considered as a option to the list.
#    Let's take [app] / source.exclude_patterns.
#    Instead of doing:
#
#        [app]
#        source.exclude_patterns = license,data/audio/*.wav,data/images/original/*
#
#    You can do:
#
#        [app:source.exclude_patterns]
#        license
#        data/audio/*.wav
#        data/images/original/*
#
