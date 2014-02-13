sudo mkdir logs
sudo cp /home/coryd/secret.py /var/www/html/gator-server/gator/
cd ../
sudo chown -R apache:apache gator-server
sudo chmod  -R 755 gator-server
sudo /etc/init.d/httpd restart