using Queen.DAL.Entity;

namespace Queen.DAL.Repository;

public class FilePointerRepository: Repository<FilePointer>
{
    public FilePointerRepository(ApplicationDbContext context) : base(context) { }
}
