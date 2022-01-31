%bcond_without check

# https://github.com/haproxytech/kubernetes-ingress
%global goipath         github.com/haproxytech/kubernetes-ingress
Version:                1.7.5

%gometa

%global common_description %{expand:
HAProxy Kubernetes Ingress Controller.}

%global golicenses      LICENSE assets/license-header.txt
%global godocs          README.md crs/README.md documentation/README.md\\\
                        documentation/canary-deployment.md\\\
                        documentation/controller.md documentation/secondary-\\\
                        config.md documentation/ingressclass.md\\\
                        documentation/gen/README.md\\\
                        documentation/gen/readme.go

Name:           %{goname}
Release:        1%{?dist}
Summary:        HAProxy Kubernetes Ingress Controller

# Upstream license specification: Apache-2.0
License:        ASL 2.0
URL:            %{gourl}
Source0:        %{gosource}

%description
%{common_description}

%gopkg

%prep
%goprep

%generate_buildrequires
%go_generate_buildrequires

%build
%gobuild -o %{gobuilddir}/bin/kubernetes-ingress %{goipath}

%install
%gopkginstall
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp %{gobuilddir}/bin/* %{buildroot}%{_bindir}/

%if %{with check}
%check
%gocheck
%endif

%files
%license LICENSE assets/license-header.txt
%doc README.md crs/README.md documentation/README.md
%doc documentation/canary-deployment.md documentation/controller.md
%doc documentation/secondary-config.md documentation/ingressclass.md
%doc documentation/gen/README.md documentation/gen/readme.go
%{_bindir}/*

%gopkgfiles

%changelog
* Mon Jan 31 2022 Brandon Perkins <bperkins@redhat.com> - 1.7.5-1
- Initial package
