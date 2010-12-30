%define target avr

%define distsuffix edm
Name:           %{target}-gdb
Version:        7.1
Release:        %mkrel 1
Summary:        GDB for (remote) debugging %{target} binaries
Group:          Development/Tools
License:        GPLv2+
URL:            http://sources.redhat.com/gdb/
Source0:        http://ftp.gnu.org/gnu/gdb/gdb-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)
BuildRequires:  ncurses-devel chrpath
Conflicts:      cross-avr-gdb

%description
This is a special version of GDB, the GNU Project debugger, for (remote)
debugging %{target} binaries. GDB allows you to see what is going on
inside another program while it executes or what another program was doing at
the moment it crashed. 


%prep
%setup -q -c
pushd gdb-%{version}
# fix various configure tests failing on -Werror-implicit-function-declaration
sed -i -e 's/exit (0)/return 0/g' -e 's/ exit(2)/ return 2/g' \
  `find -name configure`
popd


%build
mkdir -p build
pushd build
CFLAGS="${RPM_OPT_FLAGS/-Werror=format-security/} -D_GNU_SOURCE" \
  ../gdb-%{version}/configure --prefix=%{_prefix} \
  --libdir=%{_libdir} --mandir=%{_mandir} --infodir=%{_infodir} \
  --target=%{target} --disable-nls
make %{?_smp_mflags}
popd


%install
rm -rf $RPM_BUILD_ROOT
pushd build
make install DESTDIR=$RPM_BUILD_ROOT
popd
# our usual libtool sed magic doesn't work as libtool gets generated during
# the make <sigh>
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/%{name}
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/%{name}tui
# we don't want these as we are a cross version
rm -r $RPM_BUILD_ROOT%{_infodir}
rm    $RPM_BUILD_ROOT%{_libdir}/libiberty.a


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc gdb-%{version}/COPYING* gdb-%{version}/README*
%{_bindir}/%{name}*
%{_mandir}/man1/%{name}*
%ifarch x86_64
   /usr/lib64/libavr-sim.a
%endif
%ifarch i386 i486 i586 i686
   /usr/lib/libavr-sim.a
%endif
   /usr/bin/avr-run
   /usr/share/gdb/syscalls/amd64-linux.xml
   /usr/share/gdb/syscalls/gdb-syscalls.dtd
   /usr/share/gdb/syscalls/i386-linux.xml
   /usr/share/gdb/syscalls/ppc-linux.xml
   /usr/share/gdb/syscalls/ppc64-linux.xml
   /usr/share/man/man1/avr-run.1.lzma


