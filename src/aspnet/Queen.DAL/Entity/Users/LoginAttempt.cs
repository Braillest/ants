namespace Queen.DAL.Entity.Users;

public class LoginAttempt: IEntity
{
    // Main
    public int Id { get; set; }
    public string? IPAddress { get; set; }
    public string? UserAgent { get; set; }

    // Meta
    public DateTime CreatedAt { get; set; } = DateTime.Now;
}
