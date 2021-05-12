%bcond_without check

# https://github.com/lestrrat-go/apache-logformat
%global goipath         github.com/lestrrat-go/apache-logformat
Version:                2.0.6

%gometa

%global common_description %{expand:
Port of Perl5's Apache::LogFormat::Compiler to golang.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Release:        1%{?dist}
Summary:        Port of Perl5's Apache::LogFormat::Compiler to golang

License:        MIT
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires:  golang(github.com/lestrrat-go/strftime)
BuildRequires:  golang(github.com/pkg/errors)

%if %{with check}
# Tests
BuildRequires:  golang(github.com/facebookgo/clock)
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
* Wed May 12 13:30:04 EDT 2021 Brandon Perkins <bperkins@redhat.com> - 2.0.6-1
- Initial package

