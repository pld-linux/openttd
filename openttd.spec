Summary:	An open source reimplementation of the Microprose game "Transport Tycoon Deluxe"
Summary(pl.UTF-8):	Otwarta reimplementacja gry Transport Tycoon Deluxe
Name:		openttd
Version:	13.3
Release:	2
License:	GPL v2+
Group:		X11/Applications/Games
Source0:	https://cdn.openttd.org/openttd-releases/%{version}/%{name}-%{version}-source.tar.xz
# Source0-md5:	9d48c61ff9034dc3ee42128ecb2d3da8
Source1:	%{name}.desktop
Source2:	%{name}-server.desktop
Patch0:		%{name}-create-grf.patch
URL:		http://www.openttd.org/
BuildRequires:	SDL2-devel
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel
BuildRequires:	grfcodec >= 6.0.2
BuildRequires:	libicu-devel
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
%patch0 -p1

# Let's pldize
find src/lang/ -type f -exec %{__sed} -i 's/:Unix/:PLD Linux/' \{\} \;

%build

# dedicated
install -d dedicated
cd dedicated
%cmake .. \
	-DOPTION_DEDICATED:BOOL=ON \
	-DCMAKE_INSTALL_BINDIR="bin" \
	-DCMAKE_INSTALL_DATADIR="share"

%{__make}

mv openttd{,-dedicated}

cd ..

# client
install -d build
cd build
%cmake .. \
	-DCMAKE_INSTALL_BINDIR="bin" \
	-DCMAKE_INSTALL_DATADIR="share" \
	-DOPTION_DEDICATED:BOOL=OFF

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_mandir}/man6,%{_pixmapsdir}}
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/{ai/library,scenario/heightmap}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install dedicated/openttd-dedicated $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
install docs/openttd.6 $RPM_BUILD_ROOT%{_mandir}/man6
install media/openttd.256.png $RPM_BUILD_ROOT%{_pixmapsdir}/openttd.png

%{__rm} $RPM_BUILD_ROOT%{_docdir}/{COPYING.md,README.md,changelog.txt,known-bugs.txt,multiplayer.md}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%doc COPYING.md changelog.txt known-bugs.txt README.md docs/multiplayer.md
%attr(755,root,root) %{_bindir}/%{name}
%{_desktopdir}/%{name}.desktop
%{_mandir}/man6/openttd.*
%{_iconsdir}/hicolor/*x*/apps/openttd.png

%files data
%defattr(644,root,root,755)
%doc bin/scripts
%{_datadir}/%{name}
%{_pixmapsdir}/openttd.*

%files server
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}-dedicated
%{_desktopdir}/%{name}-server.desktop
