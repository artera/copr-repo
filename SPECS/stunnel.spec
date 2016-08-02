%if 0%{?rhel} < 7
%bcond_with init_systemd
%bcond_without init_sysv
%else
%bcond_with init_sysv
%bcond_without init_systemd
%endif

Summary: An SSL-encrypting socket wrapper
Name: stunnel
Version: 5.35
Release: 1%{?dist}
License: GPLv2
Group: Applications/Internet
URL: http://www.stunnel.org/
Source0: https://www.stunnel.org/downloads/stunnel-%{version}.tar.gz
Source1: https://www.stunnel.org/downloads/stunnel-%{version}.tar.gz.asc
Source7: https://www.stunnel.org/downloads/stunnel-%{version}.tar.gz.sha256
Buildroot: %{_tmppath}/stunnel-root
# util-linux is needed for rename
BuildRequires: openssl-devel, pkgconfig, tcp_wrappers-devel, util-linux
# for /usr/bin/pod2man
%if 0%{?fedora} > 18 || 0%{?rhel} >= 7
BuildRequires: perl-podlators
%endif

%{?with_init_systemd:BuildRequires: systemd-devel}
%if %{with init_systemd}
%{?systemd_requires: %systemd_requires}
%endif

%description
Stunnel is a socket wrapper which can provide SSL (Secure Sockets
Layer) support to ordinary applications. For example, it can be used
in conjunction with imapd to create an SSL secure IMAP server.

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS -fPIC"; export CFLAGS
if pkg-config openssl ; then
	CFLAGS="$CFLAGS `pkg-config --cflags openssl`";
	LDFLAGS="`pkg-config --libs-only-L openssl`"; export LDFLAGS
fi
%configure --enable-fips --enable-ipv6 \
	CPPFLAGS="-UPIDFILE -DPIDFILE='\"%{_localstatedir}/run/stunnel.pid\"'"
