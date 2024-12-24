server {
    listen 80;
    server_name my_website.com;
    root /var/www/my_website;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}

<html>
  <head><title>Welcome to My Website</title></head>
  <body><h1>Test 2 web.site</h1></body>
</html>