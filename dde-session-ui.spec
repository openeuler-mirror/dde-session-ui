Name:           dde-session-ui
Version:        5.4.35.2
Release:        1
Summary:        Deepin desktop-environment - Session UI module
License:        GPLv3
URL:            https://github.com/linuxdeepin/%{name}
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        vendor.tar.gz

Patch0:         0001-Fix-wm-chooser-error-in-openeuler.patch

BuildRequires:  gcc-c++
BuildRequires:  deepin-gettext-tools
BuildRequires:  pkgconfig(dtkwidget) >= 5.1
BuildRequires:  pkgconfig(dframeworkdbus)
BuildRequires:  pkgconfig(gsettings-qt)
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(xcb-ewmh)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(xext)
BuildRequires:  qt5-devel
BuildRequires:  dtkcore-devel >= 5.1
BuildRequires:  dde-dock-devel
Requires:       dde-daemon
Requires:       startdde

Requires:       lightdm
Requires(post): sed
Provides:       lightdm-deepin-greeter = %{version}-%{release}
Provides:       lightdm-greeter = 1.2
Provides:       deepin-notifications = %{version}-%{release}
Obsoletes:      deepin-notifications < %{version}-%{release}

%description
This project include those sub-project:

- dde-shutdown: User interface of shutdown.
- dde-lock: User interface of lock screen.
- dde-lockservice: The back-end service of locking screen.
- lightdm-deepin-greeter: The user interface when you login in.
- dde-switchtogreeter: The tools to switch the user to login in.
- dde-lowpower: The user interface of reminding low power.
- dde-osd: User interface of on-screen display.
- dde-hotzone: User interface of setting hot zone.

%prep
%autosetup -p1
sed -i 's|default_background.jpg|default.png|' widgets/fullscreenbackground.cpp
sed -i 's|lib|libexec|' \
    misc/applications/deepin-toggle-desktop.desktop* \
    dde-osd/dde-osd_autostart.desktop \
    dde-osd/com.deepin.dde.osd.service \
    dde-osd/notification/files/com.deepin.dde.*.service* \
    dde-osd/dde-osd.pro \
    dde-welcome/com.deepin.dde.welcome.service \
    dde-welcome/dde-welcome.pro \
    dde-bluetooth-dialog/dde-bluetooth-dialog.pro \
    dde-touchscreen-dialog/dde-touchscreen-dialog.pro \
    dde-warning-dialog/com.deepin.dde.WarningDialog.service \
    dde-warning-dialog/dde-warning-dialog.pro \
    dde-suspend-dialog/dde-suspend-dialog.pro \
    dnetwork-secret-dialog/dnetwork-secret-dialog.pro \
    dde-lowpower/dde-lowpower.pro
sed -i 's|/usr/lib/dde-dock|/usr/lib64/dde-dock|' dde-notification-plugin/notifications/notifications.pro

tar -xf %{SOURCE1}

%build
export GOPATH=%{_builddir}/%{name}-%{version}/vendor:$GOPATH
export PATH=%{_qt5_bindir}:$PATH
%qmake_qt5 PREFIX=%{_prefix} PKGTYPE=rpm
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%post
sed -i "s|#greeter-session.*|greeter-session=lightdm-deepin-greeter|g" /etc/lightdm/lightdm.conf

%files
%doc README.md
%license LICENSE
%{_bindir}/dde-*
%{_bindir}/dmemory-warning-dialog
%{_libexecdir}/deepin-daemon/*
%{_datadir}/%{name}/
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/dbus-1/services/*.service
%{_libdir}/dde-dock/plugins/libnotifications.so
%{_prefix}/share/glib-2.0/schemas/com.deepin.dde.dock.module.notifications.gschema.xml

%changelog
* Thu Mar 30 2023 liweiganga <liweiganga@uniontech.com> - 5.4.35.2-1
- update: update to 5.4.35.2

* Mon Jul 18 2022 konglidong <konglidong@uniontech.com> - 5.4.24.2-1
- Update to 5.4.24.2

* Thu Sep 23 2021 weidong <weidong@uniontech.com> - 5.3.0.11-2
- Fix wm-chooser error in openeuler

* Tue Jul 20 2021 weidong <weidong@uniontech.com> - 5.3.0.11-1
- Update 5.3.0.11

* Tue Aug 18 2020 chenbo pan <panchenbo@uniontech.com> - 5.1.0.11-3
- remove golang devel

* Thu Jul 30 2020 openEuler Buildteam <buildteam@openeuler.org> - 5.1.0.11-2
- Package init
