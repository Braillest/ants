using Microsoft.AspNetCore.Mvc;
using Queen.API.DTO;
using Queen.DAL.Entity;
using Queen.DAL.Repository;

namespace Queen.API.Controllers;

// TODO: Access control via BaseAuthController
[Route("api/filepointer/")]
public class FilePointerController : BaseController<FilePointerRepository, FilePointer>
{
    public FilePointerController(FilePointerRepository repository) : base(repository) { }

    [HttpPost("chunk")]
    public async Task<IActionResult> Chunk([FromBody] ChunkRequest request)
    {
        // TODO: Access control

        // Create file context to referenced file.
        var filePointer = _repository.FindOneBy(e => e.Id == request.FileId);

        if (filePointer == null)
        {
            return NotFound(new { error = "File not found." });
        }

        if (filePointer.AbsolutePath == null)
        {
            return NotFound(new { error = "File path not defined." });
        }

        using (StreamReader fileStream = new(filePointer.AbsolutePath))
        {
            long length = fileStream.BaseStream.Length;

            if (length != filePointer.Size)
            {
                // TODO: Log warning
                Console.WriteLine($"File size does not match. Expected: {filePointer.Size}, Actual: {length}");
            }

            if (request.Offset >= length)
            {
                // TODO: Log warning
                return BadRequest(new { error = "Offset is greater than file length." });
            }

            if (request.Size > length)
            {
                // TODO: Log warning
                return BadRequest(new { error = "Size is greater than file length." });
            }

            long bytesToRead = Math.Min(request.Size, length - request.Offset);
            
            if (bytesToRead <= 0)
            {
                // TODO: Log warning
                return BadRequest(new { error = "Invalid offset or size." });
            }

            char[] buffer = new char[bytesToRead];
            fileStream.Read(buffer, (int)request.Offset, (int)bytesToRead);
            fileStream.Close();

            return Ok(new { data = new string(buffer) });
        }
    }
}
