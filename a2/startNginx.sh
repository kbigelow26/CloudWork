mkdir static-html-directory
echo "FROM nginx
COPY static-html-directory /usr/share/nginx/html" > Dockerfile
echo "<html>
<body>
It works!
</body>
</html>" > static-html-directory/index.html
docker build -t some-content-nginx .
docker run --name some-nginx -d -p 8080:80 some-content-nginx