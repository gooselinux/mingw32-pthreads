%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

# The tests take ages to run and require Wine.
%define run_tests 0

Name:           mingw32-pthreads
Version:        2.8.0
Release:        10%{?dist}.6
Summary:        MinGW pthread library

%define crazy_version %(echo %{version}|tr . -)

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://sourceware.org/pthreads-win32/
Source0:        ftp://sourceware.org/pub/pthreads-win32/pthreads-w32-%{crazy_version}-release.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

Patch0:         mingw32-pthreads-2.8.0-use-wine-for-tests.patch
Patch1:         mingw32-pthreads-2.8.0-no-failing-tests.patch
Patch2:		mingw32-pthreads-flags.patch
Patch3:		mingw32-pthreads-2.8.0-w32.patch

BuildRequires:  mingw32-filesystem >= 49
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils

%if %{run_tests}
BuildRequires:  wine
%endif


%description
The POSIX 1003.1-2001 standard defines an application programming
interface (API) for writing multithreaded applications. This interface
is known more commonly as pthreads. A good number of modern operating
systems include a threading library of some kind: Solaris (UI)
threads, Win32 threads, DCE threads, DECthreads, or any of the draft
revisions of the pthreads standard. The trend is that most of these
systems are slowly adopting the pthreads standard API, with
application developers following suit to reduce porting woes.

Win32 does not, and is unlikely to ever, support pthreads
natively. This project seeks to provide a freely available and
high-quality solution to this problem.


%prep
%setup -q -n pthreads-w32-%{crazy_version}-release

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1


%build
%{_mingw32_make} clean
%{_mingw32_make} CROSS=%{_mingw32_host}- GC-inlined
%{_mingw32_make} clean
%{_mingw32_make} CROSS=%{_mingw32_host}- GCE-inlined


%check
%if %{run_tests}
pushd tests
%{_mingw32_make} clean
%{_mingw32_make} QAPC= \
  CC=%{_mingw32_cc} XXCFLAGS="-D__CLEANUP_C" TEST=GC all-pass
%{_mingw32_make} clean
%{_mingw32_make} QAPC= \
  CC=%{_mingw32_cc} XXCFLAGS="-D__CLEANUP_C" TEST=GCE all-pass
popd
%endif


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_mingw32_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mingw32_libdir}
mkdir -p $RPM_BUILD_ROOT%{_mingw32_includedir}

install -m 0755 *.dll $RPM_BUILD_ROOT%{_mingw32_bindir}
install -m 0644 *.def $RPM_BUILD_ROOT%{_mingw32_bindir}
install -m 0644 *.a $RPM_BUILD_ROOT%{_mingw32_libdir}
install -m 0644 *.h $RPM_BUILD_ROOT%{_mingw32_includedir}

# Create a symlink from libpthreadGC2.a to libpthread.a because of BZ #498616
ln -s libpthreadGC2.a $RPM_BUILD_ROOT%{_mingw32_libdir}/libpthread.a


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc ANNOUNCE BUGS ChangeLog CONTRIBUTORS COPYING COPYING.LIB
%doc FAQ MAINTAINERS NEWS PROGRESS README README.NONPORTABLE TODO
%{_mingw32_bindir}/pthreadGC2.dll
%{_mingw32_bindir}/pthreadGCE2.dll
%{_mingw32_bindir}/pthread.def
%{_mingw32_libdir}/libpthread.a
%{_mingw32_libdir}/libpthreadGC2.a
%{_mingw32_libdir}/libpthreadGCE2.a
%{_mingw32_includedir}/*.h


%changelog
* Mon Dec 27 2010 Andrew Beekhof <abeekhof@redhat.com> - 2.8.0-10.6
- Rebuild everything with gcc-4.4
  Related: rhbz#658833

* Mon Dec 27 2010 Andrew Beekhof <abeekhof@redhat.com> - 2.8.0-10.5
- Rebuild for downgrade to gcc-4.4
  Related: rhbz#658833

* Fri Dec 24 2010 Andrew Beekhof <abeekhof@redhat.com> - 2.8.0-10.4
- Rebuild for new 3.18 mingw32 runtime
  Related: rhbz#658833

* Thu Dec 23 2010 Andrew Beekhof <abeekhof@redhat.com> - 2.8.0-10.3
- Drop ExclusiveArch as its incompatible with noarch
  Related: rhbz#658833

* Wed Dec 22 2010 Andrew Beekhof <abeekhof@redhat.com> - 2.8.0-10.2
- Only build mingw packages on x86_64
  Related: rhbz#658833

* Wed Dec 22 2010 Andrew Beekhof <abeekhof@redhat.com> - 2.8.0-10.1
- Bump the revision to avoid tag collision
  Related: rhbz#658833

* Sun Nov 15 2009 Levente Farkas <lfarkas@lfarkas.org> - 2.8.0-10
- added mingw32-pthreads-2.8.0-w32.patch

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 22 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.8.0-8
- Create a symlink from libpthreadGC2.a to libpthread.a because of BZ #498616

* Fri Mar 13 2009 Richard W.M. Jones <rjones@redhat.com> - 2.8.0-7
- Move header files to system include directory.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 2.8.0-5
- Rebuild for mingw32-gcc 4.4

* Tue Jan 13 2009 Richard W.M. Jones <rjones@redhat.com> - 2.8.0-4
- Cleanup to the spec file, no functional changes.

* Mon Dec 29 2008 Levente Farkas <lfarkas@lfarkas.org> - 2.8.0-3
- minor cleanup

* Fri Oct 10 2008 Richard W.M. Jones <rjones@redhat.com> - 2.8.0-2
- Initial RPM release.
