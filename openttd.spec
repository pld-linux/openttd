%define		snap	20041120
%bcond_without	home_etc	# without home_etc support
Summary:	An open source reimplementation of the Microprose game "Transport Tycoon Deluxe"
Summary(pl):	Otwarta reimplementacja gry Transport Tycoon Deluxe
Name:		openttd
Version:	0.3.4
Release:	1.%{snap}.1
License:	GPL
Group:		X11/Applications/Games
#Source0:	http://dl.sf.net/openttd/%{name}-%{version}.tar.bz2
Source0:	%{name}-%{snap}.tar.bz2
# Source0-md5:	a19eff4336bff73ce6941c8de398cb54
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
%setup -q -n %{name}
%{?with_home_etc:%patch0 -p1}

# Let's pldize
sed -i 's/:Unix/:PLD Linux/' lang/*

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
	WITH_NETWORK=1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DEST_DIR=$RPM_BUILD_ROOT \
	INSTALL=1 \
	PREFIX="/" \
	BINARY_DIR="%{_bindir}" \
	DATA_DIR="%{_datadir}/%{name}/"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc changelog.txt readme.txt docs/{Manual.txt,console.txt,multiplayer.txt}
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
