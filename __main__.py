import instaloader

username = "username"
password = "password"


L = instaloader.Instaloader()
L.login(username, password)  # (login)


profile = instaloader.Profile.from_username(L.context, username)

# Print list of followees
follow_list = [f for f in profile.get_followers()]

f = follow_list[4]

followers_of_f = [f.get_followers()]
for ff in followers_of_f:
    print(ff)


