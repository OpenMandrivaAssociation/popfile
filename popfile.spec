%define name	popfile
%define version	0.22.4
%define release	%mkrel 1

Summary:	Automatic Email Classification
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Networking/Mail
Source0:	popfile-%{version}.zip
Source1:	popfile_16x16.png
Source2:	popfile_32x32.png
Source3:	popfile_48x48.png
Source4:	popfile.init.bz2
URL:		http://popfile.sourceforge.net/
Requires(post,preun):	rpm-helper
BuildRequires:	perl
BuildRequires:	unzip
Buildarch: 	noarch

%description
POPFile is an email classification tool with a Naive Bayes
classifier, a POP3 proxy and a web interface. It runs on most
platforms and with most email clients.

%prep

%setup -q -c %{name}-%{version}

# fix dir perms
find . -type d | xargs chmod 755

# fix file perms
find . -type f | xargs chmod 644

# fix exec file perms
find . -type f -name "*.pl" | xargs chmod 755

# strip away annoying ^M
for i in pm pl html css msg; do
    find . -type f -name "*.${i}" | xargs perl -p -i -e 's/\r//'
done

%build

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_menudir}
install -d %{buildroot}%{_liconsdir}
install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_miconsdir}
install -d %{buildroot}%{_datadir}/%{name}

bzcat %{SOURCE4} > %{buildroot}%{_initrddir}/%{name}
chmod 755 %{buildroot}%{_initrddir}/%{name}

cp -aRf * %{buildroot}%{_datadir}/%{name}/

# install script to call the web interface from the menu.
cat > %{buildroot}%{_datadir}/%{name}/%{name} << EOF
#!/bin/sh
url='http://localhost:8080/'
if ! [ -z "\$BROWSER" ] && ( which \$BROWSER ); then
  browser=\`which \$BROWSER\`
elif [ -x /usr/bin/netscape ]; then
  browser=/usr/bin/netscape
elif [ -x /usr/bin/konqueror ]; then
  browser=/usr/bin/konqueror
elif [ -x /usr/bin/lynx ]; then
  browser='xterm -bg black -fg white -e lynx'
elif [ -x /usr/bin/links ]; then
  browser='xterm -bg black -fg white -e links'
else
  xmessage "No web browser found, install one or set the BROWSER environment variable!"
  exit 1
fi
\$browser \$url
EOF
chmod 755 %{buildroot}%{_datadir}/%{name}/%{name}

# fix menu stuff
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=POPFile - Automatic Email Classification
Comment=An email classification tool with a Naive Bayes classifier
Exec=%{_datadir}/%{name}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=
EOF


install -m0644 %{SOURCE1} %{buildroot}%{_miconsdir}/%{name}.png
install -m0644 %{SOURCE2} %{buildroot}%{_iconsdir}/%{name}.png
install -m0644 %{SOURCE3} %{buildroot}%{_liconsdir}/%{name}.png

# clean up
rm -f %{buildroot}%{_datadir}/%{name}/v%{version}.change

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%clean 
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc *.change
%config(noreplace) %attr(0755,root,root) %{_initrddir}/%{name}
%{_miconsdir}/*
%{_iconsdir}/*
%{_liconsdir}/*
%{_datadir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop 


