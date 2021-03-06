# -*- coding: utf-8 -*-
##
##
## This file is part of CDS Indico.
## Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007 CERN.
##
## CDS Indico is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## CDS Indico is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with CDS Indico; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

from MaKaC.plugins.Collaboration.base import CSBookingBase
from MaKaC.plugins.Collaboration.WebcastRequest.mail import NewRequestNotification, RequestModifiedNotification, RequestDeletedNotification,\
    RequestRejectedNotification, RequestAcceptedNotification,\
    RequestAcceptedNotificationAdmin, RequestRejectedNotificationAdmin,\
    RequestRescheduledNotification, RequestRelocatedNotification
from MaKaC.common.mail import GenericMailer
from MaKaC.plugins.Collaboration.WebcastRequest.common import WebcastRequestException,\
    WebcastRequestError
from MaKaC.common.logger import Logger
from MaKaC.plugins.Collaboration.collaborationTools import MailTools
from MaKaC.i18n import _

class CSBooking(CSBookingBase):

    _hasStart = False
    _hasStop = False
    _hasCheckStatus = True
    _hasAcceptReject = True

    _needsBookingParamsCheck = True

    _allowMultiple = False

    _hasStartDate = False

    _simpleParameters = {
        "talks" : (str, ''),
        "talkSelection": (list, []),
        "otherComments": (str, ''),
        "audience": (str, '')}

    def __init__(self, type, conf):
        CSBookingBase.__init__(self, type, conf)

    def _checkBookingParams(self):
        return False

    def getStatusMessage(self):
        return self._statusMessage

    def hasHappened(self):
        return False

    def isHappeningNow(self):
        return False

    def _create(self):
        self._statusMessage = "Request successfully sent"
        self._statusClass = "statusMessageOther"

        if MailTools.needToSendEmails('WebcastRequest'):
            try:
                notification = NewRequestNotification(self)
                GenericMailer.sendAndLog(notification, self.getConference(),
                                     "MaKaC/plugins/Collaboration/WebcastRequest/collaboration.py",
                                     self.getConference().getCreator())
            except Exception,e:
                Logger.get('RecReq').exception(
                    """Could not send NewRequestNotification for request with id %s of event %s, exception: %s""" % (self._id, self.getConference().getId(), str(e)))
                return WebcastRequestError('create', e)


    def _modify(self, oldBookingParams):
        self._statusMessage = "Request successfully sent"
        self._statusClass = "statusMessageOther"

        if MailTools.needToSendEmails('WebcastRequest'):
            try:
                notification = RequestModifiedNotification(self)
                GenericMailer.sendAndLog(notification, self.getConference(),
                                     "MaKaC/plugins/Collaboration/WebcastRequest/collaboration.py",
                                     self.getConference().getCreator())
            except Exception,e:
                Logger.get('RecReq').exception(
                    """Could not send RequestModifiedNotification for request with id %s of event %s, exception: %s""" % (self._id, self.getConference().getId(), str(e)))
                return WebcastRequestError('edit', e)


    def _checkStatus(self):
        pass

    def _accept(self, user = None):
        self._statusMessage = "Request accepted"
        self._statusClass = "statusMessageOK"
        import MaKaC.webcast as webcast
        webcast.HelperWebcastManager.getWebcastManagerInstance().addForthcomingWebcast(self._conf, self._bookingParams.get("audience", ""))

        try:
            notification = RequestAcceptedNotification(self)
            GenericMailer.sendAndLog(notification, self.getConference(),
                                 "MaKaC/plugins/Collaboration/WebcastRequest/collaboration.py",
                                 None)
        except Exception,e:
            Logger.get('RecReq').exception(
                """Could not send RequestAcceptedNotification for request with id %s of event %s, exception: %s""" % (self._id, self.getConference().getId(), str(e)))
            return WebcastRequestError('accept', e)

        if MailTools.needToSendEmails('WebcastRequest'):
            try:
                notification = RequestAcceptedNotificationAdmin(self, user)
                GenericMailer.sendAndLog(notification, self.getConference(),
                                     "MaKaC/plugins/Collaboration/WebcastRequest/collaboration.py",
                                     None)
            except Exception,e:
                Logger.get('RecReq').exception(
                    """Could not send RequestAcceptedNotificationAdmin for request with id %s of event %s, exception: %s""" % (self._id, self.getConference().getId(), str(e)))
                return WebcastRequestError('accept', e)

        manager = self._conf.getCSBookingManager()
        manager.notifyInfoChange()

    def _reject(self):
        self._statusMessage = "Request rejected by responsible"
        self._statusClass = "statusMessageError"
        import MaKaC.webcast as webcast
        webcast.HelperWebcastManager.getWebcastManagerInstance().delForthcomingWebcast(self._conf)

        try:
            notification = RequestRejectedNotification(self)
            GenericMailer.sendAndLog(notification, self.getConference(),
                                 "MaKaC/plugins/Collaboration/WebcastRequest/collaboration.py",
                                 None)
        except Exception,e:
            Logger.get('RecReq').exception(
                """Could not send RequestRejectedNotification for request with id %s of event %s, exception: %s""" % (self._id, self.getConference().getId(), str(e)))
            return WebcastRequestError('reject', e)

        if MailTools.needToSendEmails('WebcastRequest'):
            try:
                notification = RequestRejectedNotificationAdmin(self)
                GenericMailer.sendAndLog(notification, self.getConference(),
                                     "MaKaC/plugins/Collaboration/WebcastRequest/collaboration.py",
                                     None)
            except Exception,e:
                Logger.get('RecReq').exception(
                    """Could not send RequestRejectedNotificationAdmin for request with id %s of event %s, exception: %s""" % (self._id, self.getConference().getId(), str(e)))
                return WebcastRequestError('reject', e)

    def _delete(self):
        import MaKaC.webcast as webcast
        webcast.HelperWebcastManager.getWebcastManagerInstance().delForthcomingWebcast(self._conf)

        if MailTools.needToSendEmails('WebcastRequest'):
            try:
                notification = RequestDeletedNotification(self)
                GenericMailer.sendAndLog(notification, self.getConference(),
                                     "MaKaC/plugins/Collaboration/WebcastRequest/collaboration.py",
                                     self.getConference().getCreator())
            except Exception,e:
                Logger.get('RecReq').exception(
                    """Could not send RequestDeletedNotification for request with id %s of event %s, exception: %s""" % (self._id, self.getConference().getId(), str(e)))
                return WebcastRequestError('remove', e)

    def notifyEventDateChanges(self, oldStartDate, newStartDate, oldEndDate, newEndDate):
        manager = self._conf.getCSBookingManager()
        manager._changeConfStartDateInIndex(self, oldStartDate, newStartDate)
        if MailTools.needToSendEmails('WebcastRequest'):
            try:
                notification = RequestRescheduledNotification(self)
                GenericMailer.sendAndLog(notification, self.getConference(),
                                     "MaKaC/plugins/Collaboration/WebcastRequest/collaboration.py",
                                     self.getConference().getCreator())
            except Exception,e:
                Logger.get('RecReq').exception(
                    """Could not send RequestRescheduledNotification for request with id %s of event %s, exception: %s""" % (self._id, self.getConference().getId(), str(e)))
                return WebcastRequestError('edit', e)

    def notifyLocationChange(self):
        if MailTools.needToSendEmails('WebcastRequest'):
            try:
                notification = RequestRelocatedNotification(self)
                GenericMailer.sendAndLog(notification, self.getConference(),
                                     "MaKaC/plugins/Collaboration/WebcastRequest/collaboration.py",
                                     self.getConference().getCreator())
            except Exception,e:
                Logger.get('RecReq').exception(
                    """Could not send RequestRelocatedNotification for request with id %s of event %s, exception: %s""" % (self._id, self.getConference().getId(), str(e)))
                return WebcastRequestError('edit', e)