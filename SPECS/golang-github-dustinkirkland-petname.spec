%bcond_without check

%global gorepo          petname

%global _hardened_build 1

# https://github.com/dustinkirkland/golang-petname
%global goipath         github.com/dustinkirkland/golang-petname
%global commit          8e5a1ed0cff0384869564ec1c086c6467a025667

%gometa

%global common_description %{expand:
An RFC1178 implementation.}

%global golicenses      LICENSE
%global godocs          README.md debian/changelog

Name:           %{goname}
Version:        0
Release:        0.1%{?dist}
Summary:        An RFC1178 implementation

# Upstream license specification: Apache-2.0
License:        ASL 2.0
URL:            %{gourl}
Source0:        %{gosource}

%description
%{common_description}

%gopkg

%prep
%goprep

%build
%gobuild -o %{gobuilddir}/bin/%{gorepo} %{goipath}/cmd/%{gorepo}/
mkdir -p %{gobuilddir}/share/man/man1
cp %{gobuilddir}/../golang-%{gorepo}.1 %{gobuilddir}/share/man/man1/%{gorepo}.1
gzip %{gobuilddir}/share/man/man1/%{gorepo}.1

%install
%gopkginstall
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp %{gobuilddir}/bin/* %{buildroot}%{_bindir}/
install -m 0755 -vd                                %{buildroot}%{_mandir}/man1
install -m 0644 -vp %{gobuilddir}/share/man/man1/* %{buildroot}%{_mandir}/man1/

%if %{with check}
%check
%gocheck
%endif

%files
%license LICENSE
%doc README.md debian/changelog
%{_mandir}/man1/%{gorepo}.1*
%{_bindir}/*

%gopkgfiles

%changelog
* Fri May 08 2020 Brandon Perkins <bperkins@redhat.com> - 0-0.1.20200508git8e5a1ed
- Initial package

