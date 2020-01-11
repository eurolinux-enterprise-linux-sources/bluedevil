
Name:           bluedevil
Summary:        Bluetooth stack for KDE
Version:        1.3
Release:        4%{?dist}

License:        GPLv2+
URL:            https://projects.kde.org/projects/extragear/base/bluedevil
Source0:        http://download.kde.org/%{?pre:un}stable/bluedevil/%{version}%{?pre:-%{pre}}/src/bluedevil-%{version}%{?pre:-%{pre}}.tar.bz2
# support (or not) same arch's that obexd does
ExcludeArch:    s390 s390x

## upstream patches

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  kdelibs4-devel
BuildRequires:  libbluedevil-devel

Provides:       dbus-bluez-pin-helper

Obsoletes:      kbluetooth < 0.4.2-3

# not sure if just kdelibs is enough -- Rex
Requires:       kde-runtime%{?_kde4_version: >= %{_kde4_version}}

## Runtime requirements for file transfers, as per README:
Requires:       obex-data-server
# This package contains the obexd client only, which is all we want:
Requires:       obexd
# (The obexd server conflicts with obex-data-server and is disabled in Fedora.)

Requires:       pulseaudio-module-bluetooth


%description
BlueDevil is the bluetooth stack for KDE.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    devel
%{summary}.


%prep
%setup -q -n %{name}-%{version}%{?pre:-%{pre}}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang %{name} --with-kde


%check
# FIXME: .desktop files need some mime/Categories love to validate properly -- Rex
for desktop_file in %{buildroot}%{_kde4_datadir}/applications/kde4/*.desktop ; do
desktop-file-validate ${desktop_file} ||:
done


%postun
if [ $1 -eq 0 ] ; then
    update-desktop-database -q &> /dev/null
    update-mime-database %{_kde4_datadir}/mime &> /dev/null
fi

%posttrans
update-desktop-database -q &> /dev/null
update-mime-database %{_kde4_datadir}/mime >& /dev/null

%files -f %{name}.lang
%doc README
%{_kde4_appsdir}/bluedevil/
%{_kde4_appsdir}/bluedevilwizard/

%{_kde4_bindir}/bluedevil-audio
%{_kde4_bindir}/bluedevil-helper
%{_kde4_bindir}/bluedevil-input
%{_kde4_bindir}/bluedevil-monolithic
%{_kde4_bindir}/bluedevil-network-dun
%{_kde4_bindir}/bluedevil-network-panu
%{_kde4_bindir}/bluedevil-sendfile
%{_kde4_bindir}/bluedevil-wizard
%{_kde4_datadir}/applications/kde4/*.desktop
%{_datadir}/dbus-1/services/*.service
%{_kde4_datadir}/kde4/services/*
%{_kde4_datadir}/kde4/servicetypes/actionplugin.desktop
%{_kde4_datadir}/mime/packages/bluedevil-mime.xml
%{_kde4_libdir}/kde4/*
%{_kde4_libdir}/libbluedevilaction.so
%{_kde4_libexecdir}/bluedevil-authorize
%{_kde4_libexecdir}/bluedevil-confirmmodechange
%{_kde4_libexecdir}/bluedevil-requestconfirmation
%{_kde4_libexecdir}/bluedevil-requestpin

%files devel
%doc HACKING
%{_includedir}/actionplugin.h


%changelog
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