make LDADD="-pie -Wl,-z,defs,-z,relro,-z,now"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/stunnel
touch $RPM_BUILD_ROOT%{_sysconfdir}/stunnel/stunnel.pem
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/%{_mandir}/man8/*.pl.8*
install -Dm644 tools/stunnel.service $RPM_BUILD_ROOT/usr/lib/systemd/system/%{name}.service

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS BUGS ChangeLog COPY* CREDITS PORTS README TODO
%doc tools/stunnel.conf-sample
%lang(en) %doc doc/en/*
%{_bindir}/stunnel
%exclude %{_bindir}/stunnel3
%exclude %{_datadir}/doc/stunnel
%{_libdir}/stunnel
%exclude %{_libdir}/stunnel/libstunnel.la
%{_mandir}/man8/stunnel.8*
%dir %{_sysconfdir}/%{name}
%exclude %{_sysconfdir}/stunnel/*
/usr/lib/systemd/system/%{name}.service

%post
%if %{with init_systemd}
%systemd_post %{name}.service
%endif

%postun
%if %{with init_systemd}
%systemd_postun
%endif

%preun
%if %{with init_systemd}
%systemd_preun %{name}.service
%endif

%changelog
* Mon May 16 2016 Massimiliano Torromeo <massimiliano.torromeo@gmail.com> - 5.32-\
- Updated to latest upstream release

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 4.56-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 4.56-3
- Mass rebuild 2013-12-27

* Mon Aug 5 2013 Avesh Agarwal <avagarwa@redhat.com> - 4.56-2
- Ftp mirrors for NA does not work, so changing source code
  URLs to the correct ones.

* Mon Aug 5 2013 Avesh Agarwal <avagarwa@redhat.com> - 4.56-1
- New upstream realease 4.56.
- Updated local patches.
- Fixed upstream URL in spec file.
- Sourced URL of sha256 hash file in spec file.

* Tue Mar 26 2013 Avesh Agarwal <avagarwa@redhat.com> - 4.55-2
- Resolves: 927841

* Mon Mar 4 2013 Avesh Agarwal <avagarwa@redhat.com> - 4.55-1
- New upstream realease 4.55
- Updated local patches
- enabled fips mode
- Fixed for pod2man as it build-requires perl-podlators

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.54-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 10 2012 Avesh Agarwal <avagarwa@redhat.com> - 4.54-2
- 884183: support for full relro.

* Tue Oct 16 2012 Avesh Agarwal <avagarwa@redhat.com> - 4.54-1
- New upstream realease 4.54
- Updated local patches

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.53-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 14 2012 Avesh Agarwal <avagarwa@redhat.com> - 4.53-1
- New upstream realease 4.53
- Updated local patches

* Tue Mar 6 2012 Avesh Agarwal <avagarwa@redhat.com> - 4.52-1
- New upstream realease 4.52
- Updated local patches

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.50-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jan 3 2012 Avesh Agarwal <avagarwa@redhat.com> - 4.50-1
- New upstream realease 4.50
- Updated local patches

* Tue Sep 20 2011 Avesh Agarwal <avagarwa@redhat.com> - 4.44-1
- New upstream realease 4.44
- Updated local patches

* Fri Aug 19 2011 Avesh Agarwal <avagarwa@redhat.com> - 4.42-1
- New upstream realease 4.42
- Updated local patches
- Fixes #732069

* Mon Aug 1 2011 Avesh Agarwal <avagarwa@redhat.com> - 4.41-1
- New upstream realease 4.41
- Updated local patches to match the new release

* Tue Jun 28 2011 Avesh Agarwal <avagarwa@redhat.com> - 4.37-1
- New upstream realease 4.37
- Updated local patches to match the new release

* Mon Apr 4 2011 Avesh Agarwal <avagarwa@redhat.com> - 4.35-1
- New upstream realease 4.35
- Updated authpriv and sample patches to match the new release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 4 2010 Avesh Agarwal <avagarwa@redhat.com> - 4.34-1
- New upstream realease 4.34
- Updated authpriv and sample patches to match the new release

* Wed Apr 7 2010 Avesh Agarwal <avagarwa@redhat.com> - 4.33-1
- New upstream realease 4.33
- Updated authpriv and sample patches to match the new release
- Addresses bz 580117 (inted mode support issue)

* Mon Mar 29 2010 Avesh Agarwal <avagarwa@redhat.com> - 4.32-1
- New upstream realease 4.32
- Updated authpriv and sample patches to match the new release

* Tue Feb 16 2010 Avesh Agarwal <avagarwa@redhat.com> - 4.31-1
- New upstream realease 4.31
- Updated authpriv and sample patches to match the new release

* Tue Jan 26 2010 Avesh Agarwal <avagarwa@redhat.com> - 4.30-1
- New upstream realease 4.30
- Updated authpriv and sample patches for the new release

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 4.27-5
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May  3 2009 Miloslav Trmač <mitr@redhat.com> - 4.27-3
- Fix the previous patch.

* Wed Apr 29 2009 Miloslav Trmač <mitr@redhat.com> - 4.27-2
- Avoid aliasing undefined by ISO C

* Thu Apr 16 2009 Miloslav Trmač <mitr@redhat.com> - 4.27-1
- Update to stunnel-4.27.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 18 2009 Tomas Mraz <tmraz@redhat.com> - 4.26-2
- disable openssl upstream fips mode

* Mon Sep 22 2008 Miloslav Trmač <mitr@redhat.com> - 4.26-1
- Update to stunnel-4.26.

* Sun Jun  8 2008 Miloslav Trmač <mitr@redhat.com> - 4.25-2
- Use a clearer error message if the service name is unknown in "accept"
  Resolves: #450344

* Mon Jun  2 2008 Miloslav Trmač <mitr@redhat.com> - 4.25-1
- Update to stunnel-4.25

* Tue May 20 2008 Miloslav Trmač <mitr@redhat.com> - 4.24-2
- Drop stunnel3
  Resolves: #442842

* Mon May 19 2008 Miloslav Trmač <mitr@redhat.com> - 4.24-1
- Update to stunnel-4.24

* Fri Mar 28 2008 Miloslav Trmač <mitr@redhat.com> - 4.22-1
- Update to stunnel-4.22

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.20-6
- Autorebuild for GCC 4.3

* Tue Dec  4 2007 Miloslav Trmač <mitr@redhat.com> - 4.20-5
- Rebuild with openssl-0.9.8g

* Tue Oct 16 2007 Miloslav Trmač <mitr@redhat.com> - 4.20-4
- Revert the port to NSS, wait for NSS-based stunnel 5.x instead
  Resolves: #301971
- Mark localized man pages with %%lang (patch by Ville Skyttä)
  Resolves: #322281

* Tue Aug 28 2007 Miloslav Trmač <mitr@redhat.com> - 4.20-3.nss
- Port to NSS

* Mon Dec  4 2006 Miloslav Trmac <mitr@redhat.com> - 4.20-2
- Update BuildRequires for the separate tcp_wrappers-devel package

* Thu Nov 30 2006 Miloslav Trmac <mitr@redhat.com> - 4.20-1
- Update to stunnel-4.20

* Sat Nov 11 2006 Miloslav Trmac <mitr@redhat.com> - 4.19-1
- Update to stunnel-4.19

* Wed Oct 25 2006 Miloslav Trmac <mitr@redhat.com> - 4.18-1
- Update to stunnel-4.18
- Remove unused stunnel.cnf from the src.rpm
- Fix some rpmlint warnings

* Fri Aug 18 2006 Jesse Keating <jkeating@redhat.com> - 4.15-2
- rebuilt with latest binutils to pick up 64K -z commonpagesize on ppc*
  (#203001)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 4.15-1.1
- rebuild

* Sat Mar 18 2006 Miloslav Trmac <mitr@redhat.com> - 4.15-1
- Update to stunnel-4.15

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.14-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.14-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Miloslav Trmac <mitr@redhat.com> - 4.14-3
- Use pthread threading to fix crash on x86_64 (#179236)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov  9 2005 Miloslav Trmac <mitr@redhat.com> - 4.14-2
- Rebuild with newer openssl

* Thu Nov  3 2005 Miloslav Trmac <mitr@redhat.com> - 4.14-1
- Update to stunnel-4.14
- Override changed default pid file location, keep it in %%{_localstatedir}/run

* Sat Oct 22 2005 Miloslav Trmac <mitr@redhat.com> - 4.13-1
- Update to stunnel-4.13

* Fri Sep 30 2005 Miloslav Trmac <mitr@redhat.com> - 4.12-1
- Update to stunnel-4.12

* Thu Sep 22 2005 Miloslav Trmac <mitr@redhat.com> - 4.11-2
- Enable IPv6 (#169050, patch by Peter Bieringer)
- Don't ship another copy of man pages in HTML

* Tue Jul 12 2005 Miloslav Trmac <mitr@redhat.com> - 4.11-1
- Update to stunnel-4.11
- Fix int/size_t mismatches in stack_info ()
- Update Certificate-Creation for /etc/pki

* Wed Jun  1 2005 Miloslav Trmac <mitr@redhat.com> - 4.10-2
- Fix inetd mode
- Remove unnecessary Requires: and BuildRequires:
- Clean up the spec file

* Tue Apr 26 2005 Nalin Dahyabhai <nalin@redhat.com> 4.10-1
- update to 4.10

* Tue Apr 26 2005 Nalin Dahyabhai <nalin@redhat.com> 4.08-2
- add buildprereqs on libtool, util-linux; change textutils/fileutils dep to
  coreutils (#133961)

* Wed Mar 16 2005 Nalin Dahyabhai <nalin@redhat.com> 4.08-1
- update to 4.08
- build stunnel as a PIE binary

* Mon Nov 22 2004 Miloslav Trmac <mitr@redhat.com> - 4.05-4
- Convert man pages to UTF-8

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 27 2004 Nalin Dahyabhai <nalin@redhat.com> 4.05-2
- move the sample configuration to %%doc, it shouldn't be used as-is (#124373)

* Thu Mar 11 2004 Nalin Dahyabhai <nalin@redhat.com> 4.05-1
- update to 4.05

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Aug  7 2003 Elliot Lee <sopwith@redhat.com> 4.04-6
- Fix libtool

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Mar 21 2003 Nalin Dahyabhai <nalin@redhat.com> 4.04-4
- fix xinetd configuration samples

* Mon Feb 10 2003 Nalin Dahyabhai <nalin@redhat.com> 4.04-3
- rebuild

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 15 2003 Nalin Dahyabhai <nalin@redhat.com> 4.04-1
- update to 4.04

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 4.03-1
- use pkgconfig for information about openssl, if available

* Fri Jan  3 2003 Nalin Dahyabhai <nalin@redhat.com>
- update to 4.03

* Mon Oct 21 2002 Nalin Dahyabhai <nalin@redhat.com> 4.02-1
- update to 4.02

* Fri Oct  4 2002 Nalin Dahyabhai <nalin@redhat.com> 4.00-1
- don't create a dummy cert

* Wed Sep 25 2002 Nalin Dahyabhai <nalin@redhat.com>
- update to 4.00
- remove textutils and fileutils as buildreqs, add automake/autoconf

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri May 17 2002 Nalin Dahyabhai <nalin@redhat.com> 3.22-2
- rebuild in new environment

* Wed Jan  2 2002 Nalin Dahyabhai <nalin@redhat.com> 3.22-1
- update to 3.22, correcting a format-string vulnerability

* Wed Oct 31 2001 Nalin Dahyabhai <nalin@redhat.com> 3.21a-1
- update to 3.21a

* Tue Aug 28 2001 Nalin Dahyabhai <nalin@redhat.com> 3.20-1
- log using LOG_AUTHPRIV facility by default (#47289)
- make permissions on stunnel binary 0755
- implicitly trust certificates in %%{_datadir}/ssl/trusted (#24034)

* Fri Aug 10 2001 Nalin Dahyabhai <nalin@redhat.com> 3.19-1
- update to 3.19 to avoid problems with stunnel being multithreaded, but
  tcp wrappers not being thrad-safe

* Mon Jul 30 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.17

* Mon Jul 23 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.16

* Mon Jul 16 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.15
- enable tcp-wrappers support

* Tue May 29 2001 Nalin Dahyabhai <nalin@redhat.com>
- remove explicit requirement on openssl (specific version isn't enough,
  we have to depend on shared library version anyway)

* Fri Apr 27 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.14

* Mon Mar 26 2001 Preston Brown <pbrown@redhat.com>
- depend on make (#33148)

* Fri Mar  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Tue Feb  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.13 to get pthread, OOB, 64-bit fixes
- don't need sdf any more

* Thu Dec 28 2000 Nalin Dahyabhai <nalin@redhat.com>
- pull in sdf to build the man page (#22892)

* Fri Dec 22 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.11
- chuck the SIGHUP patch (went upstream)
- chuck parts of the 64-bit clean patch (went upstream)

* Thu Dec 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.10
- more 64-bit clean changes, hopefully the last bunch

* Wed Dec 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- change piddir from the default /var/stunnel to /var/run
- clean out pid file on SIGHUP

* Fri Dec 15 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.9 to get a security fix

* Wed Oct 25 2000 Matt Wilson <msw@redhat.com>
- change all unsigned longs to u_int32_t when dealing with network
  addresses

* Fri Aug 18 2000 Nalin Dahyabhai <nalin@redhat.com>
- make stunnel.pem also be (missingok)

* Thu Jun 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- move to Applications/Internet group
- clean up %%post script
- make stunnel.pem %%ghost %%config(noreplace)
- provide a sample file for use with xinetd

* Thu Jun  8 2000 Nalin Dahyabhai <nalin@redhat.com>
- FHS compliance fixes
- modify defaults

* Tue Mar 14 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update to 3.8
- do not create certificate if one already exists

* Mon Feb 21 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update to 3.7
- add patch to find /usr/share/ssl
- change some perms

* Sat Oct 30 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- Modify spec file to match Red Hat standards

* Sun Jul 11 1999 Damien Miller <dmiller@ilogic.com.au>
- Updated to 3.3

* Sat Nov 28 1998 Damien Miller <dmiller@ilogic.com.au>
- Initial RPMification
