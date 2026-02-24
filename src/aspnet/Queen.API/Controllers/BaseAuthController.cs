using Queen.DAL;
using Queen.DAL.Repository;
using Queen.Service;
using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;

namespace Queen.API.Controllers;

public class BaseAuthController<TRepo, TEntity> : BaseController<TRepo, TEntity>
where TRepo : IRepository<TEntity>
where TEntity : class, IEntity
{
    protected UserService _userService;

    public BaseAuthController(TRepo repository, UserService userService)
    : base(repository)
    {
        _userService = userService;
    }

    private bool UserIsAuthenticated()
    {
        string? token = HttpContext.Session.GetString("token");

        if (token != null)
        {
            bool isTokenValid = _userService.ValidateSessionToken(token);

            if (isTokenValid)
            {
                return true;
            }
        }

        return false;
    }

    [HttpGet]
    public override IActionResult Index()
    {
        if (!UserIsAuthenticated())
        {
            return Unauthorized();
        }

        return base.Index();
    }

    [HttpGet("{id}")]
    public override IActionResult Show(int id)
    {
        if (!UserIsAuthenticated())
        {
            return Unauthorized();
        }

        return base.Show(id);
    }

    [HttpPost]
    public override IActionResult Create([FromBody] TEntity newEntity)
    {
        if (!UserIsAuthenticated())
        {
            return Unauthorized();
        }

        return base.Create(newEntity);
    }

    [HttpPut("{id}")]
    public override IActionResult Update(int id, [FromBody] TEntity updatedEntity)
    {
        if (!UserIsAuthenticated())
        {
            return Unauthorized();
        }

        return base.Update(id, updatedEntity);
    }

    [HttpDelete("{id}")]
    public override IActionResult Delete(int id)
    {
        if (!UserIsAuthenticated())
        {
            return Unauthorized();
        }

        return base.Delete(id);
    }
}
