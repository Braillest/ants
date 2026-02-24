using System.ComponentModel.DataAnnotations;

namespace Queen.API.DTO;

/// <summary>
/// Represents the JSON payload for a login request.
/// </summary>
public class LoginRequest
{
    [Required]
    [StringLength(50, MinimumLength = 3)]
    public string Username { get; set; } = string.Empty;

    [Required]
    [StringLength(100, MinimumLength = 6)]
    public string Password { get; set; } = string.Empty;
}
