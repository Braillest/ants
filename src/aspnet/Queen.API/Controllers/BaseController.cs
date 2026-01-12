using Queen.DAL;
using Queen.DAL.Repository;
using Queen.Service;
using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;

namespace Queen.API.Controllers;

public class BaseController<TRepo, TEntity> : ControllerBase
where TRepo : IRepository<TEntity>
where TEntity : class, IEntity
{
    private readonly TRepo _repository;

    public BaseController(TRepo repository)
    {
        _repository = repository;
    }

    [HttpGet]
    public IEnumerable<TEntity> Index()
    {
        return _repository.FindAll();
    }

    [HttpGet("{id}")]
    public TEntity? Show(int id)
    {
        return _repository.FindOneBy(e => e.Id == id);
    }

    [HttpPost]
    public int? Create([FromBody] TEntity newEntity)
    {
        _repository.Add(newEntity);
        _repository.Save();
        return newEntity.Id;
    }

    [HttpPut("{id}")]
    public bool Update(int id, [FromBody] TEntity updatedEntity)
    {
        var existing = _repository.FindOneBy(e => e.Id == id);
        if (existing == null)
        {
            return false;
        }

        _repository.Update(updatedEntity);
        _repository.Save();
        return true;
    }

    [HttpDelete("{id}")]
    public bool Delete(int id)
    {
        var existing = _repository.FindOneBy(e => e.Id == id);
        if (existing == null)
        {
            return false;
        }

        _repository.Delete(existing);
        _repository.Save();
        return true;
    }
}
