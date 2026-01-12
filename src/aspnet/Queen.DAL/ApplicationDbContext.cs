using Queen.DAL.Entity;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;

namespace Queen.DAL;

public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(){}

    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options): base(options){}

    public DbSet<User> Users { get; set; } = null!;

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        // if (!optionsBuilder.IsConfigured)
        // {
        //     // Build configuration from appsettings.json
        //     var config = new ConfigurationBuilder()
        //         .SetBasePath(Path.Combine(Directory.GetCurrentDirectory(), "../Queen.API"))
        //         .AddJsonFile("appsettings.json")
        //         .Build();

        //     var connectionString = config.GetConnectionString("MariaDBConnection");
        //     optionsBuilder.UseMySql(connectionString, new MySqlServerVersion(new Version(10, 11, 15)));
        // }
    }
}