#!/bin/bash
CONFIG_FILE="config.ini"
read -p "Hány adatbázist szeretnél hozzáadni? " db_count
> $CONFIG_FILE 
for i in $(seq 1 $db_count)
do
    read -p "Add meg az adatbázis nevét: " db_name
    echo "[$db_name]" >> $CONFIG_FILE
    read -p "Add meg a felhasználónevet a(z) $db_name-hoz: " db_user
    echo "user = $db_user" >> $CONFIG_FILE
    read -sp "Add meg a jelszót a(z) $db_name-hoz: " db_password
    echo "" 
    echo "password = $db_password" >> $CONFIG_FILE
    echo "" 
done
gpg -c $CONFIG_FILE
rm $CONFIG_FILE
echo "Konfigurációs fájl létrehozva és titkosítva $CONFIG_FILE.gpg néven"