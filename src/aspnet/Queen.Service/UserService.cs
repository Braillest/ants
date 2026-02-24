using Microsoft.Extensions.Caching.Distributed;
using System.Security.Cryptography;
using System.Text.Json;
using Queen.DAL;
using Queen.DAL.Entity.Users;
using Queen.DAL.Repository;

namespace Queen.Service;

public class UserService
{
    private readonly LoginSessionRepository _loginSessionRepository;
    private readonly UserRepository _userRepository;
    private readonly IDistributedCache _cache;

    private readonly int _saltSize = 32;
    private readonly int _sessionTokenSize = 32;

    public UserService(LoginSessionRepository loginSessionRepository, UserRepository userRepository, IDistributedCache cache)
    {
        _loginSessionRepository = loginSessionRepository;
        _userRepository = userRepository;
        _cache = cache;
    }

    // Creates a user record with the supplied data and assumes username has already been vetted.
    public void CreateUser(string username, string displayName, string password)
    {
        // Assemble and persist user
        byte[] salt = this.GenerateSalt();
        string passwordHash = this.HashPassword(salt, password);
        User user = new User()
        {
            Username = username,
            PasswordHash = passwordHash,
            DisplayName = displayName,
        };
        _userRepository.Add(user);
        _userRepository.Save();
    }

    public User? GetUser(string username)
    {
        // Lookup user by username and obtain stored passwordHash
        User? user = _userRepository.FindOneBy(user => user.Username == username);
        return user;
    }

    public void AddLoginAttempt(User? user, string remoteIPAddress, string userAgent)
    {
        // Create login attempt record
        LoginAttempt newLoginAttempt = new LoginAttempt();
        newLoginAttempt.IPAddress = remoteIPAddress;
        newLoginAttempt.UserAgent = userAgent;

        // Initialize LoginAttempts property
        // - This might be changed in the future.
        // - Currently LoginAttempts is null because it is not included in the GetUser query nor initialized by the entity.
        // - This does seem to add a login attempt record as expected and not nuke the other records.
        user.LoginAttempts = [];
        user.LoginAttempts.Add(newLoginAttempt);
        _userRepository.Update(user);
        _userRepository.Save();
    }

    public LoginSession AddLoginSession(User user, string remoteIPAddress, string userAgent)
    {
        // Create login session
        string sessionToken = this.GenerateSessionToken();
        LoginSession newLoginSession = new LoginSession()
        {
            UserId = user.Id,
            Token = sessionToken,
            IPAddress = remoteIPAddress,
            UserAgent = userAgent,
            ExpiresAt = DateTime.Now.AddDays(30),
            IsActive = true
        };
        _loginSessionRepository.Add(newLoginSession);
        _loginSessionRepository.Save();

        return newLoginSession;
    }

    public bool ValidateSessionToken(string sessionToken)
    {
        LoginSession? loginSession = _loginSessionRepository.FindOneBy(s => s.Token == sessionToken);
    
        if (loginSession == null)
        {
            return false;
        }

        if (loginSession.IsActive == false)
        {
            return false;
        }

        if (loginSession.ExpiresAt < DateTime.Now)
        {
            // Set the session token as inactive, as it has expired.
            loginSession.IsActive = false;
            _loginSessionRepository.Update(loginSession);
            _loginSessionRepository.Save();
            return false;
        }

        return true;
    }

    public byte[] GenerateSalt()
    {
        return RandomNumberGenerator.GetBytes(_saltSize);
    }

    public string GenerateSessionToken()
    {
        byte[] bytes = RandomNumberGenerator.GetBytes(_sessionTokenSize);
        return Convert.ToBase64String(bytes);
    }

    public string HashPassword(byte[] salt, string password)
    {
        // Generate one-way password hash using salt
        using Rfc2898DeriveBytes pbkdf2 = new Rfc2898DeriveBytes(password, salt, 100000, HashAlgorithmName.SHA256);
        byte[] hash = pbkdf2.GetBytes(32);

        // Combine and return passwordHash (salt + hash)
        byte[] result = new byte[salt.Length + hash.Length];
        Buffer.BlockCopy(salt, 0, result, 0, salt.Length);
        Buffer.BlockCopy(hash, 0, result, salt.Length, hash.Length);
        return System.Convert.ToBase64String(result);
    }

    public bool ValidatePassword(string password, string passwordHash)
    {
        // Extract salt
        byte[] passwordHashBytes = System.Convert.FromBase64String(passwordHash);
        byte[] salt = new byte[_saltSize];
        Buffer.BlockCopy(passwordHashBytes, 0, salt, 0, _saltSize);

        // Generate password hash with incoming password and extracted salt
        string generatedPasswordHash = this.HashPassword(salt, password);

        // PasswordHashes do not match case
        if (generatedPasswordHash != passwordHash)
        {
            return false;
        }

        return true;
    }
}
