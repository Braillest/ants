using Queen.DAL;
using Queen.DAL.Entity;
using Queen.DAL.Repository;

namespace Queen.API.Controllers;

public class ProjectController: BaseController<ProjectRepository, Project>
{
    public ProjectController(ProjectRepository repository) : base(repository)
    {
    }
}
