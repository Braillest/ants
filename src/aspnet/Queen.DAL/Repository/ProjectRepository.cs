using Queen.DAL.Entity;

namespace Queen.DAL.Repository;

public class ProjectRepository: Repository<Project>
{
    public ProjectRepository(ApplicationDbContext context) : base(context) { }
}
