%bcond_without check

# https://github.com/haproxytech/go-logger
%global goipath         github.com/haproxytech/go-logger
Version:                1.0.0

%gometa

%global common_description %{expand:
Go package that provides interface for logging.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Release:        1%{?dist}
Summary:        Go package that provides interface for logging

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
* Thu Sep 09 2021 Brandon Perkins <bperkins@redhat.com> - 1.0.0-1%{?dist}
- Initial package

