
find $1 -type f -name "*.a" -exec sh -c 'echo "Checking {}"; readelf -s {} 2>/dev/null | grep '$2' ' \;

find $1 -type f -name "*.a" -exec sh -c 'echo "Checking {}"; nm {} 2>/dev/null | grep -w "U '$2' "' \;
