from Misc.functions import hash_password, verify_password

password = "admin123"
hashed = '$argon2id$v=19$m=65536,t=3,p=2$Kf+XpJXQZsxUDXqvfm7vAQ$MD9ngtvp9EnXjVUwBTxpvU5KMYcVMhafwsuAxPDVtmY'
print(f"Hashed password: {hashed}")
print(verify_password(hashed, password))
#to create admin id
#email: admin@gmail.com
#password: admin123

#to run this sql query
#mysql -u root -p lms
#INSERT INTO `admin` (`email`, `password`) VALUES ('admin@gmail.com', '$argon2id$v=19$m=65536,t=3,p=2$Kf+XpJXQZsxUDXqvfm7vAQ$MD9ngtvp9EnXjVUwBTxpvU5KMYcVMhafwsuAxPDVtmY');