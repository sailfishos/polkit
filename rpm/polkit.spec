Name:       polkit
Summary:    An Authorization Framework
Version:    125
Release:    1
License:    LGPLv2+
URL:        https://github.com/sailfishos/polkit
Source0:    %{name}-%{version}.tar.gz
Patch001:   0001-dbus-Use-systemd-service.patch
Patch002:   0002-Support-for-annotation-identity-group-check.patch
Patch003:   0003-Revert-to-old-systemd-variable-names.patch
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(expat)
BuildRequires: pkgconfig(duktape)
BuildRequires: pam-devel
BuildRequires: gettext-devel
BuildRequires: meson
Requires: dbus
Requires(pre): /usr/sbin/useradd
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
polkit is a toolkit for defining and handling authorizations.
It is used for allowing unprivileged processes to speak to privileged
processes.

%package devel
Summary:    Development files for polkit
Requires:   %{name} = %{version}-%{release}
Requires:   pkgconfig(glib-2.0)

%description devel
Development files for polkit.


%prep
%autosetup -p1 -n %{name}-%{version}/%{name}

%build
%meson -D authfw=pam \
       -D examples=false \
       -D gtk_doc=false \
       -D introspection=false \
       -D man=false \
       -D session_tracking=logind \
       -D tests=false

%meson_build

%install
%meson_install

%find_lang polkit-1

%pre
getent group polkitd >/dev/null 2>&1 || groupadd -r polkitd || :
getent passwd polkitd >/dev/null 2>&1 || /usr/sbin/useradd -r -g polkitd -s /sbin/nologin -c 'User for polkitd' -d '/' polkitd || :

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f polkit-1.lang
%license COPYING
%{_libdir}/lib*.so.*
%{_datadir}/dbus-1/system-services/*
%dir %{_datadir}/polkit-1/
%dir %{_datadir}/polkit-1/actions
%{_datadir}/polkit-1/actions/org.freedesktop.policykit.policy
%config %{_datadir}/dbus-1/system.d/org.freedesktop.PolicyKit1.conf
%{_datadir}/polkit-1/rules.d/50-default.rules
%attr(0750,root,polkitd) %dir %{_sysconfdir}/polkit-1/rules.d
%{_sysusersdir}/polkit.conf
%{_prefix}/lib/pam.d/polkit-1
%config %{_sysconfdir}/polkit-1
%{_datadir}/polkit-1/policyconfig-1.dtd
%{_tmpfilesdir}/polkit-tmpfiles.conf

%{_bindir}/pkaction
%{_bindir}/pkcheck
%{_bindir}/pkttyagent
%{_prefix}/lib/polkit-1/polkitd
# see upstream docs for why these permissions are necessary
%attr(4755,root,root) %{_bindir}/pkexec
%attr(4755,root,root) %{_prefix}/lib/polkit-1/polkit-agent-helper-1
%{_unitdir}/polkit.service

%files devel
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gettext/its/polkit.its
%{_datadir}/gettext/its/polkit.loc
%{_includedir}/*
