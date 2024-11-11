from Misc.functions import hash_password

password = "admin123"
hashed = hash_password(password)
print(f"Hashed password: {hashed}")
#to create admin id
#email: admin@gmail.com
#password: admin123

#to run this sql query
#mysql -u root -p lms
#INSERT INTO `admin` (`email`, `password`) VALUES ('admin@gmail.com', '$argon2id$v=19$m=65536,t=3,p=2$Kf+XpJXQZsxUDXqvfm7vAQ$MD9ngtvp9EnXjVUwBTxpvU5KMYcVMhafwsuAxPDVtmY');