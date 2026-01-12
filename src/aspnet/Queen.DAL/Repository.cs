using Microsoft.EntityFrameworkCore;
using System.Collections.Generic;
using System.Linq.Expressions;
using System.Threading.Tasks;

namespace Queen.DAL;

// Create custom repo classes extending this one to modify or extend functionality

public class Repository<T> : IRepository<T> where T : class
{
    private readonly ApplicationDbContext _context;
    private readonly DbSet<T> _dbSet;

    public Repository(ApplicationDbContext context)
    {
        _context = context;
        _dbSet = _context.Set<T>();
    }

    // Sync methods

    // Read

    public IEnumerable<T> FindAll()
    {
        return _dbSet.ToList().AsEnumerable();
    }

    public IEnumerable<T> FindBy(Expression<Func<T, bool>> predicate)
    {
        return _dbSet.Where(predicate).AsEnumerable();
    }

    public T? FindOneBy(Expression<Func<T, bool>> predicate)
    {
        return _dbSet.Where(predicate).FirstOrDefault();
    }

    public T? FindById(int id)
    {
        return _dbSet.Find(id);
    }

    // Write

    public void Add(T entity)
    {
        _dbSet.Add(entity);
    }

    public void AddAll(IEnumerable<T> entities)
    {
        _dbSet.AddRange(entities);
    }

    public void Update(T entity)
    {
        _dbSet.Update(entity);
    }

    // Delete

    public void Delete(int id)
    {
        T? entity = FindById(id);

        if (entity != null)
        {
            _dbSet.Remove(entity);
        }
    }

    public void Delete(T entity)
    {
        _dbSet.Remove(entity);
    }

    // Execute

    public void Save()
    {
        _context.SaveChanges();
    }

    // Async methods

    // Read

    public async Task<IEnumerable<T>> FindAllAsync()
    {
        return await _dbSet.ToListAsync();
    }

    public async Task<IEnumerable<T>> FindByAsync(Expression<Func<T, bool>> predicate)
    {
        return await _dbSet.Where(predicate).ToListAsync();
    }

    public async Task<T?> FindOneByAsync(Expression<Func<T, bool>> predicate)
    {
        return await _dbSet.Where(predicate).FirstOrDefaultAsync();
    }

    public async Task<T?> FindByIdAsync(int id)
    {
        return await this._dbSet.FindAsync(id);
    }

    // Write

    public async Task AddAsync(T entity)
    {
        await _dbSet.AddAsync(entity);
    }

    public async Task AddAllAsync(IEnumerable<T> entities)
    {
        await _dbSet.AddRangeAsync(entities);
    }

    // Update and Delete are not IO blocking operations,

    // void Update(T entity);
    // Delete
    // void Delete(int id);
    // void Delete(T entity);

    // Execute
    public async Task SaveAsync()
    {
        await _context.SaveChangesAsync();
    }
}
