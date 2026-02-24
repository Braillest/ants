using Queen.DAL.Entity.Users;

namespace Queen.DAL.Repository;

public class LoginAttemptRepository : Repository<LoginAttempt>
{
    public LoginAttemptRepository(ApplicationDbContext context) : base(context) { }
}
