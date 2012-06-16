#
# Conditional build:
%bcond_without	home_etc	# without home_etc support
#
Summary:	An open source reimplementation of the Microprose game "Transport Tycoon Deluxe"
Summary(pl.UTF-8):	Otwarta reimplementacja gry Transport Tycoon Deluxe
Name:		openttd
Version:	1.2.1
Release:	1
License:	GPL v2+
Group:		X11/Applications/Games
Source0:	http://binaries.openttd.org/releases/%{version}/%{name}-%{version}-source.tar.xz
# Source0-md5:	66b54e0293594aab90085db113cc2dd3
Source1:	%{name}.desktop
Source2:	%{name}-server.desktop
Patch0:		%{name}-home_etc.patch
Patch1:		%{name}-libiconv.patch
URL:		http://www.openttd.org/
BuildRequires:	SDL-devel
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel
%{?with_home_etc:BuildRequires:	home-etc-devel}
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	lzo-devel
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
Requires:	%{name}-data = %{version}-%{release}
Suggests:	%{name}-ai
Suggests:	%{name}-opengfx
Suggests:	%{name}-openmsx
Suggests:	%{name}-opensfx
Suggests:	TiMidity++
Provides:	%{name}-binary = %{version}-%{release}
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

%description server
This package contains OpenTTD dedicated server. Note that
graphics-enabled OpenTTD client also has this functionality.

%description server -l pl.UTF-8
Ten pakiet zawiera dedykowany serwer OpenTTD. Należy zwrócić uwagę, że
graficzny klient OpenTTD również zawiera taką funkcjonalność.

%prep
%setup -q
%{?with_home_etc:%patch0 -p1}
%patch1 -p1

# Let's pldize
find src/lang/ -type f -exec %{__sed} -i 's/:Unix/:PLD Linux/' \{\} \;

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
	--enable-dedicated \
	--without-allegro \
	--without-sdl \
	--with-zlib \
	--without-png \
	--without-freetype \
	--without-fontconfig \
	--without-libtimidity

%{__make} \
	MANUAL_CONFIG=1 \
	INSTALL=1 \
	VERBOSE=1

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
	--without-allegro \
	--with-sdl \
	--with-zlib \
	--with-png \
	--with-freetype \
	--with-fontconfig \
	--without-libtimidity \
	--with-iconv \
	--with-midi=%{_bindir}/timidity

%{__make} \
	MANUAL_CONFIG=1 \
	INSTALL=1 \
	VERBOSE=1

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_mandir}/man6,%{_pixmapsdir}}
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/{ai/library,scenario/heightmap}

%{__make} install \
	INSTALL_DIR=$RPM_BUILD_ROOT \
	INSTALL=1 \
	VERBOSE=1 \
	PREFIX="/" \

install bin/openttd-dedicated $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
install docs/openttd.6 $RPM_BUILD_ROOT%{_mandir}/man6
install media/openttd.256.png $RPM_BUILD_ROOT%{_pixmapsdir}/openttd.png

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%doc changelog.txt known-bugs.txt readme.txt docs/multiplayer.txt
%attr(755,root,root) %{_bindir}/%{name}
%{_desktopdir}/%{name}.desktop
%{_mandir}/man6/openttd.*
%{_iconsdir}/*/*/*/openttd.png

%files data
%defattr(644,root,root,755)
%doc bin/scripts
%{_datadir}/%{name}
%{_pixmapsdir}/openttd.*

%files server
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}-dedicated
%{_desktopdir}/%{name}-server.desktop
