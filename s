server {
    listen 80;
    server_name 192.168.0.47;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/jitendra/Desktop/Deep/1.Django/Django_Dummy/bookstall;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
