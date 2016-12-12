# -*- coding: utf-8 -*-
###########################################################
# KEDJI Komlan Akpédjé
#
# SOA Stack components install script
# @depends: penv.py, unzip.py, optionparse.py in PYTHONPATH
#
# NEOXIA Maroc
###########################################################

"""usage: %prog [options]
    -z, --all:                 installe toute la plateforme
    -a, --ant:                 installe Ant
    -m, --maven:               installe Maven
    -u, --mule:                installe Mule
    -q, --activemq:            installe ActiveMQ
    -r, --hyperichq:           installe HypericHQ
    -i, --intalioServer:       installe le serveur Intalio
    -l, --liferayPortal:       installe Liferay-Portal
    -k, --liferaySdk:          installe Liferay-SDK (installe aussi le serveur Liferay et Ant)
    -y, --mysqlServer:         installe MySQL (configure aussi Liferay pour utiliser MySQL)
    -c, --mysql4liferay:       configure Liferay-Server pour utiliser une bdd MySQL existante (locale)
    -b, --libraries:           installe les librairies additionnelles (dll native Tomcat, etc)
    -t, --test:                affiche seulement les commandes, sans les exécuter
    -s, --source=c:\\packages: répertoire source des pacquets à installer
    -d, --dest=c:\\soastack:   répertoire de destination de l'installation
    -p, --password=neoxia:     mot de passe (le même pour tous. I know, it is stupid)
"""

import os, shutil, time
from os.path import join as pjoin
# custom modules (c:\eric\soft\scripts\python)
from penv import Penv
from unzip import extract
import optionparse

# Watch for port conflicts
# hyperic est sur 7080
# liferay est sur 9000
# ode (liferay) est sur 8080
# the braindead Intalio install has port information hard coded all over config files
# see here for a script to cahnge it:
# http://bpms.intalio.com/forums/installation/re-installing-intalio-server-using-alternate-port-s/view-3.html

# Package info
packages = {
            'mule': {
                     'zip': 'mule-standalone-2.2.0.zip',
                     'env': {'MULE_HOME': '${INSTALLDIR}', 'PATH': '%MULE_HOME%\\bin'}},
            'ant': {
                    'zip': 'apache-ant-1.7.1-bin.zip', 'dest': 'apache-ant-1.7.1',
                    'env': {
                            'ANT_HOME': '${INSTALLDIR}',
                            'ANT_OPTS': '-Xmx512m -XX:MaxPermSize=256',
                            'PATH':'%ANT_HOME%\\bin'}},
            'maven': {
                      'zip': 'apache-maven-2.1.0-bin.zip', 'dest': 'apache-maven-2.1.0',
                      'env': {
                              'MAVEN_HOME': '${INSTALLDIR}',
                              'PATH':'%MAVEN_HOME%\\bin',
                              'MAVEN_OPTS': '-Xmx512m -XX:MaxPermSize=256'}},
            'liferayPortal': {
                               'zip': 'liferay-portal-tomcat-5.5-5.2.2.zip',
                               'dest': 'liferay-portal-5.2.2',
                               'tomcatDir': 'tomcat-5.5.27',
                               'env':{'CATALINA_HOME': '${INSTALLDIR}\\tomcat-5.5.27'}},
            'activemq': {'zip': 'apache-activemq-5.2.0-bin.zip', 'dest': 'apache-activemq-5.2.0'},
            'liferaySdk': {'zip': 'liferay-plugins-sdk-5.2.2.zip', 'dest': ''},
            'intalioServer': {'zip': 'intalio-bpms-5.2.1.021.zip'},
            'mysqlServer': {'dest': 'mysql-server-5.1',
                             'name': 'MySQLServer51', 'vers': '5.1.34',
                             'user': 'root', 'password': 'neoxia',
                             'msi': 'mysql-5.1.34-win32.msi',
                             'msiOpts': '/qn /i', #intall in silent mode (must end with /i)
                             'msiProps': {'INSTALLDIR': '${INSTALLDIR}', 'DATADIR': '${INSTALLDIR}\\Data'}},
            'hyperichq': {'dest':'hyperic-hq-4.1.0',
                          'msi': 'hyperic-hq-installer-4.1.0-win32.msi',
                          'msiOpts': '/qn /i', #intall in silent mode (must end with /i)
                          'msiProps': {'INSTALLDIR': '${INSTALLDIR}','HQ_ENGINE_JNP_PORT': '10001',
                                      'HQ_ENGINE_PORT': '10002','SERVER_ADMIN_EMAIL': 'eric.kedji@gmail.com',
                                      'SERVER_ADMIN_USER': 'neoxia','SERVER_ADMIN_PASSWORD': 'neoxia',
                                      'SERVER_DATABASE_USER': 'neoxia','SERVER_DATABASE_PASSWORD': 'neoxia',
                                      'SERVER_POSTGRESQL_PORT': '10003','SERVER_WEBAPP_HOST': '',
                                      'SERVER_WEBAPP_PORT': '','SERVER_WEBAPP_SECURE_PORT': '',
                                      'HQ_START_SERVICES': '1','AGENT_IS_SECURE': '',
                                      'AGENT_PORT': '10004','AGENT_SERVER_USER': '',
                                      'AGENT_SERVER_PASSWORD': ''}},
}

