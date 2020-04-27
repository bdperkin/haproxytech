%bcond_without check

# https://github.com/haproxytech/client-native
%global goipath         github.com/haproxytech/client-native
Version:                2.0.0

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
BuildRequires:  golang(github.com/google/go-cmp/cmp)
BuildRequires:  golang(github.com/google/uuid)
BuildRequires:  golang(github.com/haproxytech/config-parser/v2)
BuildRequires:  golang(github.com/haproxytech/config-parser/v2/common)
BuildRequires:  golang(github.com/haproxytech/config-parser/v2/errors)
BuildRequires:  golang(github.com/haproxytech/config-parser/v2/params)
BuildRequires:  golang(github.com/haproxytech/config-parser/v2/parsers)
BuildRequires:  golang(github.com/haproxytech/config-parser/v2/parsers/filters)
BuildRequires:  golang(github.com/haproxytech/config-parser/v2/parsers/http/actions)
BuildRequires:  golang(github.com/haproxytech/config-parser/v2/parsers/stats/settings)
BuildRequires:  golang(github.com/haproxytech/config-parser/v2/parsers/tcp/actions)
BuildRequires:  golang(github.com/haproxytech/config-parser/v2/parsers/tcp/types)
BuildRequires:  golang(github.com/haproxytech/config-parser/v2/types)
BuildRequires:  golang(github.com/haproxytech/models/v2)
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
* Mon Apr 27 2020 Brandon Perkins <bperkins@redhat.com> - 2.0.0-1
- Upgrade to version 2.0.0

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

