from argon2 import PasswordHasher, exceptions
import timeago, datetime

# Initialize the PasswordHasher with custom settings
ph = PasswordHasher(time_cost=3, memory_cost=64 * 1024, parallelism=2)

def hash_password(password):
    """
    Hashes the password using Argon2 with secure settings.
    """
    return ph.hash(password)

def verify_password(stored_hash, provided_password):
    """
    Verifies the provided password against the stored Argon2 hash.
    Returns True if the password matches, otherwise False.
    """
    try:
        return ph.verify(stored_hash, provided_password)
    except exceptions.VerifyMismatchError:
        # Passwords do not match
        return False
    except exceptions.VerificationError:
        # Other errors like invalid hash format
        return False
    
def ago(date):
    """
        Calculate a '3 hours ago' type string from a python datetime.
    """
    now = datetime.datetime.now() + datetime.timedelta(seconds = 60 * 3.4)

    return (timeago.format(date, now)) # will print x secs/hours/minutes ago