注意：

在修改 *_nginx.conf 不会生效

真正起作用的文件是：/workspace/nginx/projects/*_nginx.conf

deploy/install.py 会将 ./nginx 下的配置复制到 /workspace/nginx/projects/ 中
