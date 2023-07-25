#
# Conditional build:
%bcond_with	tests		# tests
#
# glapi version (glapi tables in dri drivers and libglx must be in sync);
# set to current Mesa version on ABI break, when xserver tables get regenerated
# (until they start to be somehow versioned themselves)
%define		glapi_ver		7.1.0
# other packages
%define		libdrm_ver		2.4.110
%define		dri2proto_ver		2.8
%define		glproto_ver		1.4.14
%define		zlib_ver		1.2.8
%define		wayland_ver		1.18
%define		libglvnd_ver		1.3.4-2
%define		llvm_ver		11.0.0
%define		gcc_ver 		6:5

%ifarch %{x86_with_sse2}
%define		with_sse2	1
%endif

Summary:	Mesa r300 driver for the vdpau API
Summary(pl.UTF-8):	Sterownik Mesa r300 dla API vdpau
Name:		libvdpau-driver-mesa-r300
# 23.0.x were the last containing vdpau r300 driver
Version:	23.0.3
Release:	1
License:	MIT
Group:		X11/Libraries
Source0:	https://archive.mesa3d.org/mesa-%{version}.tar.xz
# Source0-md5:	3d5025f4f135a1d9131183ac75ba91e4
URL:		https://www.mesa3d.org/
BuildRequires:	bison > 2.3
BuildRequires:	elfutils-devel
BuildRequires:	expat-devel >= 1.95
BuildRequires:	flex
BuildRequires:	gcc >= %{gcc_ver}
%ifarch %{armv6}
BuildRequires:	libatomic-devel
%endif
BuildRequires:	libdrm-devel >= %{libdrm_ver}
BuildRequires:	libglvnd-devel >= %{libglvnd_ver}
BuildRequires:	libselinux-devel
BuildRequires:	libstdc++-devel >= %{gcc_ver}
BuildRequires:	libunwind-devel
BuildRequires:	libvdpau-devel >= 1.1
BuildRequires:	libxcb-devel >= 1.13
BuildRequires:	llvm-devel >= %{llvm_ver}
BuildRequires:	meson >= 1.0.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(talloc) >= 2.0.1
BuildRequires:	pkgconfig(xcb-dri2) >= 1.8
BuildRequires:	pkgconfig(xcb-dri3) >= 1.13
BuildRequires:	pkgconfig(xcb-glx) >= 1.8.1
BuildRequires:	pkgconfig(xcb-present) >= 1.13
BuildRequires:	pkgconfig(xcb-randr) >= 1.12
BuildRequires:	python3 >= 1:3.2
BuildRequires:	python3-Mako >= 0.8.0
BuildRequires:	rpmbuild(macros) >= 2.007
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel >= 1.0.5
BuildRequires:	xorg-lib-libXfixes-devel >= 2.0
BuildRequires:	xorg-lib-libXrandr-devel >= 1.3
BuildRequires:	xorg-lib-libXxf86vm-devel
BuildRequires:	xorg-lib-libxshmfence-devel >= 1.1
BuildRequires:	xorg-proto-dri2proto-devel >= %{dri2proto_ver}
BuildRequires:	xorg-proto-glproto-devel >= %{glproto_ver}
BuildRequires:	xz
BuildRequires:	zlib-devel >= %{zlib_ver}
BuildRequires:	zstd-devel
Requires:	libdrm >= %{libdrm_ver}
Requires:	libvdpau >= 1.1
Requires:	zlib >= %{zlib_ver}
Conflicts:	libvdpau-driver-mesa
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mesa r300 driver for the vdpau API. It supports ATI Radeon adapters
based on R300 chips.

%description -l pl.UTF-8
Sterownik Mesa r300 dla API vdpau. Obsługuje karty ATI Radeon oparte
na układach R300.

%prep
%setup -q -n mesa-%{version}

%build
# glx=dri or egl is required for required dri2 symbols
%meson build \
	-Dplatforms=x11 \
	-Ddri3=enabled \
	-Ddri-drivers-path=%{_libdir}/xorg/modules/dri \
	-Degl=disabled \
	-Dgallium-drivers=r300 \
	-Dgallium-nine=false \
	-Dgallium-omx=disabled \
	-Dgallium-opencl=disabled \
	-Dgallium-va=disabled \
	-Dgallium-vdpau=enabled \
	-Dgallium-xa=disabled \
	-Dgbm=disabled \
	-Dglvnd=true \
	-Dglx=dri \
	-Dlibunwind=enabled \
	-Dlmsensors=disabled \
	-Dsse2=%{__true_false sse2} \
	-Dvideo-codecs=h264dec,h264enc,h265dec,h265enc,vc1dec \
	-Dvulkan-drivers=

%ninja_build -C build

%{?with_tests:%ninja_test -C build}

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

# GLX interface and dri driver not wanted here
%{__rm} -r $RPM_BUILD_ROOT%{_includedir}/GL
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/xorg
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libGLX_mesa.so*
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libglapi.so*
%{__rm} $RPM_BUILD_ROOT%{_pkgconfigdir}/dri.pc
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/drirc.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_r300.so.1.0.0
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_r300.so.1.0
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_r300.so.1
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_r300.so
