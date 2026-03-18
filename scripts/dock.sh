docker run -it -d \
  --name muclib \
  --network bridge \
  -p 2223:22 \
  -p 8080:80 \  # 如果需要其他端口
  -w /builds/ \
  -v $(pwd)/builds:/builds \
  --env-file .env \
  registry.tpt.com:80/terapines-ci/ubuntu22-x64-dev-toolchain:20241220 \
  bash