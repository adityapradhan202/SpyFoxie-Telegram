# admin-credentials

import os
import dotenv
dotenv.load_dotenv()

from pswd_encrypt import password_hasher, verify_password

admin_username1 = os.getenv("ADMIN-USERNAME-1")
admin_username2 = os.getenv("ADMIN-USERNAME-2")
admin_pswd1 = os.getenv("ADMIN-KEY-1")
admin_pswd2 = os.getenv("ADMIN-KEY-2")

admin_data = {
    admin_username1:password_hasher(admin_pswd1),
    admin_username2:password_hasher(admin_pswd2)
}



if __name__ == "__main__":
    admin_hashed_pswd1 = password_hasher(admin_pswd1)
    print(admin_hashed_pswd1)
    print(type(admin_hashed_pswd1))

    pswd = input("Enter password: ")
    
    if verify_password(pswd, admin_hashed_pswd1):
        print("Password matched!")

    print("These are the admin credentials...")
    print(admin_data)