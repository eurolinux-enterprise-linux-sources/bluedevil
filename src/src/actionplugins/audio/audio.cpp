/*************************************************************************************
 *  Copyright (C) 2010 by Alex Fiestas <alex@eyeos.org>                              *
 *  Copyright (C) 2010 UFO Coders <info@ufocoders.com>                               *
 *                                                                                   *
 *  This program is free software; you can redistribute it and/or                    *
 *  modify it under the terms of the GNU General Public License                      *
 *  as published by the Free Software Foundation; either version 2                   *
 *  of the License, or (at your option) any later version.                           *
 *                                                                                   *
 *  This program is distributed in the hope that it will be useful,                  *
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of                   *
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                    *
 *  GNU General Public License for more details.                                     *
 *                                                                                   *
 *  You should have received a copy of the GNU General Public License                *
 *  along with this program; if not, write to the Free Software                      *
 *  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA   *
 *************************************************************************************/

#include "audio.h"
#include "audio_interface.h"

#include <QDBusConnection>

#include <KLocalizedString>
#include <KPluginFactory>
#include <KNotification>
#include <KIcon>

#include <bluedevil/bluedevildevice.h>

BLUEDEVILACTION_PLUGIN_EXPORT(AudioPlugin)

AudioPlugin::AudioPlugin(QObject* parent, const QVariantList& args)
    : ActionPlugin(parent)
{
    Q_UNUSED(args);
}

void AudioPlugin::startAction()
{
    OrgBluezAudioInterface *interface = new OrgBluezAudioInterface("org.bluez", device()->UBI(), QDBusConnection::systemBus());
    connect(interface, SIGNAL(PropertyChanged(QString,QDBusVariant)), this, SLOT(propertyChanged(QString,QDBusVariant)));

    interface->Connect();
    QTimer::singleShot(30 * 1000, this, SLOT(timeout()));
}

void AudioPlugin::timeout()
{
    KNotification::event(
        KNotification::Notification,
        i18n("%1: audio service connection timeout", device()->friendlyName()),
        KIcon(device()->icon()).pixmap(48,48)
    )->sendEvent();

    emit finished();
}

void AudioPlugin::propertyChanged(const QString &property, const QDBusVariant &value)
{
    if (property == "State") {
        if (value.variant().toString() == "connected") {
            KNotification::event(
                KNotification::Notification,
                i18n("%1: audio service connected and configured", device()->friendlyName()),
                KIcon(device()->icon()).pixmap(48,48)
            )->sendEvent();

            emit finished();
        }
    }
}
