Summary:	A program for performing checks against RBL-style blacklists
Name:		rblcheck
Version:	1.5
Release:	%mkrel 14
License:	GPL
Group:		Networking/Other
URL:		http://rblcheck.sourceforge.net/
Source0:	%{name}-%{version}.tar.bz2
Source1:	rblcheckrc
# Change the text "RBL filtered by" to "listed by"
# (RBL is a trademark of MAPS LLC.)
# 'listed by' is more accurate
Patch1:		rblcheck-texttweak.patch
# Fix broken code for looking up TXT records, code borrowed
# from Ian Gulliver's "firedns" library (GPL), which can be found at:
# http://firestuff.org/
Patch2:		rblcheck-txt.patch
# Comes from a post to the rblcheck users mailing list. See:
# http://sourceforge.net/mailarchive/forum.php?thread_id=1371771&forum_id=4256
Patch3:		rblcheck-names.patch
# Compile fix for x86_64 systems
Patch4:		rblcheck-1.5-res_query.patch
BuildRequires:	docbook-utils
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Rblcheck is a lightweight C program for performing checks against RBL-style IP
address blacklists. It works well in conjunction with Procmail for filtering
unwanted bulk email. 

This package also includes several tools that try to extract an originating IP
address from e-mail header. See %{_bindir}/origip-* and the documentation

%prep

%setup -q -n %{name}-%{version}
%patch1 -p1 -b .texttweak
%patch2 -p0 -b .txt
%patch3 -p0 -b .names
%patch4 -p1 -b .res_query

cp %{SOURCE1} .

%build

%configure

%make

%make -C utils/qmail

%make -C docs html/index.html
mv docs/html/rblcheck html

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sysconfdir}

install -m0755 rbl %{buildroot}%{_bindir}/
install -m0755 rblcheck %{buildroot}%{_bindir}/
install -m0755 utils/qmail/origip.awk %{buildroot}%{_bindir}/origip-qmail.awk
install -m0755 utils/qmail/origip %{buildroot}%{_bindir}/origip-qmail
install -m0755 utils/sendmail/origip.pl %{buildroot}%{_bindir}/origip-sendmail.pl
install -m0644 rblcheckrc %{buildroot}%{_sysconfdir}/rblcheckrc

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README html utils/test*.sh
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/rblcheckrc
%{_bindir}/rbl
%{_bindir}/rblcheck
%{_bindir}/origip-*


%changelog
* Tue Dec 07 2010 Oden Eriksson <oeriksson@mandriva.com> 1.5-14mdv2011.0
+ Revision: 614702
- the mass rebuild of 2010.1 packages

* Sat Dec 26 2009 Oden Eriksson <oeriksson@mandriva.com> 1.5-13mdv2010.1
+ Revision: 482519
- don't hardcode rbl services
- nuke dead rbl services

* Tue Sep 08 2009 Thierry Vignaud <tv@mandriva.org> 1.5-12mdv2010.0
+ Revision: 433063
- rebuild

* Fri Aug 01 2008 Thierry Vignaud <tv@mandriva.org> 1.5-11mdv2009.0
+ Revision: 260091
- rebuild

* Fri Jul 25 2008 Thierry Vignaud <tv@mandriva.org> 1.5-10mdv2009.0
+ Revision: 247966
- rebuild

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 1.5-8mdv2008.1
+ Revision: 140744
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - fix summary-ended-with-dot


* Mon Feb 05 2007 Oden Eriksson <oeriksson@mandriva.com> 1.5-8mdv2007.0
+ Revision: 116377
- Import rblcheck

* Mon Feb 05 2007 Oden Eriksson <oeriksson@mandriva.com> 1.5-8mdv2007.1
- sync with fedora extras (1.5-12)

* Tue Jun 27 2006 Oden Eriksson <oeriksson@mandriva.com> 1.5-7mdv2007.0
- rebuild

* Wed May 11 2005 Oden Eriksson <oeriksson@mandriva.com> 1.5-6mdk
- added one x86_86 fix

* Sat Oct 16 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.5-5mdk
- rpmbuildupdated

