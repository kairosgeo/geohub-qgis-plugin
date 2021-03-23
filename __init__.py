# -----------------------------------------------------------
# Copyright (C) 2021 Vitor Muniz
# -----------------------------------------------------------
# Licensed under the terms of GNU GPL 3
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# ---------------------------------------------------------------------

import sys
import json
from qgis.core import QgsNetworkAccessManager, Qgis
from PyQt5.QtWidgets import QAction
from PyQt5.QtNetwork import QNetworkRequest, QNetworkReply
from PyQt5.QtCore import QUrl, QByteArray


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
        self.__handle__response(self.__geo_hub_api.get_weather())

    def __handle__response(self, reply):
        er = reply.error()
        if er == QNetworkReply.NoError:
            response_json = json.loads(bytes(reply.content()))
            self.iface.messageBar().pushMessage(
                "Sucesso", str(response_json), level=Qgis.Success)
        else:
            self.iface.messageBar().pushMessage(
                "Erro", reply.errorString(), level=Qgis.Critical)


class GeoHubApi:
    def __init__(self, url):
        self.__baseUrl = url

    def get_weather(self):
        request = QNetworkRequest(QUrl(f"{self.__baseUrl}/repositories"))
        request.setHeader(QNetworkRequest.ContentTypeHeader,
                          QByteArray(b'application/json'))
        return QgsNetworkAccessManager.instance().blockingGet(request)
