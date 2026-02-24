namespace Queen.API.DTO;

public class ChunkRequest
{
    public int FileId { get; set; }
    public long Offset { get; set; }
    public long Size { get; set; }
}
