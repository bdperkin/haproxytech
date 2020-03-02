# Generated by go2rpm 1
%bcond_without check

# https://github.com/haproxytech/client-native
%global goipath         github.com/haproxytech/client-native
Version:                1.2.6

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
BuildRequires:  golang(github.com/haproxytech/config-parser)
BuildRequires:  golang(github.com/haproxytech/config-parser/common)
BuildRequires:  golang(github.com/haproxytech/config-parser/errors)
BuildRequires:  golang(github.com/haproxytech/config-parser/params)
BuildRequires:  golang(github.com/haproxytech/config-parser/parsers/filters)
BuildRequires:  golang(github.com/haproxytech/config-parser/parsers/http/actions)
BuildRequires:  golang(github.com/haproxytech/config-parser/parsers/tcp/actions)
BuildRequires:  golang(github.com/haproxytech/config-parser/types)
BuildRequires:  golang(github.com/haproxytech/models)
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

%install
%gopkginstall

%if %{with check}
%check
%gocheck
%endif

%gopkgfiles

%changelog
* Wed Nov 13 12:24:19 UTC 2019 Brandon Perkins <bperkins@redhat.com> - 1.2.6-1
- Initial package

