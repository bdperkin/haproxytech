%bcond_without check

# https://github.com/lestrrat-go/envload
%global goipath         github.com/lestrrat-go/envload
%global commit          a3eb8ddeffccdbca0eb6dd6cc7c7950c040a6546

%gometa

%global common_description %{expand:
Restore and load environment variables.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Version:        0
Release:        0.1%{?dist}
Summary:        Restore and load environment variables

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
* Wed May 12 2021 Brandon Perkins <bperkins@redhat.com> - 0-0.1.20210512gita3eb8dd
- Initial package

