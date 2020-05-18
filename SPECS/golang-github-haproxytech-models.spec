%bcond_without check

# https://github.com/haproxytech/models
%global goipath         github.com/haproxytech/models
Version:                2.0.2

%gometa

%global goaltipaths     %{goipath}/v2

%global common_description %{expand:
HAProxy Go structs for API.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Release:        1%{?dist}
Summary:        HAProxy Go structs for API

# Upstream license specification: Apache-2.0
License:        ASL 2.0
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires:  golang(github.com/go-openapi/errors)
BuildRequires:  golang(github.com/go-openapi/strfmt)
BuildRequires:  golang(github.com/go-openapi/swag)
BuildRequires:  golang(github.com/go-openapi/validate)

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
* Mon May 18 2020 Brandon Perkins <bperkins@redhat.com> - 2.0.2-1
- Update to version 2.0.2

* Fri May 08 2020 Brandon Perkins <bperkins@redhat.com> - 2.0.1-1
- Update to version 2.0.1

* Mon Apr 27 2020 Brandon Perkins <bperkins@redhat.com> - 2.0.0-1
- Upgrade to version 2.0.0

* Mon Mar 02 2020 Brandon Perkins <bperkins@redhat.com> - 1.2.4-2
- Clean changelog

* Wed Nov 13 2019 Brandon Perkins <bperkins@redhat.com> - 1.2.4-1
- Initial package

