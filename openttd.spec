#
# Conditional build:
%bcond_without	home_etc	# without home_etc support
#
Summary:	An open source reimplementation of the Microprose game "Transport Tycoon Deluxe"
Summary(pl.UTF-8):	Otwarta reimplementacja gry Transport Tycoon Deluxe
Name:		openttd
Version:	0.5.3
Release:	0.1
License:	GPL
Group:		X11/Applications/Games
Source0:	http://dl.sourceforge.net/openttd/%{name}-%{version}-source.tar.bz2
# Source0-md5:	592c047903a3e7f17f95279f77b8a1dd
Source1:	%{name}.desktop
Source2:	%{name}-server.desktop
Patch0:		%{name}-home_etc.patch
Patch1:		%{name}-personal-data.patch
Patch2:		%{name}-pthread.patch
URL:		http://www.openttd.com/
BuildRequires:	SDL-devel
BuildRequires:	freetype-devel
%{?with_home_etc:BuildRequires:	home-etc-devel}
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	sed >= 4
BuildRequires:	zlib-devel
Requires:	%{name}-data = %{version}-%{release}
Requires:	TiMidity++
Provides:	%{name}-binary = %{version}-%{release}
Obsoletes:	openttd-server
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenTTD is modeled after the original Transport Tycoon game by Chris
Sawyer and enhances the game experience dramatically. Many features
were inspired by TTDPatch while others are original.

It requires the original Transport Tycoon Deluxe data files.

%description -l pl.UTF-8
OpenTTD powstał na bazie gry Transport Tycoon stworzonej przez Chrisa
Sawyera, jego grywalność jest jednak dużo większa. Wiele rzeczy
zostało zainspirowanych przez TTDPatch, dużo jest jednak oryginalnych
pomysłów.

Do uruchomienia wymagane są pliki danych z Transport Tycoon Deluxe.

%package data
Summary:	OpenTTD data files
Summary(pl.UTF-8):	Pliki danych OpenTTD
Group:		X11/Applications/Games
Requires:	%{name}-binary = %{version}-%{release}

%description data
OpenTTD data files.

%description data -l pl.UTF-8
Pliki danych OpenTTD.

%package server
Summary:	OpenTTD dedicated server
Summary(pl.UTF-8):	Dedykowany serwer OpenTTD
Group:		X11/Applications/Games
Requires:	%{name}-data = %{version}-%{release}
Provides:	%{name}-binary = %{version}-%{release}
Obsoletes:	openttd

%description server
This package contains OpenTTD dedicated server. Note that
graphics-enabled OpenTTD client also has this functionality.

%description server -l pl.UTF-8
Ten pakiet zawiera dedykowany serwer OpenTTD. Należy zwrócić uwagę,
że graficzny klient OpenTTD również posiada tą funkcjonalność.

%prep
%setup -q
%{?with_home_etc:%patch0 -p1}
%patch1 -p1
%patch2 -p0

%{__sed} 's/ifndef USE_HOMEDIR/ifdef USE_HOMEDIR/' -i Makefile
# Let's pldize
find lang/ -type f -exec sed -i 's/:Unix/:PLD Linux/' \{\} \;

%build
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} `sdl-config --cflags` -I/usr/include/freetype2" \
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
	WITH_FREETYPE= \
	WITH_FONTCONFIG= \
	VERBOSE=1 \
	DEDICATED=1

mv openttd openttd-dedicated

rm -f Makefile.config
%{__make} clean
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} `sdl-config --cflags` -I/usr/include/freetype2" \
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
	WITH_FREETYPE=1 \
	WITH_FONTCONFIG=1 \
	WITH_ICONV=1 \
	VERBOSE=1 \
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
##install scenario/* $RPM_BUILD_ROOT%{_datadir}/%{name}/scenario
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
install docs/openttd.6 $RPM_BUILD_ROOT%{_mandir}/man6
install media/openttd.256.png $RPM_BUILD_ROOT%{_pixmapsdir}/openttd.png

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc changelog.txt known-bugs.txt readme.txt docs/{Manual.txt,multiplayer.txt}
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
