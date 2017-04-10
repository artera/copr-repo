Summary: Redis 2.0 protocol module
Name: nginx-mod-redis2
Version: 0.13
Release: 1%{?dist}
Vendor: Artera
URL: https://github.com/openresty/redis2-nginx-module

%define _modname            redis2
%define _nginxver           1.10.2
%define nginx_config_dir    %{_sysconfdir}/nginx
%define nginx_build_dir     %{_builddir}/nginx-%{_nginxver}
%define mod_build_dir       %{_builddir}/%{_modname}-%{version}

Source0: http://nginx.org/download/nginx-%{_nginxver}.tar.gz
Source1: https://github.com/openresty/redis2-nginx-module/archive/v%{version}/%{_modname}-%{version}.tar.gz

Patch0: https://github.com/openresty/redis2-nginx-module/commit/8cc7304787ae9542db4feb50d9e27beb485caa0f.patch

Requires: nginx
BuildRequires: nginx
BuildRequires: libtool
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: openssl-devel
BuildRequires: pcre-devel
BuildRequires: zlib-devel
BuildRequires: perl-devel
BuildRequires: gd-devel
BuildRequires: GeoIP-devel
BuildRequires: libxslt-devel
BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::Embed)
BuildRequires: gperftools-devel

License: BSD

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Redis 2.0 protocol module.

%prep
%setup -q -n nginx-%{_nginxver}
%setup -T -D -b 1 -n %{_modname}-nginx-module-%{version}
%patch0 -p1

%build
cd %{_builddir}/nginx-%{_nginxver}
./configure %(nginx -V 2>&1 | grep 'configure arguments' | sed -r 's@^[^:]+: @@') --add-dynamic-module=../%{_modname}-nginx-module-%{version}
make modules

%install
%{__rm} -rf %{buildroot}

%{__install} -Dm755 %{nginx_build_dir}/objs/ngx_http_redis2_module.so \
    $RPM_BUILD_ROOT%{_libdir}/nginx/modules/ngx_http_redis2_module.so

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/nginx/modules/*.so
