Name:       polkit

Summary:    polkit Authorization Manager
Version:    0.112
Release:    1
Group:      System/Libraries
License:    LGPLv2+
URL:        http://www.freedesktop.org/wiki/Software/polkit/
Source:     http://www.freedesktop.org/software/polkit/releases/%{name}-%{version}.tar.gz
Requires:   dbus
Requires:   systemd
Requires(preun): systemd
Requires(post): /sbin/ldconfig
Requires(post): systemd
Requires(postun): /sbin/ldconfig
Requires(postun): systemd
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libsystemd-login)
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(mozjs-17.0)
BuildRequires:  pam-devel
BuildRequires:  intltool

%description
polkit is an application-level toolkit for defining and handling the policy
that allows unprivileged processes to speak to privileged processes: It is
a framework for centralizing the decision making process with respect to
granting access to privileged operations for unprivileged applications.


%package devel
Summary:    Development files for polkit
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   %name = %{version}-%{release}
Requires:   pkgconfig
Requires:   glib2-devel

%description devel
Development files for polkit.

%prep
%setup -q -n %{name}-%{version}

%build
%configure --disable-static \
    --disable-gtk-doc \
    --disable-man-pages \
    --disable-examples \
    --disable-introspection \
    --enable-libsystemd-login=yes \
    --enable-systemd=yes

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install
%find_lang polkit-1

%preun
if [ "$1" -eq 0 ]; then
systemctl stop polkit.service
fi

%pre
# Make sure user and group "polkitd" exist
getent group polkitd >/dev/null || groupadd -r polkitd
getent passwd polkitd >/dev/null || useradd -r -g polkitd -d / -s /sbin/nologin -c "User for polkitd" polkitd

%post
/sbin/ldconfig
systemctl daemon-reload
systemctl reload-or-try-restart polkit.service

%postun
/sbin/ldconfig
systemctl daemon-reload

%files -f polkit-1.lang
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/lib*.so.*
%dir %{_libdir}/polkit-1
%{_datadir}/dbus-1/system-services/*
%dir %{_datadir}/polkit-1/
%dir %{_datadir}/polkit-1/actions
%{_datadir}/polkit-1/actions/org.freedesktop.policykit.policy
%config %{_sysconfdir}/dbus-1/system.d/org.freedesktop.PolicyKit1.conf
%config %{_sysconfdir}/pam.d/polkit-1
%{_bindir}/pkaction
%{_bindir}/pkcheck
%{_bindir}/pkttyagent
%{_libdir}/polkit-1/polkitd
%{_sysconfdir}/polkit-1/rules.d/50-default.rules
/lib/systemd/system/polkit.service
# see upstream docs for why these permissions are necessary
%attr(4755,root,root) %{_bindir}/pkexec
%attr(4755,root,root) %{_libdir}/polkit-1/polkit-agent-helper-1
%attr(0700,polkitd,root) %config %dir %{_sysconfdir}/polkit-1/rules.d
%attr(0700,polkitd,root) %dir %{_datadir}/polkit-1/rules.d

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
