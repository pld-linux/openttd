Summary:	An open source clone of the Microprose game "Transport Tycoon Deluxe"
Summary(pl):	Otwarty klon gry Transport Tycoon Deluxe
Name:		openttd
Version:	0.3.2.1
Release:	1
License:	GPL
Group:		X11/Applications/Games
Source0:	http://dl.sf.net/openttd/%{name}-%{version}.tbz
# Source0-md5:	db0011ac576874450c84843609f85d0b
URL:		http://www.openttd.com/
Requires:	TiMidity++
BuildRequires:	SDL-devel
BuildRequires:	libpng-devel
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
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} `sdl-config --cflags` -DDATA_DIR_PREFIX=\\\"%{_datadir}/%{name}/\\\"" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name}/{data,gm,lang}}

install ttd $RPM_BUILD_ROOT%{_bindir}

install data/* $RPM_BUILD_ROOT%{_datadir}/%{name}/data
install lang/*.lng $RPM_BUILD_ROOT%{_datadir}/%{name}/lang

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc changelog.txt readme.txt docs/Manual.txt
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
