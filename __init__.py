#-----------------------------------------------------------
# Copyright (C) 2021 Vitor Muniz
#-----------------------------------------------------------
# Licensed under the terms of GNU GPL 3
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#---------------------------------------------------------------------

from PyQt5.QtWidgets import QAction, QMessageBox
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtCore import QUrl
import sys, json

def classFactory(iface):
    return GeoHubPlugin(iface)

class GeoHubPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.__geo_hub_api = GeoHubApi('http://localhost:5000')

    def initGui(self):
        self.action = QAction('GeoHub', self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def run(self):
        self.__geo_hub_api.get_weather(self.__handle__response)        

    def __handle__response(self, reply):
        er = reply.error()
        if er == QNetworkReply.NoError:
            bytes_string = reply.readAll()
            json_ar = json.loads(str(bytes_string, 'utf-8'))
            QMessageBox.information(None, 'GeoHubPlugin', str(json_ar))
        else:
            QMessageBox.information(None, 'GeoHubPlugin', reply.errorString())

class GeoHubApi:
    def __init__(self, url):
        self.__baseUrl = url
        self.__manager = QNetworkAccessManager()

    def get_weather(self, handler):        
        request = QNetworkRequest(QUrl(f"{self.__baseUrl}/WeatherForecast"))
        self.__manager.finished.connect(handler)
        self.__manager.get(request)

        