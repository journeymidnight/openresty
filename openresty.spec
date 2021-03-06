Name:		openresty
Version:	1.9.7.4
Release:	1%{?dist}
Summary:	a fast web app server by extending nginx

Group:		Productivity/Networking/Web/Servers
License:	BSD
URL:		openresty.org
Source0:	http://openresty.org/download/%{name}-%{version}.tar.gz
Source1:	https://github.com/brnt/openresty-rpm-spec/raw/master/nginx.init
Source2:        nginx.logrotate 
Source3:        nginx.service
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	sed openssl-devel pcre-devel readline-devel
Requires:	openssl pcre readline
Requires(pre):	shadow-utils

%define homedir %{_usr}/local/openresty

%description
OpenResty (aka. ngx_openresty) is a full-fledged web application server by bundling the standard Nginx core, lots of 3rd-party Nginx modules, as well as most of their external dependencies.


%prep
%setup -q


%build
./configure --with-pcre-jit --with-luajit --add-module=./bundle/ngx_cache_purge-2.3/
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/etc/init.d
sed -e 's/%NGINX_CONF_DIR%/%{lua: esc,qty=string.gsub(rpm.expand("%{homedir}"), "/", "\\/"); print(esc)}\/nginx\/conf/g' \
	-e 's/%NGINX_BIN_DIR%/%{lua: esc,qty=string.gsub(rpm.expand("%{homedir}"), "/", "\\/"); print(esc)}\/nginx\/sbin/g' \
	%{SOURCE1} > %{buildroot}/etc/init.d/nginx
install -D -m 644 %{SOURCE2} %{buildroot}/etc/logrotate.d/nginx.logrotate
install -D -m 644 %{SOURCE3} %{buildroot}/usr/lib/systemd/system/nginx.service

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
#%{homedir}/*

%attr(755,root,root) /etc/init.d/nginx
%attr(755,root,root) /etc/logrotate.d/nginx.logrotate
%attr(755,root,root) /usr/lib/systemd/system/nginx.service
%{homedir}/luajit/*
%{homedir}/lualib/*
%{homedir}/nginx
%{homedir}/nginx/html/*
%{homedir}/nginx/logs
%{homedir}/nginx/sbin
%{homedir}/nginx/sbin/nginx
%{homedir}/bin/resty

%{homedir}/nginx/conf
%{homedir}/nginx/conf/fastcgi.conf.default
%{homedir}/nginx/conf/fastcgi_params.default
%{homedir}/nginx/conf/mime.types.default
%{homedir}/nginx/conf/nginx.conf.default
%{homedir}/nginx/conf/scgi_params.default
%{homedir}/nginx/conf/uwsgi_params.default

%config %{homedir}/nginx/conf/fastcgi.conf
%config %{homedir}/nginx/conf/fastcgi_params
%config %{homedir}/nginx/conf/koi-utf
%config %{homedir}/nginx/conf/koi-win
%config %{homedir}/nginx/conf/mime.types
%config %{homedir}/nginx/conf/nginx.conf
%config %{homedir}/nginx/conf/scgi_params
%config %{homedir}/nginx/conf/uwsgi_params
%config %{homedir}/nginx/conf/win-utf


%postun


%changelog

