#you have to
# - setup JAVA_HOME
# - setup a symbol link to your local moco jar, e.g. ln -sf moco-runner-0.12.0-standalone.jar moco-runner-standalone.jar
$JAVA_HOME/bin/java -jar moco-runner-standalone.jar http -p 12311 -c A.json
