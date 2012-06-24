%bcond_without	home_etc	# without home_etc support
Summary:	An open source reimplementation of the Microprose game "Transport Tycoon Deluxe"
Summary(pl):	Otwarta reimplementacja gry Transport Tycoon Deluxe
Name:		openttd
Version:	0.3.3
Release:	1
License:	GPL
Group:		X11/Applications/Games
Source0:	http://dl.sf.net/openttd/%{name}-%{version}.tar.bz2
# Source0-md5:	141064174eb9dea3435c273012bc8882
Source1:	http://dl.sf.net/openttd/%{name}-useful.zip
# Source1-md5:	070d66ed5086515a45f0a40a25c28771
Patch0:		%{name}-home_etc.patch
Patch1:		%{name}-endian.patch
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
openttd powsta� na bazie gry Transport Tycoon stworzonej przez Chrisa
Sawyera, jego grywalno�� jest jednak du�o wi�ksza. Wiele rzeczy
zosta�o zainspirowanych przez TTDPatch, du�o jest jednak oryginalnych
pomys��w.

Do uruchomienia wymagane s� pliki danych z Transport Tycoon Deluxe.

%prep
%setup -q
%{?with_home_etc:%patch0 -p1}
%patch1 -p1

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
