Name:       polkit
Summary:    PolicyKit Authorization Framework
Version:    0.105
Release:    1
License:    LGPLv2+
URL:        http://www.freedesktop.org/wiki/Software/PolicyKit
Source0:    %{name}-%{version}.tar.gz
Source1:    dbus-org.freedesktop.PolicyKit1.service
Patch0:     patches/debian/0.108/build-Fix-.gir-generation-for-parallel-make.patch
Patch1:     patches/debian/0.110/07_set-XAUTHORITY-environment-variable-if-unset.patch
Patch2:     patches/debian/0.110/04_get_cwd.patch
Patch3:     patches/debian/0.111/09_pam_environment.patch
Patch4:     patches/debian/0.112/00git_type_registration.patch
Patch5:     patches/debian/0.112/08_deprecate_racy_APIs.patch
Patch6:     patches/debian/0.112/cve-2013-4288.patch
Patch7:     patches/debian/0.113/Port-internals-non-deprecated-PolkitProcess-API-wher.patch
Patch8:     patches/debian/0.113/pkexec-Work-around-systemd-injecting-broken-XDG_RUNT.patch
Patch9:     patches/debian/0.113/03_PolkitAgentSession-fix-race-between-child-and-io-wat.patch
Patch10:    patches/debian/0.113/polkitd-Fix-problem-with-removing-non-existent-sourc.patch
Patch11:    patches/debian/0.113/PolkitSystemBusName-Add-public-API-to-retrieve-Unix-.patch
Patch12:    patches/debian/0.113/Fixed-compilation-problem-in-the-backend.patch
Patch13:    patches/debian/0.113/Don-t-discard-error-data-returned-by-polkit_system_b.patch
Patch14:    patches/debian/0.113/sessionmonitor-systemd-Deduplicate-code-paths.patch
Patch15:    patches/debian/0.113/sessionmonitor-systemd-prepare-for-D-Bus-user-bus-mo.patch
Patch16:    patches/debian/0.113/Refuse-duplicate-user-arguments-to-pkexec.patch
Patch17:    patches/debian/0.113/00git_fix_memleak.patch
Patch18:    patches/debian/0.113/00git_invalid_object_paths.patch
Patch19:    patches/debian/0.113/sessionmonitor-systemd-Use-sd_uid_get_state-to-check.patch
Patch20:    patches/debian/0.113/Fix-a-possible-NULL-dereference.patch
Patch21:    patches/debian/0.113/Fix-duplicate-GError-use-when-uid-is-missing.patch
Patch22:    patches/debian/0.113/Fix-a-crash-when-two-authentication-requests-are-in-.patch
Patch23:    patches/debian/0.113/CVE-2015-4625-Use-unpredictable-cookie-values-keep-t.patch
Patch24:    patches/debian/0.113/CVE-2015-4625-Bind-use-of-cookies-to-specific-uids.patch
Patch25:    patches/debian/0.113/docs-Update-for-changes-to-uid-binding-Authenticatio.patch
Patch26:    patches/debian/0.113/Fix-a-per-authorization-memory-leak.patch
Patch27:    patches/debian/0.113/Fix-a-memory-leak-when-registering-an-authentication.patch
Patch28:    patches/debian/0.113/CVE-2015-3255-Fix-GHashTable-usage.patch
Patch29:    patches/debian/0.113/Fix-use-after-free-in-polkitagentsession.c.patch
Patch30:    patches/debian/0.113/README-Note-to-send-security-reports-via-DBus-s-mech.patch
Patch31:    patches/debian/master/Fix-multi-line-pam-text-info.patch
Patch32:    patches/CVE-2018-1116.patch
Patch33:    patches/0001-dbus-Use-systemd-service.patch
Patch34:    patches/0002-build-Disable-gtk-doc-support.patch
Patch35:    patches/0003-Support-for-annotation-identity-group-check.patch
Patch36:    patches/0004-Fix-build-with-systemd-v233.patch
Requires:   dbus
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(expat)
BuildRequires:  pam-devel
BuildRequires:  intltool
BuildRequires:  libtool
BuildRequires:  gobject-introspection
BuildRequires:  gobject-introspection-devel


%description
PolicyKit is a toolkit for defining and handling authorizations.
It is used for allowing unprivileged processes to speak to privileged
processes.



%package devel
Summary:    Development files for PolicyKit
Requires:   %{name} = %{version}-%{release}
Requires:   pkgconfig(glib-2.0)

%description devel
Development files for PolicyKit.


%prep
%autosetup -p1 -n %{name}-%{version}/%{name}

%build
%autogen --disable-static \
         --disable-gtk-doc \
         --disable-man-pages \
         --libexecdir=%{_libexecdir}/polkit-1 \
         --disable-introspection \
         --enable-systemd=yes \
         --with-os-type=mer
# --with-os-type=mer is just some value for os type so it doesn't complain
# autogen.sh runs also configure

%make_build

%install
%make_install
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/dbus-org.freedesktop.PolicyKit1.service
%find_lang polkit-1


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f polkit-1.lang
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/lib*.so.*
%dir %{_libdir}/polkit-1
%dir %{_libdir}/polkit-1/extensions
%{_libdir}/polkit-1/extensions/*.so
%{_datadir}/dbus-1/system-services/*
%dir %{_datadir}/polkit-1/
%dir %{_datadir}/polkit-1/actions
%{_datadir}/polkit-1/actions/org.freedesktop.policykit.policy
%config %{_sysconfdir}/dbus-1/system.d/org.freedesktop.PolicyKit1.conf
%config %{_sysconfdir}/pam.d/polkit-1
%config %{_sysconfdir}/polkit-1
%{_bindir}/*
%{_libexecdir}/polkit-1/polkitd
# see upstream docs for why these permissions are necessary
%attr(4755,root,root) %{_bindir}/pkexec
%attr(4755,root,root) %{_libexecdir}/polkit-1/polkit-agent-helper-1
%attr(0700,root,root) %dir %{_sharedstatedir}/polkit-1/
%attr(0700,root,root) %dir %{_sharedstatedir}/polkit-1/localauthority
%dir %{_sharedstatedir}/polkit-1/localauthority/10-vendor.d
%dir %{_sharedstatedir}/polkit-1/localauthority/20-org.d
%dir %{_sharedstatedir}/polkit-1/localauthority/30-site.d
%dir %{_sharedstatedir}/polkit-1/localauthority/50-local.d
%dir %{_sharedstatedir}/polkit-1/localauthority/90-mandatory.d
%{_unitdir}/dbus-org.freedesktop.PolicyKit1.service


%files devel
%defattr(-,root,root,-)
# >> files devel
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_bindir}/pk-example-frobnicate
%{_datadir}/polkit-1/actions/org.freedesktop.policykit.examples.pkexec.policy
