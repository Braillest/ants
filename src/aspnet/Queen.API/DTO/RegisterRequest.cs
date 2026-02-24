using System.ComponentModel.DataAnnotations;

namespace Queen.API.DTO;

/// <summary>
/// Represents the JSON payload for a register request.
/// </summary>
public class RegisterRequest
{
    [Required]
    [StringLength(50, MinimumLength = 3)]
    public string Username { get; set; } = string.Empty;

    [Required]
    [StringLength(50, MinimumLength = 3)]
    public string DisplayName { get; set; } = string.Empty;

    [Required]
    [StringLength(100, MinimumLength = 3)]
    public string Password { get; set; } = string.Empty;

    [Required]
    [StringLength(100, MinimumLength = 3)]
    public string ConfirmPassword { get; set; } = string.Empty;

    [Required]
    [StringLength(256, MinimumLength = 6)]
    public string Token { get; set; } = string.Empty;
}
