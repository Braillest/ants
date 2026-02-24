using System.ComponentModel.DataAnnotations.Schema;

namespace Queen.DAL.Entity;

[Table("FilePointers")]
public class FilePointer: IEntity
{
    public int Id { get; set; }
    public string? Name { get; set; }
    public string? AbsolutePath { get; set; }
    public string? Type { get; set; }
    public int? Size { get; set; }
    public DateTime? CreatedAt { get; set; }
    public DateTime? UpdatedAt { get; set; }
}
