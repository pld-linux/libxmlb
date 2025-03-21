#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library
%bcond_without	stemmer		# stemmer support
#
Summary:	Library to create or query compressed XML files
Summary(pl.UTF-8):	Biblioteka do tworzenia i odpytywania skompresowanych plików XML
Name:		libxmlb
Version:	0.3.22
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/hughsie/libxmlb/releases
Source0:	https://github.com/hughsie/libxmlb/releases/download/%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	534de564b028b7ef038238efb2e70d2f
URL:		https://github.com/hughsie/libxmlb
BuildRequires:	glib2-devel >= 1:2.45.8
BuildRequires:	gobject-introspection-devel
%{?with_apidocs:BuildRequires:	gtk-doc}
%{?with_stemmer:BuildRequires:	libstemmer-devel}
BuildRequires:	libuuid-devel
BuildRequires:	meson >= 0.60.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	xz-devel
BuildRequires:	zstd-devel
Requires:	glib2 >= 1:2.45.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
XML is slow to parse and strings inside the document cannot be memory
mapped as they do not have a trailing NUL char. The libxmlb library
takes XML source, and converts it to a structured binary
representation with a deduplicated string table - where the strings
have the NULs included.

This allows an application to mmap the binary XML file, do an XPath
query and return some strings without actually parsing the entire
document. This is all done using (almost) zero allocations and no
actual copying of the binary data.

%description -l pl.UTF-8
XML jest wolny do analizy, a łańcuchy znaków wewnątrz dokumentu nie
mogą być odwzorowane w pamięci, ponieważ nie mają końcowych znaków
NUL. Biblioteka libxmlb pobiera źródło XML i przekształca je do
strukturalnej reprezentacji binarnej z zdeduplikowaną tablicą
łańcuchów znaków - w której łańcuchy mają końcowy znak NUL.

Pozwala to aplikacjom odwzorować w pamięci binarny plik XML, wykonać
zapytanie XPath i zwrócić jakieś łańcuchy znaków bez analizy całego
dokumentu. Jest to wykonywane (prawie) bez przydzielania pamięci ani
kopiowania danych binarnych.

%package devel
Summary:	Header files for libxmlb library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libxmlb
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.45.8
Requires:	libstemmer-devel
Requires:	xz-devel
Requires:	zstd-devel

%description devel
Header files for libxmlb library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libxmlb.

%package static
Summary:	Static libxmlb library
Summary(pl.UTF-8):	Statyczna biblioteka libxmlb
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libxmlb library.

%description static -l pl.UTF-8
Statyczna biblioteka libxmlb.

%package apidocs
Summary:	API documentation for libxmlb library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libxmlb
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libxmlb library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libxmlb.

%prep
%setup -q

%build
%if %{with stemmer}
CPPFLAGS="%{rpmcppflags} -I/usr/include/libstemmer"
%endif
%meson \
	%{!?with_static_libs:--default-library=shared} \
	%{!?with_apidocs:-Dgtkdoc=false} \
	-Dlzma=enabled \
	%{?with_stemmer:-Dstemmer=true} \
	-Dtests=false \
	-Dzstd=enabled

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc MAINTAINERS NEWS README.md
%attr(755,root,root) %{_bindir}/xb-tool
%attr(755,root,root) %{_libdir}/libxmlb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libxmlb.so.2
%{_libdir}/girepository-1.0/Xmlb-2.0.typelib
%{_mandir}/man1/xb-tool.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxmlb.so
%{_includedir}/libxmlb-2
%{_datadir}/gir-1.0/Xmlb-2.0.gir
%{_pkgconfigdir}/xmlb.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libxmlb.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libxmlb
%endif
