Summary:	PLD LiveCD scripts
Summary(pl):	Skrypty PLD LiveCD
Name:		livecd
Version:	1.0
Release:	1
License:	GPL
Group:		-
Source0:	http://ep09.pld-linux.org/~havner/%{name}-%{version}.tar.bz2
# Source0-md5:	f0bc5023d278c3c39dcdbca9e9539c78
Requires:	dml
Obsoletes:	livecd-installed
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Scripts for PLD LiveCD:
- init script
- HDD installer
- functions for above

%description -l pl
Skrypty dla PLD LiveCD
- skrypt init
- instalator na HDD
- funcje dla powy¿szych

%prep
%setup -q -n livecd

%build

%install
rm -rf $RPM_BUILD_ROOT
# create directories if necessary
install -d $RPM_BUILD_ROOT{%{_initrddir},%{_sbindir}}
install livecd $RPM_BUILD_ROOT%{_initrddir}
install functions-live $RPM_BUILD_ROOT%{_initrddir}
install rc.live $RPM_BUILD_ROOT/etc/rc.d/
install installer/installer.sh $RPM_BUILD_ROOT%{_sbindir}/livecd-installer.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del %{name}
fi

%postun

%files
%defattr(644,root,root,755)
%{_initrddir}/*
%attr(755,root,root) %{_initrddir}/livecd
%{_initrddir}/functions-live
%attr(755,root,root) /etc/rc.d/rc.live
%attr(755,root,root) %{_sbindir}/*
