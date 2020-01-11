
Name:           bluedevil
Summary:        Bluetooth stack for KDE
Version:        2.1
Release:        1%{?dist}

License:        GPLv2+
URL:            https://projects.kde.org/projects/extragear/base/bluedevil
%if 0%{?snap:1}
Source0:        bluedevil-%{version}-%{git_short}.tar.xz
%else
Source0:        http://download.kde.org/%{?pre:un}stable/bluedevil/%{version}%{?pre:-%{pre}}/src/bluedevil-%{version}%{?pre:-%{pre}}.tar.xz
%endif
# support (or not) same arch's that obexd does
ExcludeArch:    s390 s390x

## upstream patches
Patch2: 0002-KCM-SystemCheck-Add-NoUsableAdapter-error.patch
Patch4: 0004-obexftpdaemon-session-method-now-takes-target-parame.patch
Patch5: 0005-kio_obexftp-Prefer-pcsuite-target-for-S60-devices.patch
Patch7: 0007-wizard-Add-Success-page.patch
Patch17: 0017-filereceiver-Fix-crash-when-sending-device-is-null.patch
Patch18: 0018-kio_obexftp-Fix-finished-called-twice-in-get.patch
Patch21: 0021-daemon-Don-t-try-to-infinitely-kill-monolithic-when-.patch

BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  kdelibs4-devel
BuildRequires:  libbluedevil-devel >= %{version}

Provides:       dbus-bluez-pin-helper

Obsoletes:      kbluetooth < 0.4.2-3
Obsoletes:      bluedevil-devel < 2.0.0-0.10

Requires:       kde-runtime
Requires:       libbluedevil%{?_isa} >= %{version}
Requires:       pulseaudio-module-bluetooth


%description
BlueDevil is the bluetooth stack for KDE.

%package autostart
Summary: Autostart support for non-KDE desktops
Requires: %{name} = %{version}-%{release}
%description autostart
%{summary}.


%prep
%autosetup -n %{name}-%{version}%{?pre:-%{pre}} -p1


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang %{name} --with-kde

desktop-file-install \
  --dir=%{buildroot}%{_sysconfdir}/xdg/autostart/ \
  --add-not-show-in=KDE \
  %{buildroot}%{_kde4_datadir}/applications/kde4/bluedevil-monolithic.desktop


%check
desktop-file-validate %{buildroot}%{_kde4_datadir}/applications/kde4/bluedevil-monolithic.desktop
desktop-file-validate %{buildroot}%{_kde4_datadir}/applications/kde4/bluedevil-sendfile.desktop
desktop-file-validate %{buildroot}%{_kde4_datadir}/applications/kde4/bluedevil-wizard.desktop

%post
touch --no-create %{_kde4_datadir}/mime/packages &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    update-desktop-database -q &> /dev/null
    touch --no-create %{_kde4_datadir}/mime/packages &> /dev/null || :
    update-mime-database %{?fedora:-n} %{_kde4_datadir}/mime &> /dev/null || :
fi

%posttrans
update-desktop-database -q &> /dev/null
update-mime-database %{_kde4_datadir}/mime &> /dev/null || :

%files -f %{name}.lang
%doc README
%{_kde4_appsdir}/bluedevil/
%{_kde4_appsdir}/bluedevilwizard/


