%bcond_without check

%global gorepo          dataplaneapi
%global haproxy_user    haproxy
%global haproxy_group   %{haproxy_user}
%global haproxy_homedir %{_localstatedir}/lib/haproxy

%global _hardened_build 1

# https://github.com/haproxytech/dataplaneapi
%global goipath         github.com/haproxytech/dataplaneapi
Version:                2.0.3

%gometa

%global goaltipaths     %{goipath}/v2

%global common_description %{expand:
HAProxy Data Plane API.}

%global golicenses      LICENSE
%global godocs          CONTRIBUTING.md README.md

Name:           %{goname}
Release:        1%{?dist}
Summary:        HAProxy Data Plane API

Group:          System Environment/Daemons

# Upstream license specification: Apache-2.0
License:        ASL 2.0
URL:            %{gourl}
Source0:        %{gosource}
Source1:        %{gorepo}.service
Source2:        %{gorepo}.logrotate
Source3:        %{gorepo}.sysconfig

BuildRequires:  golang(github.com/docker/go-units)
BuildRequires:  golang(github.com/dustinkirkland/golang-petname)
BuildRequires:  golang(github.com/GehirnInc/crypt)
BuildRequires:  golang(github.com/GehirnInc/crypt/md5_crypt)
BuildRequires:  golang(github.com/GehirnInc/crypt/sha256_crypt)
BuildRequires:  golang(github.com/GehirnInc/crypt/sha512_crypt)
BuildRequires:  golang(github.com/go-openapi/errors)
BuildRequires:  golang(github.com/go-openapi/loads)
BuildRequires:  golang(github.com/go-openapi/runtime)
BuildRequires:  golang(github.com/go-openapi/runtime/flagext)
BuildRequires:  golang(github.com/go-openapi/runtime/middleware)
BuildRequires:  golang(github.com/go-openapi/runtime/security)
BuildRequires:  golang(github.com/go-openapi/spec)
BuildRequires:  golang(github.com/go-openapi/strfmt)
BuildRequires:  golang(github.com/go-openapi/swag)
BuildRequires:  golang(github.com/go-openapi/validate)
BuildRequires:  golang(github.com/haproxytech/client-native/v2)
BuildRequires:  golang(github.com/haproxytech/client-native/v2/configuration)
BuildRequires:  golang(github.com/haproxytech/client-native/v2/errors)
BuildRequires:  golang(github.com/haproxytech/client-native/v2/runtime)
BuildRequires:  golang(github.com/haproxytech/config-parser/v2)
BuildRequires:  golang(github.com/haproxytech/config-parser/v2/common)
BuildRequires:  golang(github.com/haproxytech/config-parser/v2/types)
BuildRequires:  golang(github.com/haproxytech/models/v2)
BuildRequires:  golang(github.com/jessevdk/go-flags)
BuildRequires:  golang(github.com/rs/cors)
BuildRequires:  golang(github.com/shirou/gopsutil/host)
BuildRequires:  golang(github.com/shirou/gopsutil/mem)
BuildRequires:  golang(github.com/sirupsen/logrus)
BuildRequires:  golang(golang.org/x/net/netutil)
BuildRequires:  golang(golang.org/x/sys/unix)
BuildRequires:  golang(gopkg.in/yaml.v2)
BuildRequires:  systemd-units
BuildRequires:  help2man
BuildRequires:  gzip

Requires:         haproxy >= 2.0
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

Suggests: logrotate

%description
%{common_description}

%gopkg

%prep
%goprep

%build
LDFLAGS="-X main.GitRepo=%{url}/archive/v%{version}/%{gorepo}-%{version}.tar.gz "
LDFLAGS+="-X main.GitTag=v%{version} -X main.GitCommit= -X main.GitDirty= "
LDFLAGS+="-X main.BuildTime=%(date '+%%Y-%%m-%%dT%%H:%%M:%%S') "
%gobuild -o %{gobuilddir}/sbin/%{gorepo} %{goipath}/cmd/%{gorepo}/
mkdir -p %{gobuilddir}/share/man/man8
help2man -n "%{summary}" -s 8 -o %{gobuilddir}/share/man/man8/%{gorepo}.8 -N --version-string="%{version}" %{gobuilddir}/sbin/%{gorepo}
gzip %{gobuilddir}/share/man/man8/%{gorepo}.8

%install
%gopkginstall
install -m 0755 -vd                      %{buildroot}%{_sbindir}
install -m 0755 -vp %{gobuilddir}/sbin/* %{buildroot}%{_sbindir}/
install -m 0755 -vd                                %{buildroot}%{_mandir}/man8
install -m 0644 -vp %{gobuilddir}/share/man/man8/* %{buildroot}%{_mandir}/man8/

install -d -m 0755 %{buildroot}%{_unitdir}
install -d -m 0755 %{buildroot}%{_sysconfdir}/logrotate.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/sysconfig
install -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{gorepo}.service
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{goname}
install -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{gorepo}

%if %{with check}
%check
%gocheck
%endif

%post
%systemd_post %{gorepo}.service

%preun
%systemd_preun %{gorepo}.service

%postun
%systemd_postun_with_restart %{gorepo}.service

%files
%license LICENSE
%doc CONTRIBUTING.md README.md
%{_mandir}/man8/%{gorepo}.8*
%config(noreplace) %{_sysconfdir}/logrotate.d/%{goname}
%config(noreplace) %{_sysconfdir}/sysconfig/%{gorepo}
%{_unitdir}/%{gorepo}.service
%{_sbindir}/*

%gopkgfiles

%changelog
* Mon Jun 01 2020 Brandon Perkins <bperkins@redhat.com> - 2.0.3-1
- Update to version 2.0.3

* Mon May 18 2020 Brandon Perkins <bperkins@redhat.com> - 2.0.2-1
- Update to version 2.0.2

* Fri May 08 2020 Brandon Perkins <bperkins@redhat.com> - 2.0.1-1
- Update to version 2.0.1

* Tue Apr 28 2020 Brandon Perkins <bperkins@redhat.com> - 2.0.0-2
- Add LDFLAGS for GitRepo, GitTag, GitCommit, GitDirty, and
  BuildTime variables
- Simplify gobuild action to only build dataplaneapi

* Mon Apr 27 2020 Brandon Perkins <bperkins@redhat.com> - 2.0.0-1
- Upgrade to version 2.0.0

* Wed Apr 15 2020 Brandon Perkins <bperkins@redhat.com> - 1.2.5-1
- Update to version 1.2.5

* Tue Apr 14 2020 Brandon Perkins <bperkins@redhat.com> - 1.2.4-7
- Change haproxy requires to >= 2.0 as 1.9 was never packaged
- Add specific versions for haproxytech BuildRequires

* Wed Mar 04 2020 Brandon Perkins <bperkins@redhat.com> - 1.2.4-6
- Use global instead of define macro
- Remove defattr macro that is not needed

* Mon Mar 02 2020 Brandon Perkins <bperkins@redhat.com> - 1.2.4-5
- Clean changelog

* Thu Nov 21 2019 Brandon Perkins <bperkins@redhat.com> - 1.2.4-4
- Suggest logrotate and fix logrotate configuration

* Wed Nov 20 2019 Brandon Perkins <bperkins@redhat.com> - 1.2.4-3
- Add man page

* Wed Nov 13 2019 Brandon Perkins <bperkins@redhat.com> - 1.2.4-2
- Implement systemd

* Wed Nov 13 2019 Brandon Perkins <bperkins@redhat.com> - 1.2.4-1
- Initial package

