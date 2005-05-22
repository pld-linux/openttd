%bcond_without	home_etc	# without home_etc support
Summary:	An open source reimplementation of the Microprose game "Transport Tycoon Deluxe"
Summary(pl):	Otwarta reimplementacja gry Transport Tycoon Deluxe
Name:		openttd
Version:	0.4.0.1
Release:	1
License:	GPL
Group:		X11/Applications/Games
Source0:	http://dl.sf.net/openttd/%{name}-%{version}-source.tar.gz
# Source0-md5:	ddd9790c86b7ccc68f60761704cbcf81
Source1:	%{name}.desktop
Source2:	%{name}-server.desktop
Patch0:		%{name}-home_etc.patch
Patch1:		%{name}-personal-data.patch
URL:		http://www.openttd.com/
BuildRequires:	SDL-devel
%{?with_home_etc:BuildRequires:	home-etc-devel}
BuildRequires:	libpng-devel
BuildRequires:	sed >= 4
BuildRequires:	unzip
BuildRequires:	zlib-devel
Requires:	TiMidity++
Requires:	%{name}-data = %{version}-%{release}
Provides:	%{name}-binary = %{version}-%{release}
Obsoletes:	%{name}-server
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenTTD is modeled after the original Transport Tycoon game by Chris
Sawyer and enhances the game experience dramatically. Many features
were inspired by TTDPatch while others are original.

It requires the original Transport Tycoon Deluxe data files.

%description -l pl
OpenTTD powsta³ na bazie gry Transport Tycoon stworzonej przez Chrisa
Sawyera, jego grywalno¶æ jest jednak du¿o wiêksza. Wiele rzeczy
zosta³o zainspirowanych przez TTDPatch, du¿o jest jednak oryginalnych
pomys³ów.

Do uruchomienia wymagane s± pliki danych z Transport Tycoon Deluxe.

%package data
Summary:	OpenTTD data files
Summary(pl):	Pliki danych OpenTTD
Group:		X11/Applications/Games
Requires:	%{name}-binary = %{version}-%{release}

%description data
OpenTTD data files.

%description data -l pl
Pliki danych OpenTTD.

%package server
Summary:	OpenTTD dedicated server	
Summary(pl):	Dedykowany serwer OpenTTD
Group:		X11/Applications/Games
Requires:	%{name}-data = %{version}-%{release}
Provides:	%{name}-binary = %{version}-%{release}
Obsoletes:	%{name}

%description server
This package contains OpenTTD dedicated server. Note that
graphics-enabled OpenTTD client also has this functionality.

%description server -l pl
Ten pakiet zawiera dedykowany serwer OpenTTD. Nale¿y zwróciæ uwagê,
¿e graficzny klient OpenTTD równie¿ posiada t± funkcjonalno¶æ.

%prep
%setup -q
%{?with_home_etc:%patch0 -p1}
%patch1 -p1

# Let's pldize
find lang/ -type f -exec sed -i 's/:Unix/:PLD Linux/' \{\} \;

%build
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} `sdl-config --cflags`" \
	LDFLAGS="%{rpmldflags}" \
	INSTALL=1 \
	PREFIX="" \
	BINARY_DIR="%{_bindir}" \
	DATA_DIR="%{_datadir}/%{name}/" \
	PERSONAL_DIR=".%{name}" \
	%{?with_home_etc:WITH_HOME_ETC=1} \
	USE_HOMEDIR=1 \
	WITH_NETWORK=1 \
	WITH_SDL= \
	WITH_PNG= \
	DEDICATED=1

mv openttd openttd-dedicated

%{__make} clean
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} `sdl-config --cflags`" \
	LDFLAGS="%{rpmldflags}" \
	INSTALL=1 \
	PREFIX="" \
	BINARY_DIR="%{_bindir}" \
	DATA_DIR="%{_datadir}/%{name}/" \
	PERSONAL_DIR=".%{name}" \
	%{?with_home_etc:WITH_HOME_ETC=1} \
	USE_HOMEDIR=1 \
	WITH_NETWORK=1 \
	WITH_SDL=1 \
	WITH_PNG=1 \
	DEDICATED=0

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_mandir}/man6,%{_pixmapsdir},%{_datadir}/%{name}/scenario}

%{__make} install \
	DEST_DIR=$RPM_BUILD_ROOT \
	INSTALL=1 \
	PREFIX="/" \
	BINARY_DIR="%{_bindir}" \
	DATA_DIR="%{_datadir}/%{name}/"

install openttd-dedicated $RPM_BUILD_ROOT%{_bindir}
install scenario/* $RPM_BUILD_ROOT%{_datadir}/%{name}/scenario
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
install docs/openttd.6 $RPM_BUILD_ROOT%{_mandir}/man6
install media/openttd.256.png $RPM_BUILD_ROOT%{_pixmapsdir}/openttd.png

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc changelog.txt known-bugs.txt readme.txt docs/{Manual.txt,console.txt,multiplayer.txt}
%attr(755,root,root) %{_bindir}/%{name}
%{_desktopdir}/%{name}.desktop
%{_mandir}/man6/*

%files data
%defattr(644,root,root,755)
%doc scripts
%{_datadir}/%{name}
%{_pixmapsdir}/*

%files server
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}-dedicated
%{_desktopdir}/%{name}-server.desktop
