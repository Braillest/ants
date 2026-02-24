using Queen.DAL.Entity.Users;

namespace Queen.DAL.Repository;

public class UserRepository: Repository<User>
{
    public UserRepository(ApplicationDbContext context) : base(context) { }
}
