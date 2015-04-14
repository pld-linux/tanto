Summary:	Takes monitoring data from Nagios-plugins to push with NSCA (Nagios or Icinga) or WS-Shinken
Name:		tanto
Version:	1.1
Release:	1
License:	AGPL v3
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/t/tanto/%{name}-%{version}.tar.gz
# Source0-md5:	480a1549803eb96cf221847ac10c6d3b
URL:		https://github.com/Eyepea/tanto
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	python-argparse >= 1.1
Requires:	python-configobj >= 4.7.2
Requires:	python-pynsca >= 1.2
Requires:	python-requests >= 0.10.1
Suggests:	crondaemon
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
To monitor the servers with Shinken, Nagios or Icinga, system
administrators usually configure active checks of the monitored
servers. It means the monitoring system must have a direct network
access to the monitored server.

%prep
%setup -q

%{__rm} -r %{name}.egg-info

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},/etc/cron.d}
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

# python setup can't install this properly, just puts everything under %{_prefix}
# there's old (2009) proposal, which is not implemented:
# https://wiki.python.org/moin/Distutils/Proposals/AutoconfLikeOptions
mv $RPM_BUILD_ROOT{%{_prefix}%{_sysconfdir}/%{name}/*,%{_sysconfdir}/%{name}}
mv $RPM_BUILD_ROOT{%{_prefix}/etc/cron.d/*,/etc/cron.d}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst LICENSE
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/cron.d/%{name}
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/inputs
%dir %{_sysconfdir}/%{name}/outputs
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/logging.ini
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/inputs/nagios_plugins.cfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/outputs/email.cfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/outputs/nsca.cfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/outputs/ws_shinken.cfg

%attr(755,root,root) %{_bindir}/tanto

%dir %{py_sitescriptdir}/monitoring_agent
%{py_sitescriptdir}/monitoring_agent/*.py[co]
%dir %{py_sitescriptdir}/monitoring_agent/inputs
%{py_sitescriptdir}/monitoring_agent/inputs/*.py[co]
%dir %{py_sitescriptdir}/monitoring_agent/inputs/configspecs
%{py_sitescriptdir}/monitoring_agent/inputs/configspecs/nagios_plugins.cfg
%dir %{py_sitescriptdir}/monitoring_agent/outputs
%{py_sitescriptdir}/monitoring_agent/outputs/*.py[co]
%dir %{py_sitescriptdir}/monitoring_agent/outputs/configspecs
%{py_sitescriptdir}/monitoring_agent/outputs/configspecs/email.cfg
%{py_sitescriptdir}/monitoring_agent/outputs/configspecs/nsca.cfg
%{py_sitescriptdir}/monitoring_agent/outputs/configspecs/ws_shinken.cfg
%{py_sitescriptdir}/tanto-%{version}-py*.egg-info
