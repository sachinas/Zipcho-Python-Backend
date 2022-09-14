#!/bin/bash

mysql -u root -password root << EOF
USE zipchoDoc;
GRANT ALL PRIVILEGES ON *.* TO 'root';
EOF