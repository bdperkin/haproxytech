%bcond_without check

# https://github.com/haproxytech/client-native
%global goipath         github.com/haproxytech/client-native
Version:                1.2.7

%gometa

%global common_description %{expand:
Go client for HAProxy configuration and runtime API.}

%global golicenses      LICENSE
%global godocs          README.md runtime/README.md

Name:           %{goname}
Release:        1%{?dist}
Summary:        Go client for HAProxy configuration and runtime API

# Upstream license specification: Apache-2.0
License:        ASL 2.0
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires:  golang(github.com/go-openapi/errors)
BuildRequires:  golang(github.com/go-openapi/strfmt)
BuildRequires:  golang(github.com/google/uuid)
BuildRequires:  golang(github.com/haproxytech/config-parser) >= 2.0.0
BuildRequires:  golang(github.com/haproxytech/config-parser/common) >= 2.0.0
BuildRequires:  golang(github.com/haproxytech/config-parser/errors) >= 2.0.0
BuildRequires:  golang(github.com/haproxytech/config-parser/params) >= 2.0.0
BuildRequires:  golang(github.com/haproxytech/config-parser/parsers/filters) >= 2.0.0
BuildRequires:  golang(github.com/haproxytech/config-parser/parsers/http/actions) >= 2.0.0
BuildRequires:  golang(github.com/haproxytech/config-parser/parsers/tcp/actions) >= 2.0.0
BuildRequires:  golang(github.com/haproxytech/config-parser/types) >= 2.0.0
BuildRequires:  golang(github.com/haproxytech/models) >= 1.2.4
BuildRequires:  golang(github.com/mitchellh/mapstructure)
BuildRequires:  golang(github.com/pkg/errors)

%if %{with check}
# Tests
BuildRequires:  golang(github.com/stretchr/testify/assert)
%endif

%description
%{common_description}

%gopkg

%prep
%goprep
rm runtime/README.md

%install
%gopkginstall

%if %{with check}
%check
%gocheck
%endif

%gopkgfiles

%changelog
* Wed Apr 15 2020 Brandon Perkins <bperkins@redhat.com> - 1.2.7-1
- Update to version 1.2.7

* Tue Apr 14 2020 Brandon Perkins <bperkins@redhat.com> - 1.2.6-4
- Add specific versions for haproxytech BuildRequires

* Mon Apr 13 2020 Brandon Perkins <bperkins@redhat.com> - 1.2.6-3
- Remove runtime/README.md

* Mon Mar 02 2020 Brandon Perkins <bperkins@redhat.com> - 1.2.6-2
- Clean changelog

* Wed Nov 13 2019 Brandon Perkins <bperkins@redhat.com> - 1.2.6-1
- Initial package

