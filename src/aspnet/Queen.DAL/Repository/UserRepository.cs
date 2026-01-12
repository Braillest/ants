using Queen.DAL.Entity;

namespace Queen.DAL.Repository;

public class UserRepository: Repository<User>
{
    public UserRepository(ApplicationDbContext context) : base(context) { }
}
