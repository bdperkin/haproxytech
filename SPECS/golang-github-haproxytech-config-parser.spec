%bcond_without check

# https://github.com/haproxytech/config-parser
%global goipath         github.com/haproxytech/config-parser
Version:                1.2.0

%gometa

%global common_description %{expand:
HAProxy configuration parser.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Release:        1%{?dist}
Summary:        HAProxy configuration parser

# Upstream license specification: Apache-2.0
License:        ASL 2.0
URL:            %{gourl}
Source0:        %{gosource}

%description
%{common_description}

%gopkg

%prep
%goprep

%install
%gopkginstall

%if %{with check}
%check
%gocheck
%endif

%gopkgfiles

%changelog
* Mon Mar 02 2020 Brandon Perkins <bperkins@redhat.com> - 1.2.0-1
- Upgrade to version 1.2.0
- Clean changelog

* Wed Nov 13 2019 Brandon Perkins <bperkins@redhat.com> - 1.1.10-1
- Initial package

