Summary:	A program for performing checks against RBL-style blacklists
Name:		rblcheck
Version:	1.5
Release:	%mkrel 12
License:	GPL
Group:		Networking/Other
URL:		http://rblcheck.sourceforge.net/
Source0:	%{name}-%{version}.tar.bz2
Source1:	rblcheckrc
Patch0:		%{name}-%{version}-sites.patch
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Rblcheck is a lightweight C program for performing checks against RBL-style IP
address blacklists. It works well in conjunction with Procmail for filtering
unwanted bulk email. 

This package also includes several tools that try to extract an originating IP
address from e-mail header. See %{_bindir}/origip-* and the documentation

%prep

%setup -q -n %{name}-%{version}
%patch0 -p0
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
%{_bindir}/rblcheck
%{_bindir}/origip-*


