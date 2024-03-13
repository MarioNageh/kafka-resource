#!/bin/bash

# Start Kafka Manager
./bin/kafka-manager -Dconfig.file=${KM_HOME}/conf/application.conf


#!/bin/bash

# Print debugging information
echo "Current directory contents:"
ls -la

# Start Kafka Manager
./bin/cmak -Dconfig.file=${KM_HOME}/conf/application.conf