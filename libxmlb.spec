#
# Conditional build:
%bcond_without	apidocs		# API documentation
#
Summary:	Library to create or query compressed XML files
Summary(pl.UTF-8):	Biblioteka do tworzenia i odpytywania skompresowanych plików XML
Name:		libxmlb
Version:	0.1.2
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://people.freedesktop.org/~hughsient/releases/%{name}-%{version}.tar.xz
# Source0-md5:	b8346bbcf8318f5546822ede2d7de64a
URL:		https://github.com/hughsie/libxmlb
BuildRequires:	glib2-devel >= 1:2.45.8
%{?with_apidocs:BuildRequires:	gtk-doc}
BuildRequires:	libuuid-devel
BuildRequires:	meson >= 0.46.0
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.727
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
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

%description devel
Header files for libxmlb library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libxmlb.

%package apidocs
Summary:	API documentation for libxmlb library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libxmlb
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for libxmlb library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libxmlb.

%prep
%setup -q

%build
%meson build \
	%{!?with_apidocs:-Dgtkdoc=false}

%meson_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc MAINTAINERS NEWS README.md
%attr(755,root,root) %{_libdir}/libxmlb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libxmlb.so.1
%{_libdir}/girepository-1.0/Xmlb-1.0.typelib
%attr(755,root,root) %{_libexecdir}/xb-tool

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxmlb.so
%{_includedir}/libxmlb-1
%{_datadir}/gir-1.0/Xmlb-1.0.gir
%{_pkgconfigdir}/xmlb.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libxmlb
%endif
