%bcond_without check

# https://github.com/GehirnInc/crypt
%global goipath         github.com/GehirnInc/crypt
%global commit          6c0105aabd460ae06c87afeb5a47c869f6a7557e

%gometa

%global common_description %{expand:
Pure Go crypt(3) Implementation.}

%global golicenses      LICENSE
%global godocs          AUTHORS.md README.rst

Name:           %{goname}
Version:        0
Release:        0.2%{?dist}
Summary:        Pure Go crypt(3) Implementation

# Upstream license specification: BSD-2-Clause
License:        BSD
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
* Mon Mar 02 15:30:56 EST 2020 Brandon Perkins <bperkins@redhat.com> - 0-0.2.20200302git6c0105a
- Clean changelog

* Wed Nov 13 12:21:07 UTC 2019 Brandon Perkins <bperkins@redhat.com> - 0-0.1.20191113git6c0105a
- Initial package

