rm -rf ./build/*
mkdir -p build
cmake -B build -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release
make -C build 