%bcond_without check
%global debug_package %{nil}

# https://github.com/jinzhu/copier
%global goipath         github.com/jinzhu/copier
Version:                0.3.5

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

%generate_buildrequires
%go_generate_buildrequires

%install
%gopkginstall

%if %{with check}
%check
%gocheck
%endif

%gopkgfiles

%changelog
* Mon Jan 31 2022 Brandon Perkins <bperkins@redhat.com> - 0.3.5-1
- Initial package
