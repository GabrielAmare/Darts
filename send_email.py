import yagmail
import random


def send_email(zip_url: str, major: int, minor: int, patch: int):
    port = 465  # For SSL
    origin_email = "gabriel.amare.dev@gmail.com"
    password = "ccmbmowqmstadcwg"  # TODO : password uncrypted VERY UNSECURE (DO NOT SCALE THE APP WITH THIS INSIDE)
    TOKEN_CHARS = "abcdefghijklmnopqrstuvwxyzABDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"

    EMAILS_LIST = [
        "gabriel.amare.31@gmail.com",
        "jppbbc@gmail.com"
    ]

    def generate_token(token_length=10):
        return "".join(random.choice(TOKEN_CHARS) for _ in range(token_length))

    unsubscribe_token = generate_token()

    subject = f"nouvelle mise à jour Darts version {major}.{minor}.{patch}"
    contents = [
        f"Voici un lien vers la toute dernière version de l'application de comptage de scores Darts",
        f" sur Google Drive : {zip_url}"
        f"",
        f"Si vous ne voulez plus recevoir les mises à jour, veuillez cliquer sur le lien suivant pour vous désabonner",
        f"https://www.darts.com/updates/unsubscribe?token={unsubscribe_token}",
        f"",
        f"Ce mail est un mail automatique, mais vous pouvez nous répondre à cette adresse: gabriel.amare.dev@gmail.com",
    ]
    yag = yagmail.SMTP(user=origin_email, password=password)
    for target_email in EMAILS_LIST:
        yag.send(
            to=target_email,
            subject=subject,
            contents=contents
        )

    print("\nSuccessfully sent the emails to :\n", "\n".join("  - " + mail for mail in EMAILS_LIST))


# if __name__ == '__main__':
#     send_email("https://drive.google.com/file/d/1NE9yej6mNcBJMAOSPIv91ZG6FzH9HyBx/view?usp=sharing", 1, 0, 3)
