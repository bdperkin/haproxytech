%bcond_without check

# https://github.com/rodaine/hclencoder
%global goipath         github.com/rodaine/hclencoder
%global commit          aaa140ee61ed812af9a40790e08803fb3ae1adc0

%gometa

%global common_description %{expand:
HCL Encoder/Marshaller - Convert Go Types into HCL files.}

%global golicenses      LICENSE
%global godocs          readme.md

Name:           %{goname}
Version:        0
Release:        0.1%{?dist}
Summary:        HCL Encoder/Marshaller - Convert Go Types into HCL files

License:        MIT
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires:  golang(github.com/hashicorp/hcl/hcl/ast)
BuildRequires:  golang(github.com/hashicorp/hcl/hcl/printer)
BuildRequires:  golang(github.com/hashicorp/hcl/hcl/token)

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
* Wed May 12 13:30:17 EDT 2021 Brandon Perkins <bperkins@redhat.com> - 0-0.1.20210512gitaaa140e
- Initial package

