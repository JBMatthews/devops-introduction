
nginx installation
  Package "nginx"
    should be installed
  Service "nginx"
    should be running

mysql installation
    
    should be installed
  Service "mysql"
    should be running

php installation
  Package "php"
    should be installed
  Service "php7.0-fpm"
    should be running
  Command "php --version"
    stdout
      should contain "PHP 7"

wordpress
  File "/var/www/book.example.com/wp-config.php"
    should exist
  Command "mysql -u root michaelwp -e "SELECT post_title FROM wp_posts WHERE id=1;""
    stdout
      should contain "Hey There"

Finished in 0.35718 seconds (files took 0.51265 seconds to load) 9 examples, 0 failures
