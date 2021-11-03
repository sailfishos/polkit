Name:       polkit
Summary:    PolicyKit Authorization Framework
Version:    0.105
Release:    1
License:    LGPLv2+
URL:        http://www.freedesktop.org/wiki/Software/PolicyKit
Source0:    %{name}-%{version}.tar.gz
Source1:    polkit.service
Source2:    genpatchlist.sh
Source3:    patches/debian/series
Patch0000: patches/debian/0.106/agenthelper-pam-Fix-newline-trimming-code.patch
Patch0001: patches/debian/0.107/Try-harder-to-look-up-the-right-localization.patch
Patch0002: patches/debian/0.108/build-Fix-.gir-generation-for-parallel-make.patch
Patch0003: patches/debian/0.108/PolkitAgent-Avoid-crashing-if-initializing-the-server-obj.patch
Patch0004: patches/debian/0.110/07_set-XAUTHORITY-environment-variable-if-unset.patch
Patch0005: patches/debian/0.110/04_get_cwd.patch
Patch0006: patches/debian/0.111/09_pam_environment.patch
Patch0007: patches/debian/0.111/Add-a-FIXME-to-polkitprivate.h.patch
Patch0008: patches/debian/0.111/Fix-a-memory-leak.patch
Patch0009: patches/debian/0.112/00git_type_registration.patch
Patch0010: patches/debian/0.112/08_deprecate_racy_APIs.patch
Patch0011: patches/debian/0.112/cve-2013-4288.patch
Patch0012: patches/debian/0.114/polkitpermission-Fix-a-memory-leak-on-authority-changes.patch
Patch0013: patches/debian/0.113/Port-internals-non-deprecated-PolkitProcess-API-wher.patch
Patch0014: patches/debian/0.113/pkexec-Work-around-systemd-injecting-broken-XDG_RUNT.patch
Patch0015: patches/debian/0.113/03_PolkitAgentSession-fix-race-between-child-and-io-wat.patch
Patch0016: patches/debian/0.113/polkitd-Fix-problem-with-removing-non-existent-sourc.patch
Patch0017: patches/debian/0.113/PolkitSystemBusName-Add-public-API-to-retrieve-Unix-.patch
Patch0018: patches/debian/0.113/Fixed-compilation-problem-in-the-backend.patch
Patch0019: patches/debian/0.113/Don-t-discard-error-data-returned-by-polkit_system_b.patch
Patch0020: patches/debian/0.113/sessionmonitor-systemd-Deduplicate-code-paths.patch
Patch0021: patches/debian/0.113/PolkitSystemBusName-Retrieve-both-pid-and-uid.patch
Patch0022: patches/debian/0.113/sessionmonitor-systemd-prepare-for-D-Bus-user-bus-mo.patch
Patch0023: patches/debian/0.113/Refuse-duplicate-user-arguments-to-pkexec.patch
Patch0024: patches/debian/0.113/00git_fix_memleak.patch
Patch0025: patches/debian/0.113/00git_invalid_object_paths.patch
Patch0026: patches/debian/0.113/sessionmonitor-systemd-Use-sd_uid_get_state-to-check.patch
Patch0027: patches/debian/0.113/Fix-a-possible-NULL-dereference.patch
Patch0028: patches/debian/0.113/Remove-a-redundant-assignment.patch
Patch0029: patches/debian/0.113/Fix-duplicate-GError-use-when-uid-is-missing.patch
Patch0030: patches/debian/0.113/Fix-a-crash-when-two-authentication-requests-are-in-.patch
Patch0031: patches/debian/0.113/CVE-2015-4625-Use-unpredictable-cookie-values-keep-t.patch
Patch0032: patches/debian/0.113/CVE-2015-4625-Bind-use-of-cookies-to-specific-uids.patch
Patch0033: patches/debian/0.113/docs-Update-for-changes-to-uid-binding-Authenticatio.patch
Patch0034: patches/debian/0.113/Fix-a-per-authorization-memory-leak.patch
Patch0035: patches/debian/0.113/Fix-a-memory-leak-when-registering-an-authentication.patch
Patch0036: patches/debian/0.113/CVE-2015-3255-Fix-GHashTable-usage.patch
Patch0037: patches/debian/0.113/Fix-use-after-free-in-polkitagentsession.c.patch
Patch0038: patches/debian/0.113/README-Note-to-send-security-reports-via-DBus-s-mech.patch
Patch0039: patches/debian/0.114/Fix-multi-line-pam-text-info.patch
Patch0040: patches/debian/0.114/Refactor-send_to_helper-usage.patch
Patch0041: patches/debian/0.114/Add-gettext-support-for-.policy-files.patch
Patch0042: patches/debian/0.114/gettext-switch-to-default-translate-no.patch
Patch0043: patches/debian/0.114/Support-polkit-session-agent-running-outside-user-session.patch
Patch0044: patches/debian/0.115/Fix-CVE-2018-1116-Trusting-client-supplied-UID.patch
Patch0045: patches/debian/0.116/Possible-resource-leak-found-by-static-analyzer.patch
Patch0046: patches/debian/0.116/Elaborate-message-printed-by-polkit-when-disconnecting-fr.patch
Patch0047: patches/debian/0.116/Error-message-raised-on-every-systemctl-start-in-emergenc.patch
Patch0048: patches/debian/0.116/Fix-a-critical-warning-on-calling-polkit_permission_new_s.patch
Patch0049: patches/debian/0.116/Allow-negative-uids-gids-in-PolkitUnixUser-and-Group-obje.patch
Patch0050: patches/debian/0.116/tests-add-tests-for-high-uids.patch
Patch0051: patches/debian/0.116/backend-Compare-PolkitUnixProcess-uids-for-temporary-auth.patch
Patch0052: patches/debian/0.116/Allow-uid-of-1-for-a-PolkitUnixProcess.patch
Patch0053: patches/debian/0.116/pkttyagent-PolkitAgentTextListener-leaves-echo-tty-disabl.patch
Patch0054: patches/debian/02_gettext.patch
Patch0055: patches/debian/06_systemd-service.patch
Patch0056: patches/debian/10_build-against-libsystemd.patch
Patch0057: patches/debian/Move-D-Bus-policy-file-to-usr-share-dbus-1-system.d.patch
Patch0058: patches/debian/Statically-link-libpolkit-backend1-into-polkitd.patch
Patch0059: patches/debian/Remove-example-null-backend.patch
Patch0060: patches/debian/CVE-2021-3560.patch
Patch0061: patches/0001-dbus-Use-systemd-service.patch
Patch0062: patches/0002-build-Disable-gtk-doc-support.patch
Patch0063: patches/0003-Support-for-annotation-identity-group-check.patch
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
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/polkit.service

%find_lang polkit-1


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f polkit-1.lang
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/lib*.so.*
%dir %{_libdir}/polkit-1
%dir %{_libdir}/polkit-1/extensions
%{_datadir}/dbus-1/system-services/*
%dir %{_datadir}/polkit-1/
%dir %{_datadir}/polkit-1/actions
%{_datadir}/polkit-1/actions/org.freedesktop.policykit.policy
%config %{_datadir}/dbus-1/system.d/org.freedesktop.PolicyKit1.conf
%config %{_sysconfdir}/pam.d/polkit-1
%config %{_sysconfdir}/polkit-1
%{_bindir}/pkaction
%{_bindir}/pkcheck
%{_bindir}/pkttyagent

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
%{_unitdir}/polkit.service


%files devel
%defattr(-,root,root,-)
# >> files devel
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gettext/its/polkit.its
%{_datadir}/gettext/its/polkit.loc
%{_includedir}/*
%{_bindir}/pk-example-frobnicate
%{_datadir}/polkit-1/actions/org.freedesktop.policykit.examples.pkexec.policy
