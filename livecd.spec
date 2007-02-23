Summary:	PLD LiveCD scripts
Summary(pl.UTF-8):	Skrypty PLD LiveCD
Name:		livecd
Version:	1.91
Release:	1
License:	GPL
Group:		Base
Source0:	http://ep09.pld-linux.org/~havner/%{name}-%{version}.tar.bz2
# Source0-md5:	a5fff13c0dda53b1669715dd03f52bfd
Source1:	http://developer.linuxtag.net/knoppix/sources/ddcxinfo-knoppix_0.6-5.tar.gz
# Source1-md5:	a397ca0ab56e83dd0fdeb4d0a84b8c9e
Requires:	rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-common
Requires:	%{name}-detect
Obsoletes:	%{name}-installed
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Scripts for PLD LiveCD:
- init script
- HDD installer

%description -l pl.UTF-8
Skrypty dla PLD LiveCD
- skrypt init
- instalator na HDD

%package common
Summary:	Functions for PLD LiveCD scripts
Summary(pl.UTF-8):	Funkcje dla skryptów PLD LiveCD
Group:		Applications/System

%description common
Functions for PLD LiveCD scripts.

%description common -l pl.UTF-8
Funkcje dla skryptów PLD LiveCD.

%package detect
Summary:	PCI detection program for PLD LiveCD
Summary(pl.UTF-8):	Program do wykrywania PCI dla PLD LiveCD
Group:		Applications/System

%description detect
PCI detection program for PLD LiveCD.

%description detect -l pl.UTF-8
Program do wykrywania PCI dla PLD LiveCD.

%package remaster
Summary:	PLD LiveCD remastering scripts
Summary(pl.UTF-8):	Skrypty do remasteringu PLD LiveCD
Group:		Applications/System
Requires:	busybox
Requires:	cdrtools-mkisofs
Requires:	squashfs
Requires:	%{name}-common

%description remaster
Scripts for remastering PLD LiveCD.

%description remaster -l pl.UTF-8
Skrypty do remasteringu PLD LiveCD.

%prep
%setup -q -a 1

%build
%{__cc} %{rpmldflags} %{rpmcflags} detect/detect.c -o livecd-detect
cd ddcxinfo-knoppix-0.6
%{__make} ddcxinfo

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_initrddir},%{_sbindir},/etc/{sysconfig,live-alt}} \
		$RPM_BUILD_ROOT{%{_desktopdir},%{_sbindir},/live}

install livecd $RPM_BUILD_ROOT%{_initrddir}
install functions-live $RPM_BUILD_ROOT%{_initrddir}
install rc.live $RPM_BUILD_ROOT/etc/rc.d
install installer/installer.sh $RPM_BUILD_ROOT%{_sbindir}/livecd-installer.sh
install installer/livecd-installer.desktop $RPM_BUILD_ROOT%{_desktopdir}
install livecd.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/livecd

install livecd-detect $RPM_BUILD_ROOT%{_sbindir}
install ddcxinfo-knoppix-0.6/ddcxinfo $RPM_BUILD_ROOT%{_sbindir}/livecd-ddcxinfo

install remaster/livecd_chroot $RPM_BUILD_ROOT%{_sbindir}/livecd-chroot.sh
install remaster/livecd_gen_iso $RPM_BUILD_ROOT%{_sbindir}/livecd-gen-iso.sh
install remaster/livecd_gen_initrd $RPM_BUILD_ROOT%{_sbindir}/livecd-gen-initrd.sh
install remaster/livecd_remaster_prep $RPM_BUILD_ROOT%{_sbindir}/livecd-remaster-prep.sh

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
%dir /etc/live-alt
%attr(754,root,root) /etc/rc.d/rc.live
%dir /live
%attr(755,root,root) %{_sbindir}/livecd-installer.sh
%{_desktopdir}/*.desktop
/etc/sysconfig/livecd

%files common
%defattr(644,root,root,755)
%{_initrddir}/functions-live

%files detect
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/livecd-detect
%attr(755,root,root) %{_sbindir}/livecd-ddcxinfo

%files remaster
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/livecd-chroot.sh
%attr(755,root,root) %{_sbindir}/livecd-gen-iso.sh
%attr(755,root,root) %{_sbindir}/livecd-gen-initrd.sh
%attr(755,root,root) %{_sbindir}/livecd-remaster-prep.sh
