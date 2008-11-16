#
# ToDo:
# - review -home_etc.patch
#
# Conditional build:
%bcond_without	home_etc	# without home_etc support
#
Summary:	An open source reimplementation of the Microprose game "Transport Tycoon Deluxe"
Summary(pl.UTF-8):	Otwarta reimplementacja gry Transport Tycoon Deluxe
Name:		openttd
Version:	0.6.2
Release:	0.1
License:	GPL
Group:		X11/Applications/Games
Source0:	http://dl.sourceforge.net/openttd/%{name}-%{version}-source.tar.bz2
# Source0-md5:	0678c02c92101616dbd710438dbfac43
Source1:	http://dl.sourceforge.net/openttd/%{name}-0.4.8-scenarios.tar.bz2
# Source1-md5:	34e8cb13ce1d4e6b5b24887c628c1ac8
Source2:	http://dl.sourceforge.net/openttd/%{name}-0.5.0-scenarios.tar.bz2
# Source2-md5:	37892f1fdded957f956766642a9e877d
Source3:	%{name}.desktop
Source4:	%{name}-server.desktop
Patch0:		%{name}-home_etc.patch
Patch1:		%{name}-libiconv.patch
URL:		http://www.openttd.com/
BuildRequires:	SDL-devel
BuildRequires:	freetype-devel
%{?with_home_etc:BuildRequires:	home-etc-devel}
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	sed >= 4
BuildRequires:	zlib-devel
Requires:	%{name}-data = %{version}-%{release}
Provides:	%{name}-binary = %{version}-%{release}
Obsoletes:	openttd-server
Suggests:	TiMidity++
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
cd bin/scenario
tar xvjf %{SOURCE1}
tar xvjf %{SOURCE2}
mv openttd-0.4.8-RC1-scenarios/* .
rmdir openttd-0.4.8-RC1-scenarios heightmap
cd ../..
%{?with_home_etc:%patch0 -p1}
%patch1 -p1

# Let's pldize
find src/lang/ -type f -exec sed -i 's/:Unix/:PLD Linux/' \{\} \;

%build

# dedicated
./configure \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcxxflags}" \
	LDFLAGS="%{rpmldflags}" \
	--cc-host="%{__cc}" \
	--cc-build="%{__cc}" \
	--cxx-host="%{__cxx}" \
	--cxx-build="%{__cxx}" \
	--disable-strip \
	--prefix-dir="%{_prefix}" \
	--binary-dir=bin \
	--data-dir=share/openttd \
	--icon-dir=share/pixmaps \
	--install-dir=$RPM_BUILD_ROOT \
	--os=UNIX \
	--without-sdl \
	--without-zlib \
	--without-png \
	--without-freetype \
	--without-fontconfig

%{__make} \
	MANUAL_CONFIG=1 \
	INSTALL=1 \
	VERBOSE=1 \
	DEDICATED=1

mv bin/openttd{,-dedicated}

# client
rm -f Makefile.config
%{__make} clean
./configure \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcxxflags} $(sdl-config --cflags) -I/usr/include/freetype2" \
	LDFLAGS="%{rpmldflags}" \
	--cc-host="%{__cc}" \
	--cc-build="%{__cc}" \
	--cxx-host="%{__cxx}" \
	--cxx-build="%{__cxx}" \
	--disable-strip \
	--prefix-dir="%{_prefix}" \
	--binary-dir=bin \
	--data-dir=share/openttd \
	--icon-dir=share/pixmaps \
	--install-dir=$RPM_BUILD_ROOT \
	--os=UNIX \
	--with-sdl \
	--with-zlib \
	--with-png \
	--with-freetype \
	--with-fontconfig \
	--with-iconv \
	--with-midi=/usr/bin/timidity

%{__make} \
	MANUAL_CONFIG=1 \
	INSTALL=1 \
	VERBOSE=1 \
	DEDICATED=0

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_mandir}/man6,%{_pixmapsdir},%{_datadir}/%{name}/scenario}

%{__make} install \
	INSTALL_DIR=$RPM_BUILD_ROOT \
	INSTALL=1 \
	VERBOSE=1 \
	PREFIX="/" \

install bin/openttd-dedicated $RPM_BUILD_ROOT%{_bindir}
install bin/scenario/* $RPM_BUILD_ROOT%{_datadir}/%{name}/scenario
install %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}
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
%doc bin/scripts
%{_datadir}/%{name}
%{_pixmapsdir}/*

%files server
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}-dedicated
%{_desktopdir}/%{name}-server.desktop
