%bcond_without check

# https://github.com/facebookgo/clock
%global goipath         github.com/facebookgo/clock
%global commit          600d898af40aa09a7a93ecb9265d87b0504b6f03

%gometa

%global common_description %{expand:
Clock is a small library for mocking time in Go.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Version:        0
Release:        0.1%{?dist}
Summary:        Clock is a small library for mocking time in Go

License:        MIT
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
* Wed May 12 13:54:36 EDT 2021 Brandon Perkins <bperkins@redhat.com> - 0-0.1.20210512git600d898
- Initial package

