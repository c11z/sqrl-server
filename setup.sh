sudo mkdir logs
sudo cp ~/secret.py gator/
cd ../
sudo chown -R apache:apache gator-server
sudo chmod  -R 755 gator-server
sudo /etc/init.d/httpd restart