%{_kde4_bindir}/bluedevil-monolithic
%{_kde4_bindir}/bluedevil-sendfile
%{_kde4_bindir}/bluedevil-wizard
%{_kde4_datadir}/applications/kde4/bluedevil-monolithic.desktop
%{_kde4_datadir}/applications/kde4/bluedevil-sendfile.desktop
%{_kde4_datadir}/applications/kde4/bluedevil-wizard.desktop
%{_kde4_datadir}/kde4/services/bluedevil*.desktop
%{_kde4_datadir}/kde4/services/*.protocol
%{_kde4_datadir}/kde4/services/kded/*.desktop
%{_kde4_datadir}/mime/packages/bluedevil-mime.xml
%{_kde4_libdir}/kde4/*.so
%{_kde4_libexecdir}/bluedevil-authorize
%{_kde4_libexecdir}/bluedevil-confirmmodechange
%{_kde4_libexecdir}/bluedevil-requestconfirmation
%{_kde4_libexecdir}/bluedevil-requestpin

%files autostart
%{_sysconfdir}/xdg/autostart/bluedevil-monolithic.desktop


%changelog
* Mon May 25 2015 Jan Grulich <jgrulich@redhat.com> 2-1-1
- Re-base to 2.1 (sync with F21)

* Fri May 08 2015 Ray Strode <rstrode@redhat.com> 1.3-5
- Rebuild against bluez5.  This won't work, but will
  at least prevent broken dependencies
  Related: #1174545 1219504

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.3-4
- Mass rebuild 2013-12-27

* Wed Jun 19 2013 Rex Dieter <rdieter@fedoraproject.org> 1.3-3
- ExcludeArch: s390 s390x (#975736)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 31 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3-1
- 1.3

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-0.6.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 30 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3-0.5.rc2
- include translations (copied from -rc1)

* Sun Apr 29 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3-0.4.rc2
- update to 1.3-rc2

* Wed Apr 25 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3-0.3.rc1
- kde daemon crash (kde#284052)

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-0.2.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 03 2011 Jaroslav Reznik <jreznik@redhat.com> - 1.3-0.1.rc1
- update to 1.3-rc1

* Mon Oct 10 2011 Jaroslav Reznik <jreznik@redhat.com> - 1.2.2-1
- update to 1.2.2

* Tue Sep 13 2011 Jaroslav Reznik <jreznik@redhat.com> - 1.2-1
- update to 1.2 final

* Mon Sep 05 2011 Jaroslav Reznik <jreznik@redhat.com> - 1.2-0.2.rc2
- update to 1.2-rc2

* Fri Aug 19 2011 Jaroslav Reznik <jreznik@redhat.com> - 1.2-0.1.rc1
- update to 1.2-rc1

* Tue Jul 26 2011 Jaroslav Reznik <jreznik@redhat.com> - 1.1.1-1
- update to 1.1.1

* Mon May 02 2011 Jaroslav Reznik <jreznik@redhat.com> - 1.1-2
- rebuilt for libbluedevil 1.9 snapshot

* Fri Apr 15 2011 Jaroslav Reznik <jreznik@redhat.com> - 1.1-1
- update to 1.1
- add pulseaudio-module-bluetooth req

* Mon Mar 28 2011 Jaroslav Reznik <jreznik@redhat.com> - 1.0.3-1
- update to 1.0.3

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 02 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.0.2-2
- Requires: obex-data-server obexd (for file transfers)

* Wed Feb 02 2011 Lukas Tinkl <ltinkl@redhat.com> - 1.0.2-1
- 1.0.2 upstream version, fixes mainly for device pairing and obex crashes

* Tue Feb 01 2011 Rex Dieter <rdieter@fedoraproject.org> 1.0.1-3
- Requires: kdebase-runtime
- add scriptlets

* Sat Jan 29 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.0.1-2
- Provides: dbus-bluez-pin-helper (keeps blueman and hal off the KDE spin)
- fix kbluetooth Obsoletes to match 0.4.2-2.fc* properly

* Fri Jan 14 2011 Jaroslav Reznik <jreznik@redhat.com> 1.0.1-1
- update to 1.0.1

* Tue Nov 30 2010 Jaroslav Reznik <jreznik@redhat.com> 1.0-1
- update to 1.0 final

* Mon Sep 27 2010 Jaroslav Reznik <jreznik@redhat.com> 1.0-0.1.rc4.1
- update to rc4-1

* Thu Aug 19 2010 Jaroslav Reznik <jreznik@redhat.com> 1.0-0.1.rc3
- update to rc3

* Fri Aug 13 2010 Jaroslav Reznik <jreznik@redhat.com> 1.0-0.1.rc2
- initial package
