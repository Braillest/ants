using System.ComponentModel.DataAnnotations.Schema;
using Queen.DAL.Entity.Users;

namespace Queen.DAL.Entity;

[Table("Projects")]
public class Project : IEntity
{
    public Project()
    {
        CreatedAt = DateTime.UtcNow;
        UpdatedAt = DateTime.UtcNow;
        IsActive = true;
    }

    public int Id { get; set; }

    public string? Name { get; set; }
    public string? Description { get; set; }

    public User? Owner { get; set; }

    public int? FileCount { get; set; }
    public List<FilePointer>? FilePointers { get; set; }

    public int? BrailleOutputCols { get; set; }
    public int? BrailleOutputRows { get; set; }

    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }
    public bool IsActive { get; set; }
}