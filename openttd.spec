%bcond_without	home_etc	# without home_etc support
Summary:	An open source clone of the Microprose game "Transport Tycoon Deluxe"
Summary(pl):	Otwarty klon gry Transport Tycoon Deluxe
Name:		openttd
Version:	0.3.2.1
Release:	3
License:	GPL
Group:		X11/Applications/Games
#Source0:	http://dl.sf.net/openttd/%{name}-%{version}.tbz
Source0:	%{name}.tar.bz2
# Source0-md5:	ee15b3149cafcbda4ee69e117f7c1b50
Source1:	http://dl.sf.net/openttd/%{name}-useful.zip
# Source1-md5:	070d66ed5086515a45f0a40a25c28771
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-home_etc.patch
URL:		http://www.openttd.com/
Requires:	TiMidity++
BuildRequires:	SDL-devel
%{?with_home_etc:BuildRequires:	home-etc-devel}
BuildRequires:	libpng-devel
BuildRequires:	sed >= 4
BuildRequires:	unzip
BuildRequires:	zlib-devel
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
%setup -q -n %{name}
%patch0 -p1
%{?with_home_etc:%patch1 -p1}

unzip %{SOURCE1} -d useful

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
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name}/{data,gm,lang}}

install ttd $RPM_BUILD_ROOT%{_bindir}

install data/* $RPM_BUILD_ROOT%{_datadir}/%{name}/data
install lang/*.lng $RPM_BUILD_ROOT%{_datadir}/%{name}/lang
install useful/opntitle.dat $RPM_BUILD_ROOT%{_datadir}/%{name}/data

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc changelog.txt readme.txt docs/Manual.txt
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
