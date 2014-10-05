# based on PLD Linux spec git://git.pld-linux.org/packages/.git
Summary:	LADSPA SDK example plugins
Name:		ladspa
Version:	1.13
Release:	5
License:	LGPL
Group:		Libraries
Source0:	http://www.ladspa.org/download/%{name}_sdk_%{version}.tgz
# Source0-md5:	671be3e1021d0722cadc7fb27054628e
Patch0:		%{name}-fix-memleak-in-plugin-scanning.patch
Patch1:		%{name}-fallback-path.patch
URL:		http://www.ladspa.org/
BuildRequires:	libstdc++-devel
BuildRequires:	sed
Requires:	%{name}-common
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
There is a large number of synthesis packages in use or development on
the Linux platform at this time. The Linux Audio Developer's Simple
Plugin API (LADSPA) attempts to give programmers the ability to write
simple `plugin' audio processors in C/C++ and link them dynamically
against a range of host applications.

This package contains the example plugins from the LADSPA SDK.

%package common
Summary:	Common environment for LADSPA plugins
Group:		Libraries

%description common
Common environment for LADSPA plugins. Currently it contains only
appropriate directory trees.

%package devel
Summary:	Linux Audio Developer's Simple Plugin API
Group:		Development/Libraries
# doesn't require base or common

%description devel
There is a large number of synthesis packages in use or development on
the Linux platform at this time. The Linux Audio Developer's Simple
Plugin API (LADSPA) attempts to give programmers the ability to write
simple `plugin' audio processors in C/C++ and link them dynamically
against a range of host applications.

Definitive technical documentation on LADSPA plugins for both the host
and plugin is contained within copious comments within the ladspa.h
header file.

%prep
%setup -qn %{name}_sdk
%patch0 -p0
cd src
%{__sed} -e "s|@LIBDIR@|%{_libdir}|" %{PATCH1} | patch -p1 -s
cd ..

# fix links to the header file in the docs
%{__sed} -i -e 's|HREF=\"ladspa.h.txt\"|href=\"file:///usr/include/ladspa.h\"|' doc/*.html
%{__sed} -i -e 's|mkdirhier|/usr/bin/install -d|' src/makefile

%build
%{__make} -C src targets \
	CC="%{__cc}" CPP="%{__cxx}" \
	CFLAGS="-I. -Wall -Werror %{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/ladspa/rdf

%{__make} -C src install \
	INSTALL_PLUGINS_DIR=$RPM_BUILD_ROOT%{_libdir}/ladspa	\
	INSTALL_INCLUDE_DIR=$RPM_BUILD_ROOT%{_includedir}	\
	INSTALL_BINARY_DIR=$RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/ladspa/*.so

%files common
%defattr(644,root,root,755)
%dir %{_libdir}/ladspa
%dir %{_datadir}/ladspa
%dir %{_datadir}/ladspa/rdf

%files devel
%defattr(644,root,root,755)
%doc doc/*.html
%{_includedir}/ladspa.h

