%bcond_without	home_etc	# without home_etc support
Summary:	An open source reimplementation of the Microprose game "Transport Tycoon Deluxe"
Summary(pl):	Otwarta reimplementacja gry Transport Tycoon Deluxe
Name:		openttd
Version:	0.3.4
Release:	1
License:	GPL
Group:		X11/Applications/Games
#Source0:	http://dl.sf.net/openttd/%{name}-%{version}.tar.bz2
Source0:	http://osdn.dl.sourceforge.net/sourceforge/openttd/openttd-0.3.4.tar.bz
# Source0-md5:	14a4761593ac31418454c9cc1fe8a8bb
Patch0:		%{name}-home_etc.patch
URL:		http://www.openttd.com/
BuildRequires:	SDL-devel
%{?with_home_etc:BuildRequires:	home-etc-devel}
BuildRequires:	libpng-devel
BuildRequires:	sed >= 4
BuildRequires:	unzip
BuildRequires:	zlib-devel
Requires:	TiMidity++
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
openttd is modeled after the original Transport Tycoon game by Chris
Sawyer and enhances the game experience dramatically. Many features
were inspired by TTDPatch while others are original.

It requires the original Transport Tycoon Deluxe data files.

%description -l pl
openttd powsta³ na bazie gry Transport Tycoon stworzonej przez Chrisa
Sawyera, jego grywalno¶æ jest jednak du¿o wiêksza. Wiele rzeczy
zosta³o zainspirowanych przez TTDPatch, du¿o jest jednak oryginalnych
pomys³ów.

Do uruchomienia wymagane s± pliki danych z Transport Tycoon Deluxe.

%prep
%setup -q
%{?with_home_etc:%patch0 -p1}

# Let's pldize
sed -i 's/:Unix/:PLD Linux/' lang/*

%build
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} `sdl-config --cflags`" \
	LDFLAGS="%{rpmldflags}" \
	GAME_DATA_DIR="%{_datadir}/%{name}/" \
	PERSONAL_DIR=".%{name}" \
	%{?with_home_etc:WITH_HOME_ETC=1} \
	USE_HOMEDIR=1 \
	WITH_NETWORK=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name}/{data,gm,lang,scripts}}

install openttd $RPM_BUILD_ROOT%{_bindir}

install data/* $RPM_BUILD_ROOT%{_datadir}/%{name}/data
install lang/*.lng $RPM_BUILD_ROOT%{_datadir}/%{name}/lang
install scripts/* $RPM_BUILD_ROOT%{_datadir}/%{name}/scripts

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc changelog.txt readme.txt docs/{Manual.txt,console.txt,multiplayer.txt}
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
