Name:           webdot
Version:        1.7.1
Release:        1
Group:          Applications/Graphics
Copyright:      BSD-style
URL:            http://www.graphviz.org/
Summary:        A CGI graph server script that uses tcldot from graphviz.
Packager:       John Ellson (ellson@lucent.com)
Requires:       graphviz ghostscript tcl
Source:         http://www.graphviz.org/pub/graphviz/%{name}-%{version}.tar.gz
BuildArchitectures: noarch
BuildRoot:	%{_tmppath}/%{name}-root

%description
A cgi-bin program that produces clickable graphs in web pages
when provided with an href to a .dot file.  Uses Tcldot from the
graphviz rpm.

%prep
%setup -n %{name}-%{version}

%define cgibindir  %(rpm -ql apache | grep '/cgi-bin$')
%define htmldir    %(rpm -ql apache | grep '/html$')
%define cachedir   /var/cache/webdot
%define tclsh8bin  %(rpm -ql tcl | grep tclsh8)
%define libtcldot  %(rpm -ql graphviz | grep 'libtcldot.so$')
%define gsbin      %(which gs)
%define ps2epsibin %(which ps2epsi)

%install
mkdir -p $RPM_BUILD_ROOT/%{cgibindir}
mkdir -p $RPM_BUILD_ROOT/%{htmldir}
mkdir -p $RPM_BUILD_ROOT/%{cachedir}
cat > $RPM_BUILD_ROOT/%{cgibindir}/webdot << '__EOF__'
#!%{tclsh8bin}
set LIBTCLDOT %{libtcldot}
set CACHE_ROOT %{cachedir}
set GS %{gsbin}
set PS2EPSI %{ps2epsibin}
set LOCALHOSTONLY 1
__EOF__
cat $RPM_SOURCE_DIR/cgi-bin/webdot >> $RPM_BUILD_ROOT/%{cgibindir}/webdot
chmod 755 $RPM_BUILD_ROOT/%{cgibindir}/webdot
cp -r $RPM_SOURCE_DIR/html/webdot $RPM_BUILD_ROOT/%{htmldir}/
chown apache:apache $RPM_BUILD_ROOT/%{cachedir}
chmod 700 $RPM_BUILD_ROOT/%{cachedir}
%{?suse_check}

%files
%attr(755,root,root) %{cgibindir}/webdot
%attr(-,root,root) %{htmldir}/webdot/
%attr(700,apache,apache) %{cachedir}/

%post
cat > %{cgibindir}/webdot.new << '__EOF__'
#!%{tclsh8bin}
set LIBTCLDOT %{libtcldot}
set CACHE_ROOT %{cachedir}
set GS %{gsbin}
set PS2EPSI %{ps2epsibin}
set LOCALHOSTONLY 1
__EOF__
tail +7 %{cgibindir}/webdot >> %{cgibindir}/webdot.new
mv -f %{cgibindir}/webdot.new %{cgibindir}/webdot
chmod +x %{cgibindir}/webdot

%clean
rm -rf $RPM_BUILD_ROOT
