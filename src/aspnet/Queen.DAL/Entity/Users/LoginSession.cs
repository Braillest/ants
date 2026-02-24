namespace Queen.DAL.Entity.Users;

public class LoginSession: IEntity
{
    public LoginSession()
    {
        CreatedAt = DateTime.Now;
        UpdatedAt = DateTime.Now;
    }

    public LoginSession(LoginSession loginSession)
    {
        this.Id = loginSession.Id;
        this.UserId = loginSession.UserId;
        this.Token = loginSession.Token;
        this.IPAddress = loginSession.IPAddress;
        this.UserAgent = loginSession.UserAgent;
        this.CreatedAt = loginSession.CreatedAt;
        this.UpdatedAt = loginSession.UpdatedAt;
        this.ExpiresAt = loginSession.ExpiresAt;
        this.IsActive = loginSession.IsActive;
    }

    // Main
    public int Id { get; set; }
    public required int? UserId { get; set; }
    public required string? Token { get; set; }
    public string? IPAddress { get; set; }
    public string? UserAgent { get; set; }

    // Meta
    public DateTime CreatedAt { get; set; } = DateTime.Now;
    public DateTime UpdatedAt { get; set; } = DateTime.Now;
    public DateTime? ExpiresAt { get; set; } = DateTime.Now.AddDays(30);
    
    // IsActive updated with successful TokenHash validation.
    public bool IsActive { get; set; } = false;

    // Navigation
    public User? User { get; set; }
}
