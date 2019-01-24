Name:       polkit
Summary:    PolicyKit Authorization Framework
Version:    0.105
Release:    1
Group:      System/Libraries
License:    LGPLv2+
URL:        http://www.freedesktop.org/wiki/Software/PolicyKit
Source0:    %{name}-%{version}.tar.gz
Source1:    dbus-org.freedesktop.PolicyKit1.service
Patch0:     patches/0.108/build-Fix-.gir-generation-for-parallel-make.patch
Patch1:     patches/0.110/07_set-XAUTHORITY-environment-variable-if-unset.patch
Patch2:     patches/0.110/04_get_cwd.patch
Patch3:     patches/0.111/09_pam_environment.patch
Patch4:     patches/0.112/00git_type_registration.patch
Patch5:     patches/0.112/08_deprecate_racy_APIs.patch
Patch6:     patches/0.112/cve-2013-4288.patch
Patch7:     patches/0.113/Port-internals-non-deprecated-PolkitProcess-API-wher.patch
Patch8:     patches/0.113/pkexec-Work-around-systemd-injecting-broken-XDG_RUNT.patch
Patch9:     patches/0.113/03_PolkitAgentSession-fix-race-between-child-and-io-wat.patch
Patch10:    patches/0.113/polkitd-Fix-problem-with-removing-non-existent-sourc.patch
Patch11:    patches/0.113/PolkitSystemBusName-Add-public-API-to-retrieve-Unix-.patch
Patch12:    patches/0.113/Fixed-compilation-problem-in-the-backend.patch
Patch13:    patches/0.113/Don-t-discard-error-data-returned-by-polkit_system_b.patch
Patch14:    patches/0.113/sessionmonitor-systemd-Deduplicate-code-paths.patch
Patch15:    patches/0.113/sessionmonitor-systemd-prepare-for-D-Bus-user-bus-mo.patch
Patch16:    patches/0.113/Refuse-duplicate-user-arguments-to-pkexec.patch
Patch17:    patches/0.113/00git_fix_memleak.patch
Patch18:    patches/0.113/00git_invalid_object_paths.patch
Patch19:    patches/0.113/sessionmonitor-systemd-Use-sd_uid_get_state-to-check.patch
Patch20:    patches/0.113/Fix-a-possible-NULL-dereference.patch
Patch21:    patches/0.113/Fix-duplicate-GError-use-when-uid-is-missing.patch
Patch22:    patches/0.113/Fix-a-crash-when-two-authentication-requests-are-in-.patch
Patch23:    patches/0.113/CVE-2015-4625-Use-unpredictable-cookie-values-keep-t.patch
Patch24:    patches/0.113/CVE-2015-4625-Bind-use-of-cookies-to-specific-uids.patch
Patch25:    patches/0.113/docs-Update-for-changes-to-uid-binding-Authenticatio.patch
Patch26:    patches/0.113/Fix-a-per-authorization-memory-leak.patch
Patch27:    patches/0.113/Fix-a-memory-leak-when-registering-an-authentication.patch
Patch28:    patches/0.113/CVE-2015-3255-Fix-GHashTable-usage.patch
Patch29:    patches/0.113/Fix-use-after-free-in-polkitagentsession.c.patch
Patch30:    patches/0.113/README-Note-to-send-security-reports-via-DBus-s-mech.patch
Patch31:    patches/master/Fix-multi-line-pam-text-info.patch
Patch32:    patches/CVE-2018-1116.patch
Patch33:    patches/0001-dbus-Use-systemd-service.patch
Patch34:    patches/0002-build-Disable-gtk-doc-support.patch
Requires:   dbus
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libsystemd-login)
BuildRequires:  expat-devel
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
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   pkgconfig
Requires:   glib2-devel

%description devel
Development files for PolicyKit.


%prep
%setup -q -n %{name}-%{version}/%{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1

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

make %{?_smp_mflags}

%install
%make_install
install -D -m 644 %{SOURCE1} %{buildroot}/%{_lib}/systemd/system/dbus-org.freedesktop.PolicyKit1.service
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
/%{_lib}/systemd/system/dbus-org.freedesktop.PolicyKit1.service


%files devel
%defattr(-,root,root,-)
# >> files devel
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_bindir}/pk-example-frobnicate
%{_datadir}/polkit-1/actions/org.freedesktop.policykit.examples.pkexec.policy
