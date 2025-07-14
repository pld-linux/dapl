# TODO: --enable-mcm (BR: libscif), --enable-coll-type=fca (BR: libfca)
Summary:	Userspace access to RDMA devices using OS-agnostic DAT APIs
Summary(pl.UTF-8):	Dostęp z przestrzeni użytkownika do urządzeń RDMA poprzez API DAT
Name:		dapl
Version:	2.1.10
Release:	1
License:	CPL v1.0 or BSD or GPL v2
Group:		Libraries
Source0:	https://www.openfabrics.org/downloads/dapl/%{name}-%{version}.tar.gz
# Source0-md5:	50df18f8011a37da88f4886514b9dd96
Patch0:		%{name}-link.patch
Patch1:		%{name}-include.patch
Patch2:		%{name}-ibacm.patch
URL:		http://www.openfabrics.org/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	ibacm-devel
BuildRequires:	libibverbs-devel >= 1.1.4
BuildRequires:	librdmacm-devel
BuildRequires:	libtool
Requires:	libibverbs >= 1.1.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Along with the OpenFabrics kernel drivers, libdat2 and libdapl provide
a userspace RDMA API that supports DAT 2.0 specification and
InfiniBand transport extensions for atomic operations and RDMA write
with immediate data.

%description -l pl.UTF-8
Wraz z modułami jądra OpenFabrics, libdat2 i libdapl dostarczają API
RDMA w przestrzeni użytkownika, obsługujące specyfikację DAT 2.0 wraz
z rozszerzeniami transportu InfiniBand dla operacji atomowych i zapisu
RDMA danych bezpośrednich.

%package devel
Summary:	Header files for libdat2 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libdat2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libibverbs-devel >= 1.1.4

%description devel
Header files for libdat2 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libdat2.

%package static
Summary:	Static libdat2 library
Summary(pl.UTF-8):	Statyczna biblioteka libdat2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains the static libdat2 library.

%description static -l pl.UTF-8
Ten pakiet zawiera statyczną bibliotekę libdat2.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-acm \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

# modules dlopened by soname
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libdapl*.{so,la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
# LICENSE is CPL, LICENSE2 is BSD, LICENSE3 is GPL (not included here)
%doc AUTHORS COPYING ChangeLog LICENSE.txt LICENSE2.txt README
%attr(755,root,root) %{_bindir}/dapltest
%attr(755,root,root) %{_bindir}/dtest
%attr(755,root,root) %{_bindir}/dtestcm
%attr(755,root,root) %{_bindir}/dtestsrq
%attr(755,root,root) %{_bindir}/dtestx
%attr(755,root,root) %{_libdir}/libdat2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdat2.so.2
%attr(755,root,root) %{_libdir}/libdaplofa.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdaplofa.so.2
%attr(755,root,root) %{_libdir}/libdaploscm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdaploscm.so.2
%attr(755,root,root) %{_libdir}/libdaploucm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdaploucm.so.2
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dat.conf
%{_mandir}/man1/dapltest.1*
%{_mandir}/man1/dtest.1*
%{_mandir}/man1/dtestcm.1*
%{_mandir}/man1/dtestsrq.1*
%{_mandir}/man1/dtestx.1*
%{_mandir}/man5/dat.conf.5*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdat2.so
%{_libdir}/libdat2.la
%{_includedir}/dat2

%files static
%defattr(644,root,root,755)
%{_libdir}/libdat2.a
