using Queen.DAL;
using Queen.DAL.Repository;
using Queen.Service;
using Microsoft.EntityFrameworkCore;
using System.IO;

var builder = WebApplication.CreateBuilder(args);

// MariaDB initialization
string? username = Environment.GetEnvironmentVariable("MARIADB_USERNAME");
string? password = Environment.GetEnvironmentVariable("MARIADB_PASSWORD");
string? server = Environment.GetEnvironmentVariable("MARIADB_SERVER");
string? database = Environment.GetEnvironmentVariable("MARIADB_DATABASE");

if (username == null || password == null || server == null || database == null)
{
    throw new Exception("MARIADB environment variables not set.");
}

string MariaDBConnection = $"Server={server};Database={database};User={username};Password={password};";

// Redis initialization
string? redisConnection = Environment.GetEnvironmentVariable("REDIS_CONNECTION");

if (redisConnection == null)
{
    throw new Exception("REDIS_CONNECTION environment variable not set.");
}

builder.Services.AddControllers();
builder.Services.AddOpenApi();
builder.Services.AddDbContext<ApplicationDbContext>(options => options.UseMySql(MariaDBConnection, new MySqlServerVersion(new Version(10, 11, 15))));
// Repositories
builder.Services.AddScoped<UserRepository>();
builder.Services.AddScoped<LoginSessionRepository>();
builder.Services.AddScoped<LoginAttemptRepository>();
builder.Services.AddScoped<FilePointerRepository>();
builder.Services.AddScoped<ProjectRepository>();
// Services
builder.Services.AddScoped<UserService>();
// Session
builder.Services.AddStackExchangeRedisCache(options =>
{
    options.Configuration = redisConnection;
    options.InstanceName = "Queen_";
});
builder.Services.AddSession(options =>
{
    options.IdleTimeout = TimeSpan.FromMinutes(60 * 24);
    options.Cookie.HttpOnly = true;
    options.Cookie.IsEssential = true;
});

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseAuthorization();
app.MapControllers();
app.Run();
