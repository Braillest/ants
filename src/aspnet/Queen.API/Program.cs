using Queen.DAL;
using Queen.DAL.Repository;
using Queen.Service;
using Microsoft.EntityFrameworkCore;
using System;

var builder = WebApplication.CreateBuilder(args);

string? username = Environment.GetEnvironmentVariable("MARIADB_USERNAME");
string? password = Environment.GetEnvironmentVariable("MARIADB_PASSWORD");
string? server = Environment.GetEnvironmentVariable("MARIADB_SERVER");
string? database = Environment.GetEnvironmentVariable("MARIADB_DATABASE");

if (username == null || password == null || server == null || database == null)
{
    throw new Exception("MARIADB environment variables not set.");
}

string MariaDBConnection = $"Server={server};Database={database};User={username};Password={password};";

builder.Services.AddControllers();
builder.Services.AddOpenApi();
builder.Services.AddDbContext<ApplicationDbContext>(options => options.UseMySql(MariaDBConnection, new MySqlServerVersion(new Version(10, 11, 15))));
builder.Services.AddScoped(typeof(IRepository<>), typeof(Repository<>));
builder.Services.AddScoped<UserRepository>();
// builder.Services.AddScoped<UserService>();

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
