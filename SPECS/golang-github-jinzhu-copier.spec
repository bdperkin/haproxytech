%bcond_without check

# https://github.com/jinzhu/copier
%global goipath         github.com/jinzhu/copier
Version:                0.3.4

%gometa

%global common_description %{expand:
Copier for golang, copy value from struct to struct and more.}

%global golicenses      License
%global godocs          README.md

Name:           %{goname}
Release:        1%{?dist}
Summary:        Copier for golang, copy value from struct to struct and more

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
* Mon Dec 13 2021 Brandon Perkins <bperkins@redhat.com> - 0.3.4-1%{?dist}
- Initial package

