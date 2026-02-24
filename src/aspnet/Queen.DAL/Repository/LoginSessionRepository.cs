using Queen.DAL.Entity.Users;

namespace Queen.DAL.Repository;

public class LoginSessionRepository: Repository<LoginSession>
{
    public LoginSessionRepository(ApplicationDbContext context) : base(context) { }
}
