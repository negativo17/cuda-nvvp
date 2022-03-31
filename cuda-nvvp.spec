%global real_name cuda_nvvp

%global debug_package %{nil}
%global __strip /bin/true
%global _missing_build_ids_terminate_build 0
%global _build_id_links none
%global major_package_version 11-6

Name:           %(echo %real_name | tr '_' '-')
Epoch:          1
Version:        11.6.124
Release:        1%{?dist}
Summary:        CUDA NVIDIA Visual Profiler
License:        CUDA Toolkit
URL:            https://developer.nvidia.com/cuda-toolkit
ExclusiveArch:  x86_64 ppc64le

Source0:        https://developer.download.nvidia.com/compute/cuda/redist/%{real_name}/linux-x86_64/%{real_name}-linux-x86_64-%{version}-archive.tar.xz
Source1:        https://developer.download.nvidia.com/compute/cuda/redist/%{real_name}/linux-ppc64le/%{real_name}-linux-ppc64le-%{version}-archive.tar.xz
Source2:        nvvp.desktop
Source3:        nvvp.appdata.xml

BuildRequires:  ImageMagick
BuildRequires:  desktop-file-utils

Conflicts:      %{name}-nvvp-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}   

%description
The NVIDIA Visual Profiler is a cross-platform performance profiling tool that
delivers developers vital feedback for optimizing CUDA C/C++ applications.

%prep
%ifarch x86_64
%setup -q -n %{real_name}-linux-x86_64-%{version}-archive
%endif

%ifarch ppc64le
%setup -q -T -b 1 -n %{real_name}-linux-ppc64le-%{version}-archive
%endif

%install
mkdir -p %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_datadir}/applications/
mkdir -p %{buildroot}%{_datadir}/pixmaps/
mkdir -p %{buildroot}%{_libdir}/nvvp/

# Nvidia Visual Profiler
convert libnvvp/icon.xpm nvvp.png
install -m 644 -p nvvp.png %{buildroot}%{_datadir}/pixmaps/nvvp.png
cp -fr libnvvp/* %{buildroot}%{_libdir}/nvvp/
ln -sf ../%{_lib}/nvvp/nvvp %{buildroot}%{_bindir}/

# Remove non-working libcrypto libraries
# find . -name "*libcrypto*" -delete

# Desktop files
desktop-file-install --dir %{buildroot}%{_datadir}/applications/ %{SOURCE2}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/nvvp.desktop

%if 0%{?fedora}
# install AppData and add modalias provides
mkdir -p %{buildroot}%{_metainfodir}
install -p -m 0644 %{SOURCE3} %{buildroot}%{_metainfodir}/
%endif

%files
%license LICENSE
%{_bindir}/nvvp
%if 0%{?fedora} || 0%{?rhel} >= 8
%{_metainfodir}/nvvp.appdata.xml
%endif
%{_datadir}/applications/nvvp.desktop
%{_datadir}/pixmaps/nvvp.png
%{_libdir}/nvvp

%changelog
* Thu Mar 31 2022 Simone Caronni <negativo17@gmail.com> - 1:11.6.124-1
- Update to 11.6.124 (CUDA 11.6.2).

* Tue Mar 08 2022 Simone Caronni <negativo17@gmail.com> - 1:11.6.112-1
- Update to 11.6.112 (CUDA 11.6.1).

* Tue Feb 01 2022 Simone Caronni <negativo17@gmail.com> - 1:11.6.58-1
- First build with the new tarball components.
