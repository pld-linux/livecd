Summary:	PLD LiveCD scripts
Summary(pl):	Skrypty PLD LiveCD
Name:		livecd
Version:	1.0
Release:	1
License:	GPL
Group:		Base
Source0:	http://ep09.pld-linux.org/~havner/%{name}-%{version}.tar.bz2
# Source0-md5:	f0bc5023d278c3c39dcdbca9e9539c78
Source1:	http://developer.linuxtag.net/knoppix/sources/ddcxinfo-knoppix_0.6-5.tar.gz
# Source1-md5:	a397ca0ab56e83dd0fdeb4d0a84b8c9e
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	dml
Requires:	${name}-common
Requires:	${name}-detect
Obsoletes:	%{name}-installed
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Scripts for PLD LiveCD:
- init script
- HDD installer

%description -l pl
Skrypty dla PLD LiveCD
- skrypt init
- instalator na HDD

%package common
Summary:	Functions for PLD LiveCD scripts
Summary(pl):	Funkcje dla skryptów PLD LiveCD
Group:		Applications/System

%description common
Functions for PLD LiveCD scripts.

%description common -l pl
Funkcje dla skryptów PLD LiveCD.

%package detect
Summary:	PCI detection program for PLD LiveCD
Summary(pl):	Program do wykrywania PCI dla PLD LiveCD
Group:		Applications/System

%description detect
PCI detection program for PLD LiveCD.

%description detect -l pl
Program do wykrywania PCI dla PLD LiveCD.

%package remaster
Summary:	PLD LiveCD remastering scripts
Summary(pl):	Skrypty do remasteringu PLD LiveCD
Group:		Applications/System
Requires:	busybox
Requires:	cdrtools-mkisofs
Requires:	squashfs
Requires:	%{name}-common

%description remaster
Scripts for remastering PLD LiveCD.

%description remaster -l pl
Skrypty do remasteringu PLD LiveCD.

%prep
%setup -q -n %{name} -a 1

%build
%{__cc} %{rpmldflags} %{rpmcflags} detect/detect.c -o livecd-detect
cd ddcxinfo-knoppix-0.6
%{__make} ddcxinfo

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_initrddir},%{_sbindir},/etc/sysconfig} \
		$RPM_BUILD_ROOT%{{_desktopdir},%{_sbindir},%{_bindir}}

install livecd $RPM_BUILD_ROOT%{_initrddir}
install functions-live $RPM_BUILD_ROOT%{_initrddir}
install rc.live $RPM_BUILD_ROOT/etc/rc.d
install installer/installer.sh $RPM_BUILD_ROOT%{_sbindir}/livecd-installer.sh
install installer/livecd-installer.desktop $RPM_BUILD_ROOT%{_desktopdir}
install livecd.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/livecd

install livecd-detect $RPM_BUILD_ROOT%{_bindir}
install ddcxinfo-knoppix-0.6/ddcxinfo $RPM_BUILD_ROOT%{_bindir}/livecd-ddcxinfo

install livecd_gen_iso $RPM_BUILD_ROOT%{_sbindir}/livecd-gen-iso.sh
install livecd_remaster_prep $RPM_BUILD_ROOT%{_sbindir}/livecd-remaster-prep.sh
install livecd_symlinks $RPM_BUILD_ROOT%{_sbindir}/livecd-symlinks.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_initrddir}/livecd
%attr(755,root,root) /etc/rc.d/rc.live
%attr(755,root,root) %{_sbindir}/*
%{_desktopdir}/*
/etc/sysconfig/livecd

%files common
%defattr(644,root,root,755)
%{_initrddir}/functions-live

%files detect
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*

%files remaster
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*.sh