if __name__ == '__main__':
    options,args=optionparse.parse(__doc__)
    if not args and not options:
        optionparse.exit()
    
    if options.mysqlServer:
        options.liferayServer = True
        options.mysql4liferay = True
    if options.liferaySdk:
        options.liferayPortal = True
        options.ant = True
    if options.all:
        for option in options.__dict__:
            if type(getattr(options, option)) == bool and option != 'test':
                setattr(options, option, True)
    
    # copier le mot de passe (ugly, really)
    packages['mysqlServer']['password'] = options.password
    packages['hyperichq']['msiProps']['SERVER_ADMIN_PASSWORD'] = options.password
    packages['hyperichq']['msiProps']['SERVER_DATABASE_PASSWORD'] = options.password
        
    if not os.path.exists(options.dest):
        os.mkdir(dest)
    if not os.path.exists(options.source):
        print '! Erreur: le répertoire source n\'existe pas.'
        exit(1)
    
    print '--- Installation de la plateforme SOA ---'
    print ' Source: ', options.source
    print ' Destination: ', options.dest
    print '-----------------------------------------'

    # augment package data with automatically deductible info
    for name, data in packages.items():
        if 'zip' in data and 'dest' not in data:
            packages[name]['dest'] = data['zip'][:-4] # strip '.zip'
        packages[name]['dest'] = pjoin(options.dest, name, packages[name]['dest'])
        
    penv = Penv()
    
    # extract files, install MSI archives, and create environmental vars
    for name, data in packages.items():
        if not getattr(options, name):
            continue
        if 'zip' in data:
            print '> Extraction: ' + name + ' ...'
            if not options.test: extract(pjoin(options.source, data['zip']), pjoin(options.dest, name))
        if 'msi' in data:
            cmd = 'msiexec ' + data['msiOpts'] + ' ' + pjoin(options.source, data['msi']) + ' '
            for key, value in data['msiProps'].items():
                if value != '':
                    value = packages[name]['msiProps'][key] = value.replace('${INSTALLDIR}', data['dest'])
                    cmd = cmd + ' ' + key + '=' + value
            target = pjoin(options.dest, name)
            if not os.path.exists(target):
                print '> Création de répertoire: ', target
                if not options.test: os.mkdir(target)
                 # we are not extracting a zip, so destination does not exist
                print '> Création de répertoire: ', data['dest']
                if not options.test: os.mkdir(data['dest'])
            print '> Execution: ' + cmd + '...'
            if not options.test: os.system(cmd)
        if 'env' in data:
            for key, value in data['env'].items():
                value = packages[name]['env'][key] = value.replace('${INSTALLDIR}', data['dest'])
                print '> Variable d\'environnement: ', key, '\t = ', value
                if not options.test: penv.set(key, value)
    
    # Install Hyperic plugin
    # WARNING: the directory 'hq-plugins' must exist prior to the HypericHQ
    # server startup, if you want the plugin hot-reload feature
    if options.hyperichq:
        pluginDir = pjoin(packages['hyperichq']['dest'], 'hq-plugins')
        if not os.path.exists(pluginDir):
            print 'Création de répertoire: ', pluginDir
            if not options.test: os.mkdir(pluginDir)
        source = pjoin(options.source, 'mule-plugin.xml')
        print '> Copie: ', source, ' -> ', pluginDir
        if not options.test: shutil.copy(source, pluginDir)

    # Use alternate config so Liferay runs on port 9000 (this *should* be an option)
    if options.liferayPortal:
        tomcatConf = pjoin(packages['liferayPortal']['dest'], packages['liferayPortal']['tomcatDir'], 'conf', 'server.xml')
        source = pjoin(options.source, 'tomcat-server.xml')
        print '> Copie: ', source, ' -> ', tomcatConf
        if not options.test:shutil.copy(source, tomcatConf)
        
    # generate MySQL configuration file
    if options.mysqlServer:
        mysqlHome = packages['mysqlServer']['dest']
        mysqlName = packages['mysqlServer']['name']
        mysqlVers = packages['mysqlServer']['vers']
        mysqlPass = packages['mysqlServer']['password']
        mysqlConfigCommand = 'MySQLInstanceConfig.exe" -i -q     \
-l"%s\MySQLInstanceConfigLog.txt"    \
-n"%s"                    \
-p"%s"                    \
-v%s                      \
-t"%s\my-template.ini"    \
-c"%s\my.ini"             \
ServiceName=%s            \
AddBinToPath=yes          \
ServerType=SERVER         \
DatabaseType=MIXED        \
ConnectionUsage=DSS       \
SkipNetworking=no         \
StrictMode=yes            \
Charset=utf8              \
RootPassword=%s' % (mysqlHome, mysqlName, mysqlHome, mysqlVers, mysqlHome, mysqlHome, mysqlName, mysqlPass)
        # a bug in the windows command interpreter causes it to fail on commands with more than
        # one pair of quotes. The fix is to use 'call [command-line]'.
        # see: http://bugs.python.org/issue1524
        cmd = 'call "' + pjoin(mysqlHome, 'bin', mysqlConfigCommand)
        print'> Execution: ', cmd , ' ...'
        if not options.test: os.system(cmd)
        # Now, patch the braindead mess MySQLInstanceConfig.exe & mysqld & friends do at startup
        # about config files by appendind datadir=$DATADIR/data to my.ini
        # see http://dev.mysql.com/doc/refman/5.1/en/windows-troubleshooting.html
        # and http://dev.mysql.com/doc/refman/5.1/en/windows-create-option-file.html
        # l'appel précédent à MySQLInstanceConfig.exe va tenter de démarrer le service, mais va échouer
        # il nous sert pourtant parce qu'il ve créer my.ini, que nous allons patcher
        cmd = 'call echo datadir=%s >> "%s"' % (pjoin(packages['mysqlServer']['msiProps']['DATADIR'], 'data').replace(os.path.sep, '/'),
                                           pjoin(packages['mysqlServer']['dest'], 'my.ini'))
        print'> Execution: ', cmd , ' ...'
        print '  (wrapped into NET STOP/START %s)' % (mysqlName)
        if not options.test:
            os.system('NET STOP %s' % (mysqlName)) # il va se plaint, mais n'y fait pas attention
            time.sleep(5) # give the service some time to stop
            os.system(cmd)
            os.system('NET START %s' % (mysqlName))
            time.sleep(5) # give the service some time to start
        # étrange, mais MySQLInstanceConfig.exe ne configure pas le mot de passe root
        cmd = pjoin(mysqlHome, 'bin', 'mysqladmin') + ' -u root password %s' % (mysqlPass)
        print'> Execution: ', cmd , ' ...'
        if not options.test: os.system(cmd)
        # Est-ce nécessaire ensuite de donner tous les privilèges à root?
        # il devrait les avoir par défaut non?
        # mysql -u root
        # GRANT ALL PRIVILEGES ON *.* TO 'Root'@'%' IDENTIFIED BY 'pass';
        # FLUSH PRIVILEGES;
        # exit 

    # create the liferay database in mysql
    if options.mysql4liferay:
        portalDBCreateCmd = '%s\\bin\\mysql --user=root --password=%s --execute="create database lportal character set utf8"' % (mysqlHome, mysqlPass)
        if not options.test: os.system(portalDBCreateCmd)
        # configure Liferay to use Mysql
        file = pjoin(
                     packages['liferayPortal']['dest'],
                     packages['liferayPortal']['tomcatDir'],
                     'webapps\\ROOT\\WEB-INF\\classes\\portal-ext.properties')
        config = '''
jdbc.default.driverClassName=com.mysql.jdbc.Driver
jdbc.default.url=jdbc:mysql://localhost/lportal?useUnicode=true&characterEncoding=UTF-8&useFastDateParsing=false
jdbc.default.username=%s
jdbc.default.password=%s
        ''' % (packages['mysqlServer']['user'], packages['mysqlServer']['password'])
        if not options.test:
            print '> Fichier de configuration: ', file
            portalJdbcConfig = open(file, 'w')
            portalJdbcConfig.write(config)
            portalJdbcConfig.close();
    
    if options.liferaySdk:
        # configure tomcat directory for Liferay SDK
        file = pjoin(packages['liferaySdk']['dest'], 'build.' + os.environ['USERNAME'] + '.properties')
        config = '''
app.server.dir=%s\\%s
        ''' % (packages['liferayPortal']['dest'], packages['liferayPortal']['tomcatDir'])
        if not options.test:
            print '> Fichier de configuration: ', file
            portalTomcatConfig = open(file, 'w')
            portalTomcatConfig.write(config)
            portalTomcatConfig.close()
            # should we add additionnal modifications to enable hot-deploy, etc?
    
    # add additionnal libraries (TOMCAT native library, etc)
    if options.libraries:
        source = pjoin(options.source, 'lib')
        dest = pjoin(options.dest, 'lib')
        
        print '> Copie: ', source, ' -> ', dest
        if not options.test: shutil.copytree(source, dest)
        
        print '> Variable d\'environnement: PATH = ', dest
        if not options.test: penv.set('PATH', dest)
    
    print
    print ">> Installation terminée avec succès <<"
